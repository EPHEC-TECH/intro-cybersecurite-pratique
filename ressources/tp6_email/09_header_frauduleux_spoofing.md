# Exemples d'en-têtes frauduleux — Techniques de spoofing et phishing

Recueil de plusieurs scénarios d'attaque réels ou réalistes, avec analyse des indicateurs de compromission.

---

## Exemple 1 : Phishing PayPal — Typosquatting + absence d'authentification

**Technique** : Le domaine `paypa1.com` (avec un "1" à la place du "l") est utilisé pour imiter PayPal.

```
Received: from mail.paypa1.com (mail.paypa1.com [45.76.135.218])
        by mx.google.com with ESMTP id p1si9876543qkm;
        Sat, 14 Mar 2026 11:32:17 -0700 (PDT)
Received-SPF: none (google.com: paypa1.com does not designate permitted sender hosts)
Authentication-Results: mx.google.com;
       spf=none smtp.mailfrom=no-reply@paypa1.com;
       dkim=none;
       dmarc=none
Return-Path: <no-reply@paypa1.com>
From: "PayPal" <security@paypal.com>
Reply-To: collect-creds@paypa1.com
To: victim@gmail.com
Subject: Your account has been limited - Verify now
Date: Sat, 14 Mar 2026 11:32:12 -0700
Message-ID: <2026031411321234@paypa1.com>
```

### Signaux suspects

| Signal | Explication |
|--------|-------------|
| `From: security@paypal.com` + `Return-Path: @paypa1.com` | **Spoofing visible** : le `From:` affiche `paypal.com` (légitime), mais l'enveloppe révèle `paypa1.com` (frauduleux) |
| `Reply-To: collect-creds@paypa1.com` | Les réponses vont vers l'attaquant |
| `spf=none`, `dkim=none`, `dmarc=none` | Aucune authentification — `paypa1.com` n'a aucun enregistrement de sécurité |
| IP `45.76.135.218` | Appartient à un hébergeur VPS public (Vultr) — pas l'infrastructure PayPal |
| Typosquatting | `paypa1.com` ≠ `paypal.com` : impossible à voir à vitesse de lecture normale |

---

## Exemple 2 : Phishing bancaire — Reply-To piégé (Chase Bank)

**Technique** : L'attaquant envoie depuis une adresse légitime en apparence, mais détourne les réponses.

```
Received: from smtp.legit-looking-domain.com (smtp.legit-looking-domain.com [203.0.113.99])
        by mx.google.com with ESMTP id r2si1234567qkm;
        Fri, 13 Mar 2026 08:15:44 -0800 (PST)
Authentication-Results: mx.google.com;
       spf=pass smtp.mailfrom=alerts@legit-looking-domain.com;
       dkim=pass header.d=legit-looking-domain.com;
       dmarc=pass header.from=legit-looking-domain.com
Return-Path: <alerts@legit-looking-domain.com>
From: "Chase Bank Security" <no-reply@chase.com>
Reply-To: chase-verification@protonmail.com
To: victim@gmail.com
Subject: Suspicious login detected on your account
Date: Fri, 13 Mar 2026 08:15:40 -0800
Message-ID: <20260313081540.9876543@legit-looking-domain.com>
```

### Signaux suspects

| Signal | Explication |
|--------|-------------|
| **SPF/DKIM/DMARC passent** | ⚠️ Ici SPF, DKIM, DMARC passent — mais pour `legit-looking-domain.com`, PAS pour `chase.com` |
| `From: @chase.com` | Affiché comme Chase Bank — mais SPF/DKIM vérifient `legit-looking-domain.com` |
| **Désalignement DMARC** | Le `From:` affiche `chase.com`, mais l'alignement est sur `legit-looking-domain.com` — normalement DMARC devrait fail |
| `Reply-To: @protonmail.com` | Les réponses vont vers un compte ProtonMail de l'attaquant |
| `Message-ID: @legit-looking-domain.com` | Révèle le vrai serveur expéditeur |

> **Note pédagogique** : Cet exemple illustre pourquoi il faut vérifier l'alignement DMARC, pas seulement si SPF et DKIM passent chacun de leur côté.

---

## Exemple 3 : Fake mailer emkei.cz — SPF softfail + DMARC fail

**Technique** : L'attaquant utilise le service `emkei.cz` (faux mailer en ligne, depuis longtemps connu pour le phishing) pour envoyer un email avec n'importe quelle adresse From:.

```
Received: from emkei.cz (emkei.cz [93.99.104.210])
        by mx.google.com with ESMTP id e1si3456789qkm;
        Thu, 12 Mar 2026 15:47:22 -0700 (PDT)
Received-SPF: softfail (google.com: domain of ceo@bigcorp.com does not
        designate 93.99.104.210 as permitted sender)
        client-ip=93.99.104.210;
Authentication-Results: mx.google.com;
       spf=softfail (google.com: domain of ceo@bigcorp.com does not designate
             93.99.104.210 as permitted sender) smtp.mailfrom=ceo@bigcorp.com;
       dkim=none;
       dmarc=fail (p=QUARANTINE sp=QUARANTINE dis=QUARANTINE) header.from=bigcorp.com
Return-Path: <ceo@bigcorp.com>
From: "John Doe - CEO" <ceo@bigcorp.com>
To: accountant@bigcorp.com
Subject: URGENT - Virement à effectuer aujourd'hui
Date: Thu, 12 Mar 2026 15:47:18 -0700
Message-ID: <2026031215471234567@emkei.cz>
X-Mailer: The Bat! 9.3 (BETA)
```

