# Exemple d'en-tête frauduleux — Phishing BNP Paribas (SPF fail + DMARC fail)

**Scénario** : Un attaquant envoie un email de phishing en usurpant l'identité de BNP Paribas pour voler les identifiants bancaires d'une victime. Il utilise un faux serveur mail qui n'est pas autorisé par le SPF de bnpparibas.fr.

---

## En-tête brut

```
Delivered-To: victim@gmail.com
Received: by 2002:a17:906:4cd6:b0:a91:7c82:9e5f with SMTP id x22csp789012qvw;
        Mon, 16 Mar 2026 02:14:33 -0700 (PDT)
Received: from mail.evil-host.ru (mail.evil-host.ru. [185.220.101.47])
        by mx.google.com with ESMTP id a1si2345678qkm.2026.03.16.02.14.32
        for <victim@gmail.com>;
        Mon, 16 Mar 2026 02:14:32 -0700 (PDT)
Received-SPF: fail (google.com: domain of support@bnpparibas.fr does NOT
        designate 185.220.101.47 as permitted sender)
        client-ip=185.220.101.47;
Authentication-Results: mx.google.com;
       spf=fail (google.com: domain of support@bnpparibas.fr does NOT designate
             185.220.101.47 as permitted sender) smtp.mailfrom=support@bnpparibas.fr;
       dkim=none;
       dmarc=fail (p=REJECT sp=REJECT dis=REJECT) header.from=bnpparibas.fr
Return-Path: <support@bnpparibas.fr>
From: "BNP Paribas Sécurité" <support@bnpparibas.fr>
To: victim@gmail.com
Subject: [URGENT] Votre compte a été suspendu - Action requise
Date: Mon, 16 Mar 2026 02:14:29 -0700
Message-ID: <20260316021429.1234567@evil-host.ru>
MIME-Version: 1.0
X-PHP-Originating-Script: 1000:mailer.php
X-Mailer: PHPMailer 6.6.5 (https://github.com/PHPMailer/PHPMailer)
Content-Type: text/html; charset=UTF-8
Content-Transfer-Encoding: quoted-printable
```

---

## Analyse : les signaux d'alerte

### 1. SPF = FAIL ❌

```
spf=fail (google.com: domain of support@bnpparibas.fr does NOT designate
      185.220.101.47 as permitted sender)
```

**Explication** : L'IP `185.220.101.47` **n'est pas** dans l'enregistrement SPF du domaine `bnpparibas.fr`. Le vrai SPF de BNP Paribas autorise uniquement les serveurs de BNP — et non un serveur hébergé en Russie (`evil-host.ru`).

→ **Un serveur légitime de BNP Paribas aurait SPF=pass.**

---

### 2. DKIM = NONE ❌

```
dkim=none
```

**Explication** : Aucune signature DKIM n'est présente dans cet email. BNP Paribas signe tous ses emails sortants avec DKIM. L'absence de signature signifie que cet email ne provient pas de leur infrastructure.

→ **Un email authentique de BNP Paribas aurait DKIM=pass.**

---

### 3. DMARC = FAIL avec action REJECT ❌

```
dmarc=fail (p=REJECT sp=REJECT dis=REJECT) header.from=bnpparibas.fr
```

**Explication** : BNP Paribas a déployé DMARC avec la politique `p=reject`. L'email échoue l'alignement DMARC car :
- SPF fail → l'enveloppe n'est pas alignée
- DKIM none → pas de signature à aligner

Normalement, cet email devrait être **rejeté** par le serveur Gmail. Certains providers l'acceptent quand même mais le marquent comme suspect.

---

### 4. IP suspecte dans `Received:` ❌

```
Received: from mail.evil-host.ru (mail.evil-host.ru. [185.220.101.47])
```

**Explication** :
- Le serveur source s'appelle `mail.evil-host.ru` — domaine russe sans rapport avec BNP Paribas
- L'IP `185.220.101.47` appartient à un hébergeur connu pour héberger des nœuds Tor et des serveurs utilisés dans des activités malveillantes

---

### 5. Message-ID révélateur ❌

```
Message-ID: <20260316021429.1234567@evil-host.ru>
```

**Explication** : Le Message-ID est généré par le serveur émetteur réel — ici `evil-host.ru`. Un email de BNP Paribas aurait un Message-ID avec un domaine `bnpparibas.fr` ou un prestataire email légitime.

---

### 6. X-PHP-Originating-Script ❌

```
X-PHP-Originating-Script: 1000:mailer.php
X-Mailer: PHPMailer 6.6.5
```

**Explication** : Cet email a été envoyé par un **script PHP** (`mailer.php`) tournant sur un serveur web compromis ou loué par l'attaquant. Les vrais emails d'une grande banque ne sont pas envoyés par des scripts PHP. Ce header est caractéristique des outils de phishing.

---

### 7. Envoi nocturne depuis un timezone suspect ❌

```
Date: Mon, 16 Mar 2026 02:14:29 -0700
```

**Explication** : L'email est envoyé à 2h14 du matin (heure du Pacifique) — ou 9h14 UTC. BNP Paribas est une banque française (UTC+1). Un email de leur système de sécurité arriverait en heures ouvrables françaises, pas à 2h du matin.

---

## Tableau récapitulatif

| Signal | Valeur | Status | Signification |
|--------|--------|--------|---------------|
| `spf=` | `fail` | ❌ | IP non autorisée par BNP Paribas |
| `dkim=` | `none` | ❌ | Aucune signature — pas envoyé par BNP |
| `dmarc=` | `fail` | ❌ | Désalignement complet |
| IP source | `185.220.101.47` | ❌ | Serveur russe, pas BNP |
| `Return-Path` | `@bnpparibas.fr` | ⚠️ | Usurpé — ne correspond pas à l'IP |
| `Message-ID` | `@evil-host.ru` | ❌ | Révèle le vrai serveur expéditeur |
| `X-PHP-Originating-Script` | `mailer.php` | ❌ | Script PHP = phishing tool |
| `X-Mailer` | `PHPMailer` | ❌ | Outil non utilisé par les banques |
| Objet | `[URGENT]` + suspension | ⚠️ | Technique d'urgence classique du phishing |

---

## Contexte : comment se protéger

BNP Paribas (comme toutes les grandes banques) a normalement `p=reject` dans son DMARC. Cela signifie que les serveurs de messagerie **bien configurés** devraient automatiquement rejeter cet email. Si la victime le reçoit quand même, soit son fournisseur email est mal configuré, soit l'email a contourné les filtres via une autre technique.
