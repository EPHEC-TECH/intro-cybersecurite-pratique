# MXToolbox — Documentation des outils

**URL** : https://mxtoolbox.com
**Source** : mxtoolbox.com (documentation officielle + interface)

---

## Présentation

MXToolbox est une suite d'outils en ligne gratuits pour diagnostiquer, vérifier et monitorer la sécurité et la délivrabilité des emails. C'est l'outil de référence pour analyser les enregistrements DNS email et les headers.

---

## Outils disponibles

### 🔍 Email Header Analyzer
**URL** : https://mxtoolbox.com/EmailHeaders.aspx

L'outil phare pour l'analyse forensique d'emails.

**Fonctionnement** :
1. Copier-coller le bloc d'en-têtes complet dans le champ "Paste Header"
2. Cliquer sur "Analyze Header"

**Ce que l'outil analyse** :
- **Routage** : chemin complet de l'email avec délais entre chaque hop (serveur à serveur)
- **Anti-spam** : vérification de chaque domaine et IP contre les blacklists
- **Authentification** : résultats SPF, DKIM, DMARC mis en évidence
- **Blacklists** : colonne indiquant si chaque domaine est sur une liste noire
- **Timing** : délais anormaux entre serveurs (peut indiquer une interception)

---

### 📋 MX Lookup
**URL** : https://mxtoolbox.com/MXLookup.aspx
**Syntaxe SuperTool** : `mx:domaine.com`

Interroge les serveurs de noms autoritaires pour lister les enregistrements MX (Mail Exchange) d'un domaine avec leur priorité.

**Résultat type** :
```
Hostname                    Priority   IP Address       TTL
mail.example.com            10         203.0.113.10     3600
mail2.example.com           20         198.51.100.20    3600
```

---

### ✅ SPF Record Check
**URL** : https://mxtoolbox.com/spf.aspx
**Syntaxe SuperTool** : `spf:domaine.com`

- Valide la syntaxe de l'enregistrement SPF
- Vérifie le respect de la limite de 10 DNS lookups
- Identifie les erreurs (`permerror`, mécanismes mal formés)
- Affiche le SPF déployé résolu

---

### 🔑 DKIM Lookup
**URL** : https://mxtoolbox.com/dkim.aspx
**Syntaxe SuperTool** : `dkim:domaine.com:selecteur`

- Récupère et affiche la clé publique DKIM depuis le DNS
- Vérifie la validité de l'enregistrement
- Nécessite de connaître le **sélecteur** (tag `s=` du header DKIM-Signature)

**Exemple** : `dkim:gmail.com:20230601`

---

### 📊 DMARC Check
**URL** : https://mxtoolbox.com/dmarc.aspx
**Syntaxe SuperTool** : `dmarc:domaine.com`

- Parse l'enregistrement DMARC de `_dmarc.domaine.com`
- Identifie la politique (`p=`), les adresses de rapport (`rua=`, `ruf=`)
- Vérifie les erreurs de configuration
- Indique si la protection est active

---

### 🚫 Blacklist Check
**URL** : https://mxtoolbox.com/blacklists.aspx
**Syntaxe SuperTool** : `blacklist:IP_ou_domaine`

- Teste une adresse IP ou un domaine contre **plus de 100 listes noires DNS** (DNS-based Email Blacklists)
- Blacklists couvertes : Spamhaus ZEN, SpamCop, Barracuda, et nombreuses RBSL (domain blocklists)
- Indique sur quelles listes l'IP/domaine est répertorié

---

### 🔎 SuperTool (Multi-lookup)
**URL** : https://mxtoolbox.com/SuperTool.aspx

Interface unifiée qui regroupe tous les lookups. Syntaxe : `type:valeur`

| Commande | Description |
|----------|-------------|
| `mx:example.com` | Enregistrements MX |
| `spf:example.com` | Enregistrement SPF |
| `dkim:example.com:selector` | Clé publique DKIM |
| `dmarc:example.com` | Politique DMARC |
| `blacklist:203.0.113.10` | Vérification blacklists |
| `a:example.com` | Enregistrement A (IP) |
| `txt:example.com` | Tous les enregistrements TXT |
| `smtp:mail.example.com` | Diagnostic SMTP |
| `ptr:203.0.113.10` | Reverse DNS (PTR) |
| `whois:example.com` | Informations WHOIS |

---

### 📧 SMTP Diagnostics
**Syntaxe SuperTool** : `smtp:mail.example.com`

- Se connecte au serveur SMTP
- Vérifie la connectivité et la disponibilité
- Teste la présence d'un reverse DNS
- Détecte les relais ouverts (open relay)

---

## BIMI (bonus)

MXToolbox supporte aussi la vérification **BIMI** (Brand Indicators for Message Identification) — le standard qui permet d'afficher le logo de l'entreprise dans les clients email certifiés.

**Syntaxe** : `bimi:example.com`

---

## Outils complémentaires pour l'analyse d'en-têtes

| Outil | URL | Spécialité |
|-------|-----|-----------|
| **MXToolbox Header Analyzer** | https://mxtoolbox.com/EmailHeaders.aspx | Analyse complète + blacklists |
| **Google Message Header Analyzer** | https://toolbox.googleapps.com/apps/messageheader/ | Visualisation du routage et délais |
| **Microsoft Message Header Analyzer** | https://mha.azurewebsites.net/ | Spécialisé Microsoft 365 |
| **Mail Header Analysis (mxtoolbox)** | https://mxtoolbox.com/EmailHeaders.aspx | Standard industrie |
| **learndmarc.com** | https://www.learndmarc.com/ | Outil pédagogique interactif SPF/DKIM/DMARC |

---

## Cas d'usage typiques

**Pour vérifier la légitimité d'un email reçu :**
1. Afficher les en-têtes complets dans le client email
2. Copier le bloc entier dans https://mxtoolbox.com/EmailHeaders.aspx
3. Analyser : SPF pass ? DKIM pass ? DMARC pass ? IP sur blacklist ?

**Pour vérifier un domaine suspect :**
1. `mx:domaine-suspect.com` → Le domaine a-t-il des serveurs mail configurés ?
2. `spf:domaine-suspect.com` → Quelle est sa politique SPF ?
3. `dmarc:domaine-suspect.com` → A-t-il un DMARC actif ?
4. `blacklist:IP-du-serveur` → L'IP est-elle connue pour du spam ?
