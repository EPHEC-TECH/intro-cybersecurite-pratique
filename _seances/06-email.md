---
layout: default
title: Sécurité Email
order: 6
description: SPAM, SPF, DKIM, DMARC, Phishing
nav_order: 6
published: true
---

# Séance 6 : Sécurité des Emails
{: .no_toc }

## Table des matières
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Objectifs pédagogiques

À la fin de la séance, l'étudiant sera capable de :

- Comprendre que l'adresse `From:` d'un email peut être falsifiée.
- Lire les résultats d'authentification (SPF, DKIM, DMARC) dans les en-têtes d'un email.
- Utiliser MXToolbox pour analyser des emails suspects.
- Identifier les signaux concrets d'un email frauduleux.

---

## Introduction : l'email n'a pas été conçu pour la sécurité

L'email existe depuis 1971 (ARPANET). Le protocole SMTP qui le transporte a été standardisé en 1982. À l'époque, tout le monde se connaissait sur Internet — la sécurité n'était pas une priorité. Résultat : **n'importe qui peut envoyer un email en se faisant passer pour n'importe qui**.

C'est comme envoyer une lettre papier : vous pouvez écrire `Expéditeur : Président de la République` sur l'enveloppe. Le facteur la livrera quand même.

Depuis, trois mécanismes ont été ajoutés pour authentifier les emails :

| Mécanisme | Rôle |
|-----------|------|
| **SPF** | Vérifie si le serveur qui envoie l'email est autorisé par le domaine |
| **DKIM** | Vérifie si l'email a été signé cryptographiquement par le domaine |
| **DMARC** | Vérifie l'alignement SPF/DKIM avec le `From:` visible, et définit la politique (rejeter ? mettre en spam ?) |

Dans ce TP, vous allez jouer le rôle d'un analyste sécurité et examiner des emails suspects reçus dans une organisation belge.

---

## Exercice : Dans la boîte noire des emails

{: .d-inline-block }
Durée estimée : 20 min
{: .label .label-yellow }

