# DMARC (Domain-based Message Authentication, Reporting, and Conformance)

**Sources** : Proofpoint Threat Reference, dmarcian.com, learndmarc.com, RFC 7489
**RFC officielle** : https://datatracker.ietf.org/doc/html/rfc7489

---

## Définition

DMARC est un protocole d'authentification email qui s'appuie sur SPF et DKIM pour permettre aux propriétaires de domaines de :
1. **Déclarer une politique** : que faire si SPF/DKIM échouent ?
2. **Recevoir des rapports** : savoir qui envoie des emails depuis leur domaine
3. **Forcer l'alignement** : lier les résultats SPF/DKIM au domaine visible dans le `From:`

DMARC résout la faille principale de SPF et DKIM : ni l'un ni l'autre ne vérifient le champ `From:` visible par l'utilisateur.

---

## Comment DMARC fonctionne

```
[Email reçu]
      │
      ├─► SPF vérifié ?   (Return-Path domain ↔ SPF record)
      │        │
      └─► DKIM vérifié ?  (DKIM-Signature domain ↔ clé publique DNS)
               │
               ▼
   DMARC vérifie l'ALIGNEMENT :
   ┌─────────────────────────────────────────────────────┐
   │ SPF aligned : smtp.mailfrom domain = From: domain   │
   │ DKIM aligned : d= tag domain = From: domain         │
   └─────────────────────────────────────────────────────┘
               │
   Au moins 1 des deux est aligned ET pass ?
      │
      ├─► OUI → DMARC pass ✓
      │
      └─► NON → DMARC fail → Appliquer la politique (p=)
                    ├─► p=none     → Ne rien faire (monitoring)
                    ├─► p=quarantine → Mettre en spam
                    └─► p=reject   → Rejeter l'email
```

---

## Alignement SPF et DKIM

L'alignement est le concept central de DMARC :

**SPF alignment** : le domaine du `MAIL FROM` (Return-Path) doit correspondre au domaine du `From:` header.
- Alignement relaxed : les sous-domaines sont acceptés (ex: `mail.example.com` aligne avec `example.com`)
- Alignement strict : les domaines doivent être identiques

**DKIM alignment** : le domaine dans le tag `d=` de la signature DKIM doit correspondre au domaine du `From:` header.

**Exemple de réussite DMARC** :
```
From: alice@example.com
Return-Path: bounce@example.com   ← même domaine root → SPF aligned
DKIM-Signature: d=example.com    ← même domaine → DKIM aligned
```

**Exemple d'échec DMARC (spoofing) :**
```
From: support@bnp-paribas.fr     ← domaine visible de la banque
Return-Path: attacker@evil.com   ← SPF pass sur evil.com, mais PAS aligné
DKIM-Signature: d=evil.com       ← DKIM pass sur evil.com, mais PAS aligné
→ DMARC fail
```

---

## Structure d'un enregistrement DMARC

L'enregistrement DMARC est un TXT DNS publié à `_dmarc.<domaine>` :

```
_dmarc.example.com   IN   TXT   "v=DMARC1; p=reject; rua=mailto:dmarc@example.com; ruf=mailto:forensic@example.com; adkim=r; aspf=r; pct=100"
```

### Tags DMARC

| Tag | Requis | Description | Valeurs |
|-----|--------|-------------|---------|
| `v=` | Oui | Version DMARC | Toujours `DMARC1` |
| `p=` | Oui | Politique pour les emails du domaine racine | `none`, `quarantine`, `reject` |
| `sp=` | Non | Politique pour les sous-domaines | `none`, `quarantine`, `reject` |
| `rua=` | Non | URI pour les rapports agrégés (quotidiens) | `mailto:dmarc@example.com` |
| `ruf=` | Non | URI pour les rapports forensiques (par email échoué) | `mailto:forensic@example.com` |
| `adkim=` | Non | Alignement DKIM | `r` (relaxed, défaut) ou `s` (strict) |
| `aspf=` | Non | Alignement SPF | `r` (relaxed, défaut) ou `s` (strict) |
| `pct=` | Non | % des emails soumis à la politique | `0`-`100` (défaut: 100) |
| `fo=` | Non | Options de rapport forensique | `0`, `1`, `d`, `s` |
| `ri=` | Non | Intervalle de rapport agrégé en secondes | `86400` (défaut: 24h) |

---

## Les trois politiques DMARC

### `p=none` — Mode monitoring
```
"v=DMARC1; p=none; rua=mailto:dmarc@example.com"
```
- Aucune action sur les emails qui échouent DMARC
- Permet de recevoir des rapports sans risquer de bloquer des emails légitimes
- **Utilisé en phase de déploiement initial**

### `p=quarantine` — Mode quarantaine
```
"v=DMARC1; p=quarantine; pct=50; rua=mailto:dmarc@example.com"
```
- Les emails qui échouent DMARC vont dans le dossier spam/junk
- `pct=50` : seulement 50% des emails concernés (déploiement progressif)
- **Transition vers la protection complète**

### `p=reject` — Mode rejet
```
"v=DMARC1; p=reject; rua=mailto:dmarc@example.com"
```
- Les emails qui échouent DMARC sont rejetés (retournés à l'expéditeur)
- **Protection maximale contre le spoofing**
- À utiliser quand on est certain que tous les serveurs légitimes sont configurés

---

## Exemples d'enregistrements DMARC réels

**Gmail / Google Workspace (domaine personnel) :**
```
v=DMARC1; p=none; rua=mailto:mailauth-reports@google.com
```

**Microsoft :**
```
v=DMARC1; p=reject; pct=100; rua=mailto:d@rua.agari.com
```

**Exemple minimal de départ (monitoring) :**
```
v=DMARC1; p=none; rua=mailto:dmarc-rapports@mondomaine.fr
```

**Protection totale :**
```
v=DMARC1; p=reject; sp=reject; adkim=s; aspf=s; rua=mailto:dmarc@mondomaine.fr; ruf=mailto:forensic@mondomaine.fr; pct=100
```

---

## Résultats DMARC dans les en-têtes email

Dans `Authentication-Results` :

```
Authentication-Results: mx.google.com;
       dmarc=fail (p=REJECT sp=REJECT dis=REJECT) header.from=bnp-paribas.fr
```

Syntaxe complète :
```
dmarc=<pass|fail|bestguesspass|none> action=<permerror|temperror|oreject|pct.quarantine|pct.reject> header.from=<domain>
```

Exemples :
```
dmarc=pass action=none header.from=example.com
dmarc=fail action=quarantine header.from=usurped-domain.com
dmarc=fail action=oreject header.from=bank.com
```

---

## Déploiement progressif recommandé

```
Étape 1 : p=none    → Collecter des rapports, identifier tous les flux légitimes
Étape 2 : p=quarantine; pct=10  → Commencer à filtrer 10% des emails suspects
Étape 3 : p=quarantine; pct=100 → Filtrer tous les emails suspects
Étape 4 : p=reject             → Protection maximale
```

---

## Ressource pédagogique interactive

**LearnDMARC** : https://www.learndmarc.com/
→ Simulateur visuel qui montre comment SPF, DKIM et DMARC interagissent sur de vrais emails

---

## Outils de vérification

- **MXToolbox DMARC Check** : https://mxtoolbox.com/dmarc.aspx
- **dmarcian DMARC Inspector** : https://dmarcian.com/dmarc-inspector/
- **En ligne de commande** :
  ```bash
  dig TXT _dmarc.example.com
  # Exemple :
  dig TXT _dmarc.gmail.com
  ```
