# Exercices et Ressources pédagogiques — Sécurité Email

---

## Outils d'analyse en ligne

| Outil | URL | Usage |
|-------|-----|-------|
| **MXToolbox Email Header Analyzer** | https://mxtoolbox.com/EmailHeaders.aspx | Analyse complète + blacklists (⭐ outil principal du TP) |
| **MXToolbox SuperTool** | https://mxtoolbox.com/SuperTool.aspx | MX, SPF, DKIM, DMARC, Blacklist lookups |
| **Google Apps Toolbox** | https://toolbox.googleapps.com/apps/messageheader/ | Visualisation du routage, délais entre serveurs |
| **Microsoft Message Header Analyzer** | https://mha.azurewebsites.net/ | Spécialisé Microsoft 365 / Exchange |
| **LearnDMARC (simulateur interactif)** | https://www.learndmarc.com/ | Outil pédagogique : envoie un email réel et analyse SPF/DKIM/DMARC en temps réel |
| **Mail Header Analysis** | https://mailheader.org/ | Analyse simple et lisible |

---

## Challenges et exercices en ligne

### TryHackMe — Phishing Emails Series
**URL** : https://tryhackme.com/room/phishingemails1

Série de 5 rooms dédiées à l'analyse de phishing :
- **Phishing Emails 1** : Introduction à l'analyse d'emails phishing, anatomie d'un email suspect
- **Phishing Emails 2** : Défenses email (SPF, DKIM, DMARC) et outils d'analyse
- **Phishing Emails 3** : Analyse de pièces jointes malveillantes
- **Phishing Emails 4** : Analyse d'en-têtes email, MXToolbox, identifier l'infrastructure d'attaque
- **Phishing Emails 5** : Email phishing dans un contexte de SOC

**Niveau** : Débutant à intermédiaire
**Compétences** : Analyse headers, SPF/DKIM/DMARC, outils OSINT email

---

### Hack The Box — "Easy Phish"
**Difficulté** : Very Easy
**Catégorie** : OSINT / Forensics

**Synopsis** : Étant donné un domaine, trouver pourquoi les emails d'une organisation échouent les contrôles de sécurité. Nécessite d'interroger les enregistrements DNS pour trouver les enregistrements SPF et DMARC manquants ou mal configurés, et construire la réponse (flag) à partir des découvertes.

**Compétences** : DNS lookups, analyse SPF/DMARC, MXToolbox

---

### Metaspike CTF — Email Forensics
**URL** : https://ctf.metaspike.com/

CTF spécialisé en forensique email. Exercices autour de :
- Analyse d'en-têtes pour identifier l'expéditeur réel
- Détection d'anomalies temporelles (X-Mailer anachronique)
- Reconstruction de la chaîne de routage
- Identification des métadonnées révélatrices

**Exemple de défi** : Un email prétend avoir été envoyé en 2016 avec Chrome 87 dans le X-Mailer, mais Chrome 87 n'existait pas en 2016 → l'email est une fabrication ultérieure.

---

### PhishTool
**URL** : https://app.phishtool.com/

Plateforme d'analyse de phishing avec :
- Upload d'emails `.eml` pour analyse automatique
- Extraction des indicateurs de compromission (URLs, IPs, domaines)
- Vérification blacklists
- Version gratuite disponible

---

## Ressources de documentation de référence

### RFC officielles
| RFC | Sujet | URL |
|-----|-------|-----|
| RFC 5321 | SMTP (Simple Mail Transfer Protocol) | https://datatracker.ietf.org/doc/html/rfc5321 |
| RFC 5322 | Format des messages Internet (en-têtes) | https://datatracker.ietf.org/doc/html/rfc5322 |
| RFC 7208 | SPF (Sender Policy Framework) | https://datatracker.ietf.org/doc/html/rfc7208 |
| RFC 6376 | DKIM (DomainKeys Identified Mail) | https://datatracker.ietf.org/doc/html/rfc6376 |
| RFC 7489 | DMARC | https://datatracker.ietf.org/doc/html/rfc7489 |
| RFC 7001 | Authentication-Results header | https://datatracker.ietf.org/doc/html/rfc7001 |

### Documentation technique
| Ressource | URL | Contenu |
|-----------|-----|---------|
| dmarcian | https://dmarcian.com | Guides SPF, DKIM, DMARC, outils gratuits |
| Proofpoint Threat Reference | https://www.proofpoint.com/us/threat-reference | Définitions techniques |
| Microsoft Learn — Anti-spam headers | https://learn.microsoft.com/en-us/defender-office-365/message-headers-eop-mdo | Headers Microsoft 365 complets |
| MXToolbox Learn | https://mxtoolbox.com/learn/ | Tutoriels et guides |

---

## Idées d'exercices pratiques pour le TP

### Exercice A — Analyse MX Record
1. Choisir un domaine connu (ex: `ephec.be`, `gmail.com`)
2. Utiliser MXToolbox → MX Lookup
3. Identifier les serveurs MX et leur priorité
4. **Question** : Quel domaine gère les emails de `ephec.be` ?

### Exercice B — Vérification SPF
1. Choisir plusieurs domaines (legitime et suspect)
2. MXToolbox → SPF Check
3. Comparer les politiques (`-all` vs `~all` vs pas de SPF)
4. **Question** : Quel domaine accepterait qu'un email frauduleux passe le SPF ?

### Exercice C — Analyse d'en-têtes (MXToolbox)
1. Fournir un bloc d'en-têtes (légitime ou frauduleux)
2. Coller dans https://mxtoolbox.com/EmailHeaders.aspx
3. Identifier : SPF pass/fail ? DKIM pass/fail ? DMARC pass/fail ? IP sur blacklist ?

### Exercice D — Détection de phishing
1. Fournir plusieurs en-têtes (mélange legitimes/frauduleux)
2. L'étudiant doit identifier lequel est frauduleux et justifier par les indicateurs

### Exercice E — Vérification DMARC d'un domaine connu
1. MXToolbox → DMARC Check sur plusieurs domaines
2. Comparer les politiques déployées
3. **Question** : Parmi `gmail.com`, `free.fr`, `ephec.be` — lequel a la protection la plus forte ?

---

## Anatomie d'une campagne de phishing — Vue d'ensemble

```
ATTAQUANT
   │
   ├── Choisit un domaine cible à usurper (ex: votre-banque.fr)
   │
   ├── Enregistre un domaine similaire (ex: v0tre-banque.fr) OU
   │   utilise un faux mailer (emkei.cz, PHPMailer sur serveur compromis)
   │
   ├── Envoie l'email avec :
   │      From: support@votre-banque.fr    ← falsifié (visible)
   │      Return-Path: @v0tre-banque.fr    ← réel (enveloppe)
   │      Reply-To: attacker@protonmail.com ← pour récupérer les réponses
   │
   └── L'email arrive chez la victime :
          - SPF fail (IP non autorisée par votre-banque.fr)
          - DKIM none (pas de signature légitime)
          - DMARC fail → devrait être rejeté

DÉFENSE
   └── DMARC p=reject → rejet automatique
       ou
       Formation utilisateurs → reconnaître les signaux visuels
```
