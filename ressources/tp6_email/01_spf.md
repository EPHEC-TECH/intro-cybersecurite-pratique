# SPF (Sender Policy Framework)

**Sources** : Proofpoint Threat Reference, dmarcian.com, RFC 7208
**RFC officielle** : https://datatracker.ietf.org/doc/html/rfc7208

---

## Définition

SPF est un protocole d'authentification email qui permet aux propriétaires de domaines de spécifier quels serveurs mail sont autorisés à envoyer des emails en leur nom. Cette information est publiée dans un **enregistrement DNS TXT**.

Quand un serveur récepteur reçoit un email, il consulte l'enregistrement SPF du domaine expéditeur (extrait du champ `Return-Path` / `MAIL FROM`) et vérifie si l'adresse IP du serveur émetteur est dans la liste autorisée.

---

## Comment SPF fonctionne

```
[Serveur A envoie un email depuis IP 203.0.113.10]
           │
           ▼
[Serveur destinataire reçoit l'email]
           │
           ▼
[Consulte le DNS : quel est l'enregistrement SPF de l'expéditeur ?]
  → TXT record de example.com : "v=spf1 ip4:203.0.113.10 ~all"
           │
           ▼
[Comparaison : IP 203.0.113.10 est-elle autorisée ?]
  → OUI → SPF pass ✓
  → NON → SPF fail ✗
```

**Point critique** : SPF vérifie le domaine du `Return-Path` (l'enveloppe SMTP, champ technique `MAIL FROM`), **pas** le champ `From:` visible dans le client email. C'est pourquoi SPF seul ne protège pas contre le spoofing de l'adresse affichée — c'est le rôle de DMARC.

---

## Syntaxe d'un enregistrement SPF

Un enregistrement SPF est un enregistrement DNS TXT qui commence toujours par `v=spf1` :

```
v=spf1 [mécanismes] [qualificateur]all
```

### Mécanismes

| Mécanisme | Description | Exemple |
|-----------|-------------|---------|
| `all` | Catch-all : correspond à toutes les IP non matchées (toujours en dernier) | `-all` |
| `a` | L'adresse IP de l'enregistrement A du domaine | `a` ou `a:mail.example.com` |
| `mx` | Les serveurs MX du domaine | `mx` |
| `ip4` | Une adresse IPv4 ou plage CIDR | `ip4:203.0.113.10` ou `ip4:203.0.113.0/24` |
| `ip6` | Une adresse IPv6 ou plage CIDR | `ip6:2001:db8::1` |
| `include` | Inclut et évalue le SPF d'un autre domaine | `include:_spf.google.com` |
| `redirect` | Délègue entièrement la politique à un autre domaine | `redirect=_spf.example.com` |
| `exists` | Vérifie l'existence d'un enregistrement A construit dynamiquement | `exists:%{i}._spf.example.com` |
| `ptr` | Vérifie le reverse DNS — **déconseillé** (lent, peu fiable) | `ptr:example.com` |

### Qualificateurs

Les qualificateurs précèdent les mécanismes et définissent l'action si le mécanisme correspond :

| Qualificateur | Résultat | Signification |
|---------------|----------|---------------|
| `+` (défaut, implicite) | **Pass** | L'expéditeur est autorisé |
| `-` | **Fail** (hard fail) | L'expéditeur est rejeté — le serveur doit refuser l'email |
| `~` | **Softfail** | L'expéditeur est suspect — accepter mais marquer comme spam |
| `?` | **Neutral** | Pas de politique définie |

---

## Exemples d'enregistrements SPF réels

**Simple — une seule IP autorisée, rejet strict :**
```
v=spf1 ip4:203.0.113.10 -all
```

**Autoriser les serveurs MX du domaine :**
```
v=spf1 mx -all
```

**Autoriser Google Workspace :**
```
v=spf1 include:_spf.google.com ~all
```

**Autoriser Microsoft 365 :**
```
v=spf1 include:spf.protection.outlook.com ~all
```

**Enregistrement combiné (plusieurs prestataires) :**
```
v=spf1 ip4:203.0.113.10 ip4:198.51.100.0/24 include:_spf.google.com include:sendgrid.net ~all
```

**Domaine qui n'envoie jamais d'email (protection maximale) :**
```
v=spf1 -all
```

**Enregistrement réel de google.com :**
```
v=spf1 include:_spf.google.com ~all
```
(Le domaine google.com délègue entièrement à `_spf.google.com`)

---

## Résultats SPF dans les en-têtes email

Dans le header `Authentication-Results`, le résultat SPF apparaît comme :

```
Authentication-Results: mx.google.com;
       spf=pass (google.com: domain of alice@example.com designates 203.0.113.10
             as permitted sender) smtp.mailfrom=alice@example.com
```

| Résultat | Signification |
|----------|---------------|
| `pass` | IP autorisée — email légitime |
| `fail` | IP non autorisée (hard fail `-all`) |
| `softfail` | IP non autorisée mais domaine clément (`~all`) |
| `neutral` | Domaine sans politique (`?all`) |
| `none` | Pas d'enregistrement SPF trouvé |
| `temperror` | Erreur temporaire (DNS timeout) |
| `permerror` | Erreur permanente (SPF mal formé, > 10 DNS lookups) |

---

## Limites de SPF

1. **Le problème du forwarding** : Quand un email est redirigé (forward), l'IP du redirecteur n'est pas dans le SPF original → SPF échoue sur des emails légitimes redirigés.

2. **Limite de 10 DNS lookups** : Un enregistrement SPF ne peut pas déclencher plus de 10 résolutions DNS cumulées (`include`, `mx`, `a`, `exists`). Au-delà → `permerror` et le SPF échoue.

3. **SPF ne protège pas le From: affiché** : SPF vérifie le `Return-Path` (`MAIL FROM` SMTP), pas le `From:` visible. Un attaquant peut afficher `From: support@bnp.fr` avec un `Return-Path: attacker@evil.com`. DMARC est nécessaire pour fermer cette faille via l'alignement.

---

## Outils de vérification

- **MXToolbox SPF Check** : https://mxtoolbox.com/spf.aspx
- **dmarcian SPF Surveyor** : https://dmarcian.com/spf-survey/
- **En ligne de commande** :
  ```bash
  dig TXT example.com | grep spf
  # ou
  nslookup -type=TXT example.com
  ```
