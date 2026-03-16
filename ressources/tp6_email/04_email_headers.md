# Guide des En-têtes Email (Email Headers)

**Sources** : mailtrap.io, Microsoft Learn, RFC 5322, RFC 7001

---

## Qu'est-ce qu'un en-tête email ?

Quand un email est envoyé, chaque serveur qui le traite ajoute des **métadonnées techniques** invisibles par défaut dans le client email. Ces métadonnées — les en-têtes — contiennent :
- Le chemin complet parcouru par l'email (tous les serveurs traversés)
- Les résultats d'authentification (SPF, DKIM, DMARC)
- Les scores anti-spam
- L'IP d'origine réelle de l'expéditeur
- Les timestamps de chaque étape

Les en-têtes sont la **boîte noire de l'email** : ils ne mentent pas (enfin, moins facilement que les champs visibles).

---

## Comment afficher les en-têtes complets

### Gmail
1. Ouvrir l'email
2. Menu ⋮ (3 points) → **"Afficher l'original"** (Show Original)
3. Ou directement : `Ctrl+U`

### Outlook / Microsoft 365
1. Ouvrir l'email
2. Menu ⋯ → **Affichage** → **Afficher la source du message**
3. Ou : Fichier → Propriétés → **En-têtes Internet**

### Apple Mail
1. Affichage → Message → **Tous les en-têtes**

### Yahoo Mail
1. Menu ⋮ (3 points) → **"Voir le message brut"** (View Raw Message)

### Thunderbird
1. Affichage → En-têtes → **Tous**

---

## Les en-têtes importants et leur signification

### En-têtes d'identification

| Header | Description | Exemple |
|--------|-------------|---------|
| `From:` | Adresse de l'expéditeur **visible** (peut être falsifiée) | `From: Alice <alice@example.com>` |
| `To:` | Destinataires principaux | `To: bob@example.com` |
| `Cc:` | Copie carbone (visible par tous) | `Cc: carol@example.com` |
| `Subject:` | Objet de l'email | `Subject: Réunion demain` |
| `Date:` | Date d'envoi selon l'expéditeur (peut être falsifiée) | `Date: Mon, 16 Mar 2026 09:00:00 +0100` |
| `Message-ID:` | Identifiant unique de l'email, généré par le serveur expéditeur | `Message-ID: <abc123@mail.example.com>` |

### En-têtes d'enveloppe SMTP (les vrais)

| Header | Description | Importance |
|--------|-------------|-----------|
| `Return-Path:` | Adresse réelle de l'enveloppe SMTP (`MAIL FROM`). C'est cette adresse que vérifie SPF. Les bounces y sont envoyés. | ⚠️ Critique |
| `Reply-To:` | Adresse de réponse — si différente du `From:`, c'est souvent suspect dans un contexte de phishing | ⚠️ Suspect si ≠ From |
| `Delivered-To:` | Adresse finale du destinataire (après expansion des alias) | Info |

### En-têtes de routage — la chaîne `Received:`

C'est la piste d'audit de l'email. **Chaque serveur traversé ajoute un header `Received:` en haut de la pile.**

**Lecture** : lire de bas en haut = ordre chronologique (le premier hop est en bas).

```
Received: from mail.exemple.com (mail.exemple.com [203.0.113.10])
        by mx.google.com with ESMTPS id abc123
        for <bob@gmail.com>;
        Mon, 16 Mar 2026 09:00:05 +0000

Received: from pc-alice.local ([192.168.1.42])
        by mail.exemple.com with ESMTP id xyz789;
        Mon, 16 Mar 2026 09:00:01 +0100
```

Structure d'un `Received:` :
- `from [serveur source]` : qui envoie
- `by [serveur destination]` : qui reçoit
- `with [protocole]` : comment (SMTP, ESMTP, ESMTPS...)
- `id [identifiant]` : identifiant de transaction
- `for <destinataire>` : pour qui
- timestamp : quand

### En-têtes d'authentification

