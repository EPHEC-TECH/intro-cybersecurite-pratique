# DKIM (DomainKeys Identified Mail)

**Sources** : Proofpoint Threat Reference, dmarcian.com, RFC 6376
**RFC officielle** : https://datatracker.ietf.org/doc/html/rfc6376

---

## Définition

DKIM est un protocole d'authentification email qui permet à un expéditeur d'**apposer une signature cryptographique** sur ses emails. Cette signature prouve deux choses :
1. L'email a bien été envoyé par le domaine signataire
2. Le contenu de l'email n'a pas été modifié en transit

DKIM utilise une cryptographie asymétrique (paire de clés publique/privée).

**Origine** : DKIM est né en 2004 de la fusion de "Enhanced DomainKeys" (Yahoo) et "Identified Internet Mail" (Cisco).

---

## Comment DKIM fonctionne

```
CÔTÉ EXPÉDITEUR (à l'envoi)
─────────────────────────────────────────────
1. Sélection des champs à signer
   (From, Subject, To, Date, corps du message...)

2. Calcul d'un hash de ces champs
   Exemple : hash("From: alice@example.com\nSubject: Bonjour\n...")
   → "3303baf8986f910720abcfa607d81f53"

3. Chiffrement du hash avec la CLÉ PRIVÉE
   (stockée sur le serveur mail expéditeur, secrète)

4. Ajout du header DKIM-Signature à l'email
   avec le hash chiffré (valeur du tag b=)

CÔTÉ RÉCEPTEUR (à la réception)
─────────────────────────────────────────────
1. Lecture du header DKIM-Signature
   → Récupération du domaine (d=) et du sélecteur (s=)

2. Requête DNS pour récupérer la CLÉ PUBLIQUE
   → TXT record : s._domainkey.example.com

3. Déchiffrement de la signature avec la clé publique

4. Recalcul du hash des champs signés

5. Comparaison : hash reçu = hash recalculé ?
   → OUI → DKIM pass ✓ (message intègre)
   → NON → DKIM fail ✗ (message altéré ou clé incorrecte)
```

---

## Structure du header DKIM-Signature

Un header DKIM-Signature réel ressemble à ceci :

```
DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed;
        d=gmail.com; s=20230601;
        h=from:to:subject:date:message-id:mime-version:content-type;
        bh=47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU=;
        b=AbCdEfGhIjKlMnOpQrStUvWxYz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ
           abcdefghijklmnopqrstuvwxyz0123456789+/==
```

### Description de chaque tag

| Tag | Nom | Description | Exemple |
|-----|-----|-------------|---------|
| `v=` | Version | Toujours `1` | `v=1` |
| `a=` | Algorithme | Algorithme de signature | `a=rsa-sha256` |
| `c=` | Canonicalisation | Normalisation header/body avant hash | `c=relaxed/relaxed` |
| `d=` | Domaine | Domaine signataire (vérifié dans le DNS) | `d=gmail.com` |
| `s=` | Sélecteur | Identifie quelle clé DNS utiliser | `s=20230601` |
| `h=` | Headers | Liste des headers inclus dans la signature | `h=from:to:subject:date` |
| `bh=` | Body Hash | Hash du corps de l'email (base64) | `bh=47DEQpj8...` |
| `b=` | Signature | La signature cryptographique elle-même (base64) | `b=AbCdEf...` |
| `t=` | Timestamp | Date/heure de signature (optionnel) | `t=1698765432` |
| `x=` | Expiration | Date d'expiration de la signature (optionnel) | `x=1698851832` |
| `i=` | Identité | Identité de l'agent signataire (optionnel) | `i=@gmail.com` |

### Canonicalisation (`c=`)

La canonicalisation normalise les headers et le body avant de calculer le hash, pour tolérer certaines modifications bénignes :

| Mode | Description |
|------|-------------|
| `simple` | Strict : moindre modification invalide la signature |
| `relaxed` | Tolère changements mineurs (espaces, casse des noms de headers) |

Le format est `c=<header>/<body>`, par exemple `c=relaxed/relaxed`.

---

## Enregistrement DNS DKIM (clé publique)

La clé publique est publiée en DNS sous la forme :
```
<selector>._domainkey.<domaine>   IN   TXT   "v=DKIM1; k=rsa; p=<clé_publique_base64>"
```

Exemple réel :
```
20230601._domainkey.gmail.com   IN   TXT
  "v=DKIM1; k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC5N3lnvvrYgPCRSoqn8vr...AQAB"
```

**Comment trouver le sélecteur** : il est indiqué dans le tag `s=` du header DKIM-Signature.

**Vérification DNS en ligne de commande** :
```bash
dig TXT 20230601._domainkey.gmail.com
```

---

## Résultats DKIM dans les en-têtes email

Dans `Authentication-Results` :

```
Authentication-Results: mx.google.com;
       dkim=pass header.d=example.com header.s=20230601 header.b=AbCdEfGh
```

| Résultat | Signification |
|----------|---------------|
| `pass` | Signature valide — email intègre et provenant du domaine |
| `fail` | Signature invalide (email modifié en transit ou fausse clé) |
| `none` | Pas de signature DKIM dans l'email |
| `policy` | La politique DKIM du domaine interdit la signature |
| `neutral` | Le message est signé mais la signature ne confirme rien |
| `temperror` | Erreur DNS temporaire lors de la récupération de la clé |
| `permerror` | Erreur permanente (sélecteur inexistant, clé malformée) |

---

## Limites de DKIM

1. **DKIM ne protège pas le From: contre le spoofing** : Un attaquant peut envoyer un email avec une signature DKIM valide depuis `attacker.com`, mais afficher `From: support@votre-banque.fr`. DKIM passe, mais l'email est frauduleux. → DMARC est nécessaire pour l'alignement.

2. **DKIM survit au forwarding** : Contrairement à SPF, DKIM résiste à la redirection d'email (le hash signé voyage avec le message).

3. **Rotation des clés** : Les clés DKIM doivent être régulièrement changées. Une clé compromise permettrait de signer des emails frauduleux.

---

## Outils de vérification

- **MXToolbox DKIM Lookup** : https://mxtoolbox.com/dkim.aspx
- **dmarcian DKIM Inspector** : https://dmarcian.com/dkim-inspector/
- **En ligne de commande** :
  ```bash
  dig TXT <selector>._domainkey.<domain>
  # Exemple :
  dig TXT 20230601._domainkey.gmail.com
  ```