{: .highlight }
> **Outil requis :** [MXToolbox](https://mxtoolbox.com) — accessible depuis n'importe quel navigateur, sans installation.

### Mise en situation

> Vous venez d'intégrer l'équipe IT d'une PME belge. Ce matin, deux employés ont transféré des emails qu'ils ont trouvés suspects. Votre mission : analyser les en-têtes techniques pour déterminer si ces emails sont légitimes.

---

### Et dans votre vraie boîte mail ?

Avant de commencer, ouvrez votre client email et affichez les en-têtes complets d'un email quelconque que vous avez reçu — une newsletter, un email de l'EPHEC, peu importe.

**Comment faire :**
- **Outlook 365 (version web)** : ouvrir l'email → menu (trois petits points) ⋯ → *Affichager* → *Afficher les détails du message*
- **Gmail** : ouvrir l'email → menu ⋮ → *Afficher l'original*
- **Apple Mail** : menu *Affichage* → *Message* → *Tous les en-têtes*
- etc ...

{: .highlight }
> Prenez le temps de parcourir ce bloc de texte. Vous allez y retrouver la plupart des champs que vous manipulerez dans la suite de cet exercice : `From:`, `Return-Path:`, `Received:`, `Authentication-Results:`...

---

### Étape 0 — Comprendre la baseline

{: .d-inline-block }
~5 min
{: .label .label-green }

Avant d'analyser les emails suspects, allez vérifier comment un domaine **sérieusement protégé** est configuré.

1. Rendez-vous sur [https://mxtoolbox.com/SuperTool.aspx](https://mxtoolbox.com/SuperTool.aspx)
2. Tapez `dmarc:bnpparibas.fr` et lancez la recherche
3. Observez la politique DMARC en place

> Gardez ce résultat en tête — il vous servira à analyser le premier email suspect.

---

### Email suspect n°1 — "Votre compte bancaire a été suspendu"

{: .d-inline-block }
~7 min
{: .label .label-green }

Un employé a reçu cet email prétendant venir de BNP Paribas. Copiez l'intégralité du bloc ci-dessous et collez-le dans [https://mxtoolbox.com/EmailHeaders.aspx](https://mxtoolbox.com/EmailHeaders.aspx), puis cliquez sur **Analyze Header**.

```
Delivered-To: employe@votrepme.be
Received: by 2002:a17:906:4cd6:b0:a91:7c82:9e5f with SMTP id x22csp112233qvw;
        Tue, 17 Mar 2026 02:14:33 -0700 (PDT)
Received: from mail.srv-bulk99.ru (mail.srv-bulk99.ru [185.220.101.47])
        by mx.google.com with ESMTP id a1si9876543qkm.2026.03.17.02.14.32
        for <employe@votrepme.be>;
        Tue, 17 Mar 2026 02:14:32 -0700 (PDT)
Received-SPF: fail (google.com: domain of support@bnpparibas.fr does NOT
        designate 185.220.101.47 as permitted sender)
        client-ip=185.220.101.47;
Authentication-Results: mx.google.com;
       spf=fail (google.com: domain of support@bnpparibas.fr does NOT designate
             185.220.101.47 as permitted sender) smtp.mailfrom=support@bnpparibas.fr;
       dkim=none;
       dmarc=fail (p=REJECT sp=REJECT dis=NONE) header.from=bnpparibas.fr
Return-Path: <support@bnpparibas.fr>
From: "BNP Paribas - Service Sécurité" <support@bnpparibas.fr>
To: employe@votrepme.be
Reply-To: bnp-verification@protonmail.com
Subject: [URGENT] Votre compte a été suspendu - Vérification requise sous 24h
Date: Tue, 17 Mar 2026 02:14:28 -0700
Message-ID: <20260317021428.bulk99@srv-bulk99.ru>
X-PHP-Originating-Script: 1000:bulk_mailer.php
X-Mailer: PHPMailer 6.6.5
MIME-Version: 1.0
Content-Type: text/html; charset=UTF-8
```

#### Questions

1. Regardez le champ `Authentication-Results`. Quels sont les résultats SPF, DKIM et DMARC ?
2. Regardez le `Message-ID`. Quel domaine apparaît à la fin ? Est-ce cohérent avec l'expéditeur affiché ?
3. L'email affiche `From: support@bnpparibas.fr` et `Return-Path: support@bnpparibas.fr`. Pourtant, si vous cliquez sur **Répondre**, votre réponse ira à `Reply-To: bnp-verification@protonmail.com`. Qu'est-ce que cela vous inspire ?
4. MXToolbox affiche l'IP `185.220.101.47`. Cliquez sur cette IP dans l'interface. Que dit MXToolbox à son sujet ?
5. Rappelez-vous la politique DMARC de `bnpparibas.fr` que vous avez vérifiée à l'étape 0. Cet email aurait-il dû arriver dans la boîte de réception ? Regardez le tag `dis=` dans `Authentication-Results` — que vous apprend-il sur ce qui s'est réellement passé ?

---

### Email suspect n°2 — "Confirmez votre paiement PayPal"

{: .d-inline-block }
~8 min
{: .label .label-green }

Un second employé a reçu cet email. Même procédure : copiez et collez dans [https://mxtoolbox.com/EmailHeaders.aspx](https://mxtoolbox.com/EmailHeaders.aspx).

```
Delivered-To: employe@votrepme.be
Received: by 2002:a17:906:5abc:b0:a91:9c44:1e2f with SMTP id r11csp334455qvw;
        Mon, 16 Mar 2026 14:07:19 -0700 (PDT)
Received: from emkei.cz (emkei.cz [93.99.104.210])
        by mx.google.com with ESMTP id e1si1234567qkm.2026.03.16.14.07.18
        for <employe@votrepme.be>;
        Mon, 16 Mar 2026 14:07:18 -0700 (PDT)
Received-SPF: softfail (google.com: domain of noreply@paypal.com does not
        designate 93.99.104.210 as permitted sender)
        client-ip=93.99.104.210;
Authentication-Results: mx.google.com;
       spf=softfail (google.com: domain of noreply@paypal.com does not designate
             93.99.104.210 as permitted sender) smtp.mailfrom=noreply@paypal.com;
       dkim=none;
       dmarc=fail (p=REJECT sp=REJECT dis=NONE) header.from=paypal.com
Return-Path: <noreply@paypal.com>
From: "Service PayPal" <noreply@paypal.com>
To: employe@votrepme.be
Reply-To: support@paypa1-secure.net
Subject: Votre paiement de 349,00 EUR a été initié - Confirmez maintenant
Date: Mon, 16 Mar 2026 14:07:15 -0700
Message-ID: <20260316140715.654321@emkei.cz>
X-Mailer: The Bat! 9.3
MIME-Version: 1.0
Content-Type: text/html; charset=UTF-8
```

#### Questions

1. Quel service a envoyé cet email, selon le champ `Received: from` ? Cherchez ce nom sur un moteur de recherche.
2. Regardez attentivement l'adresse `Reply-To`. Comparez-la avec `paypal.com`. Voyez-vous quelque chose d'inhabituel ?
3. MXToolbox indique-t-il quelque chose concernant l'IP `93.99.104.210` ?
4. SPF retourne `softfail` plutôt que `fail`. Quelle différence y a-t-il entre les deux ? Est-ce que `softfail` signifie que l'email est légitime ?

---

### Questions de synthèse

1. Dans les deux emails, le champ `From:` affiche des adresses qui semblent parfaitement légitimes. Pourquoi ne faut-il pas se fier uniquement au `From:` pour juger de la légitimité d'un email ?
2. Quel est, selon vous, le champ le plus fiable pour identifier l'origine réelle d'un email ?
3. Si votre organisation voulait se protéger contre ce type d'usurpation d'identité de son propre domaine, quelle politique DMARC devrait-elle mettre en place ?

---

## Quiz phishing

{: .d-inline-block }
À faire en autonomie
{: .label .label-blue }

Le phishing ne passe pas toujours par des en-têtes suspects — parfois, l'email semble parfaitement légitime à l'œil nu. Ce quiz développé par Google met votre instinct à l'épreuve : saurez-vous distinguer un vrai email d'un faux, uniquement à partir de ce que vous voyez à l'écran ?

👉 [https://phishingquiz.withgoogle.com/](https://phishingquiz.withgoogle.com/)

Notez votre score et réfléchissez aux cas qui vous ont trompé. Quels indices visuels auraient pu vous alerter ?