### Signaux suspects

| Signal | Explication |
|--------|-------------|
| `Received: from emkei.cz [93.99.104.210]` | **emkei.cz** est un service de fake mail notoirement connu, IP blacklistée |
| `spf=softfail` | L'IP n'est pas autorisée par `bigcorp.com` |
| `dkim=none` | Pas de signature DKIM |
| `dmarc=fail` | Désalignement + SPF fail |
| `Message-ID: @emkei.cz` | Révèle l'outil utilisé |
| **BEC (Business Email Compromise)** | Email prétendant être le PDG pour demander un virement urgent |

---

## Exemple 4 : Spoofing whitehouse.gov — Script PHP + Return-Path université

**Technique** : Email prétendant venir de la Maison Blanche, en réalité envoyé via un script PHP sur un serveur universitaire compromis.

```
Received: from webserver.university.edu (webserver.university.edu [130.60.1.42])
        by mx.google.com with ESMTP id w4si5678901qkm;
        Wed, 11 Mar 2026 10:22:15 -0700 (PDT)
Authentication-Results: mx.google.com;
       spf=fail (google.com: domain of president@whitehouse.gov does NOT designate
             130.60.1.42 as permitted sender) smtp.mailfrom=president@whitehouse.gov;
       dkim=none;
       dmarc=fail header.from=whitehouse.gov
Return-Path: <nobody@university.edu>
From: "President of the United States" <president@whitehouse.gov>
To: victim@gmail.com
Subject: Important message from the White House
Date: Wed, 11 Mar 2026 10:22:10 -0700
Message-ID: <20260311102210.654321@webserver.university.edu>
X-PHP-Originating-Script: 500:send_mail.php
X-Mailer: PHP/8.1.12
```

### Signaux suspects

| Signal | Explication |
|--------|-------------|
| `Return-Path: @university.edu` | **Contradiction totale** : le vrai expéditeur est `nobody@university.edu`, pas la Maison Blanche |
| `Received: from webserver.university.edu` | Email envoyé depuis un serveur universitaire (probablement compromis) |
| `spf=fail` | L'IP de l'université n'est pas autorisée par `whitehouse.gov` |
| `X-PHP-Originating-Script: send_mail.php` | Script PHP = outil de phishing automatisé |
| `Message-ID: @webserver.university.edu` | Confirme l'origine réelle |
| `dkim=none` | Aucune signature DKIM de la Maison Blanche |

---

## Exemple 5 : SPF pass + DMARC fail — Désalignement SendGrid

**Technique** : L'attaquant envoie via SendGrid (SPF/DKIM passent pour SendGrid) mais le `From:` usurpe un autre domaine. DMARC détecte le désalignement.

```
Authentication-Results: mx.google.com;
       spf=pass (google.com: domain of bounces+12345@em9876.targetedomain.com
             designates 167.89.102.34 as permitted sender)
             smtp.mailfrom=bounces+12345@em9876.targetedomain.com;
       dkim=pass header.d=em9876.targetedomain.com header.s=s1;
       dmarc=fail (p=REJECT sp=REJECT dis=REJECT) header.from=realdomain.com
Return-Path: <bounces+12345@em9876.targetedomain.com>
From: "Official Support" <support@realdomain.com>
```

### Signaux suspects

| Signal | Explication |
|--------|-------------|
| `spf=pass` pour `em9876.targetedomain.com` | SPF passe — mais pour le **mauvais domaine** |
| `dkim=pass` pour `em9876.targetedomain.com` | DKIM passe — mais pour le **mauvais domaine** |
| `dmarc=fail` pour `realdomain.com` | **DMARC détecte l'incohérence** : `From: @realdomain.com` ≠ domaines SPF/DKIM |
| `Return-Path: @em9876.targetedomain.com` | L'enveloppe révèle le vrai expéditeur (SendGrid d'un attaquant) |

> **Enseignement clé** : SPF pass + DKIM pass ne signifie pas que l'email est légitime. Il faut que ce soit aligné avec le `From:` visible. DMARC vérifie cet alignement.

---

## Récapitulatif des techniques de spoofing

| Technique | Description | Détection |
|-----------|-------------|-----------|
| **Display name spoofing** | Le nom affiché est trompeur mais l'adresse email est suspecte | Vérifier l'adresse complète, pas juste le nom |
| **Lookalike domain** | Domaine similaire (`paypa1.com`, `arnazon.com`) | Comparer soigneusement le domaine |
| **Subdomain spoofing** | `paypal.com.evil.com` — le vrai domaine est `evil.com` | Lire le domaine de droite à gauche |
| **Return-Path spoofing** | From: légitime, Return-Path: frauduleux | Vérifier la cohérence From:/Return-Path: |
| **Reply-To hijacking** | From: légitime, Reply-To: vers attaquant | Vérifier Reply-To: avant de répondre |
| **Fake mailer** | emkei.cz, script PHP → SPF fail/none | Vérifier `X-PHP-Originating-Script`, `X-Mailer` |
| **SendGrid abuse** | SPF/DKIM passent sur domaine SendGrid ≠ From: | DMARC détecte le désalignement |