| Header | Description |
|--------|-------------|
| `Authentication-Results:` | Résultats des vérifications SPF, DKIM, DMARC effectuées par le serveur récepteur |
| `DKIM-Signature:` | La signature cryptographique DKIM ajoutée par le serveur expéditeur |
| `Received-SPF:` | Résultat du check SPF (format alternatif, parfois présent) |
| `ARC-Authentication-Results:` | Résultats ARC (Authenticated Received Chain) pour les emails redirigés |

**Exemple d'Authentication-Results complet (Gmail) :**
```
Authentication-Results: mx.google.com;
       dkim=pass header.d=example.com header.s=20230601 header.b=AbCdEfGh;
       spf=pass (google.com: domain of alice@example.com designates 203.0.113.10
             as permitted sender) smtp.mailfrom=alice@example.com;
       dmarc=pass (p=REJECT sp=REJECT dis=NONE) header.from=example.com
```

### En-têtes anti-spam

| Header | Description |
|--------|-------------|
| `X-Spam-Score:` | Score anti-spam (ex: SpamAssassin — plus le score est élevé, plus c'est suspect) |
| `X-Spam-Status:` | Résultat du filtre spam (`Yes`/`No`) |
| `X-Spam-Flag:` | Marqueur spam (`YES`/`NO`) |
| `X-Originating-IP:` | IP d'origine réelle (ajoutée par certains services comme Yahoo/Hotmail) |

### En-têtes Microsoft 365 / Defender

| Header | Description |
|--------|-------------|
| `X-Forefront-Antispam-Report:` | Rapport anti-spam Defender (SCL, pays source, catégorie menace...) |
| `X-Microsoft-Antispam:` | Informations anti-spam Microsoft (BCL — Bulk Complaint Level) |
| `X-MS-Exchange-Organization-SCL:` | Spam Confidence Level (SCL) de -1 à 9 |

Dans `X-Forefront-Antispam-Report`, les champs clés :
- `SCL:` Score spam (0=légitime, 5-9=spam probable)
- `CAT:` Catégorie (`PHSH`=phishing, `SPOOF`=spoofing, `SPM`=spam, `BULK`=bulk...)
- `CTRY:` Pays source de l'IP
- `CIP:` IP connectante

### En-têtes de format

| Header | Description |
|--------|-------------|
| `MIME-Version:` | Version MIME (normalement `1.0`) |
| `Content-Type:` | Format du corps (`text/plain`, `text/html`, `multipart/mixed`...) |
| `Content-Transfer-Encoding:` | Encodage (`base64`, `quoted-printable`, `7bit`) |

---

## Signaux suspects dans les en-têtes

Lors de l'analyse d'un email potentiellement frauduleux, chercher :

| Signal | Ce que ça indique |
|--------|-------------------|
| `spf=fail` ou `spf=softfail` | L'IP expéditrice n'est pas autorisée par le domaine affiché |
| `dkim=none` ou `dkim=fail` | Pas de signature ou signature invalide |
| `dmarc=fail` | Le domaine `From:` n'est pas aligné avec SPF/DKIM |
| `Reply-To:` ≠ `From:` | Réponses détournées vers une adresse de l'attaquant |
| `Return-Path:` domaine ≠ `From:` domaine | L'enveloppe SMTP révèle le vrai expéditeur |
| IP dans `Received:` géographiquement incohérente | Expédition depuis un pays suspect pour le domaine prétendu |
| `Message-ID:` avec domaine ≠ `From:` | Généré par un serveur différent du domaine prétendu |
| `X-Mailer:` ou `X-PHP-Originating-Script:` | Révèle un script PHP (emkei.cz, fake mailers...) |
| `X-Originating-IP:` suspect | IP résidentielle ou d'un VPN/proxy |
| Timestamp `Date:` incohérent | Date antérieure ou future anormalement |

---

## Outil d'analyse recommandé

**MXToolbox Email Header Analyzer** : https://mxtoolbox.com/EmailHeaders.aspx

Cet outil :
- Parse les headers selon RFC 822
- Affiche le chemin de routage avec les délais entre serveurs
- Vérifie chaque domaine contre les blacklists
- Met en évidence les résultats SPF/DKIM/DMARC
- Identifie les anomalies de timing

**Utilisation** : copier-coller le bloc d'en-têtes brut dans le champ "Paste Header".
