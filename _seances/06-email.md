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
- **Outlook 365 (version web)** : ouvrir l'email → menu ⋯ → *Afficher* → *Afficher les détails du message*
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

{: .note }
> SPF, DKIM et DMARC ne sont pas de la magie : ils reposent sur des informations **publiques**, publiées par chaque domaine dans le DNS. Tout le monde peut les consulter — un serveur de messagerie, un outil en ligne, ou vous. C'est précisément ce qui les rend fiables : la "source de vérité" est publique et vérifiable par n'importe qui, à tout moment. DKIM va un cran plus loin en ajoutant une signature cryptographique (le même principe de clé publique/privée que vous avez vu en séance 3).

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

### Email suspect n°3 — "Transmission de facture"

{: .d-inline-block }
~10 min
{: .label .label-yellow }

{: .highlight }
> **Note :** Cet email est un vrai email reçu par une PME belge (les noms ont été anonymisés). 
> 
>Même procédure : copiez et collez les en-têtes dans [https://mxtoolbox.com/EmailHeaders.aspx](https://mxtoolbox.com/EmailHeaders.aspx).

```
Return-Path: <carine.obfuscated@ac-dijon.fr>
Delivered-To: laurent@fake-company.be
Received: from localhost (HELO queue) (127.0.0.1)
	by localhost with SMTP; 7 Mar 2026 19:23:46 +0200
Received: from unknown (HELO output43.mail.ovh.net) (192.168.13.45)
  by 192.168.9.40 with AES256-GCM-SHA384 encrypted SMTP; 7 Mar 2026 19:23:46 +0200
Received: from vr25.mail.ovh.net (unknown [10.101.8.25])
	by out43.mail.ovh.net (Postfix) with ESMTP id 4fSqr24ktfz2cMZw
	for <laurent@fake-company.be>; Sat,  7 Mar 2026 17:23:46 +0000 (UTC)
Received: from in42.mail.ovh.net (unknown [10.101.4.42])
	by vr25.mail.ovh.net (Postfix) with ESMTP id 4fSqr24FpSz1spdQ
	for <laurent@fake-company.be>; Sat,  7 Mar 2026 17:23:46 +0000 (UTC)
Received: from smtp-out.ac-dijon.fr (smtp-out.ac-dijon.fr [195.221.236.195])
	by in42.mail.ovh.net (Postfix) with ESMTP id 4fSqr23ZBdzVfdv
	for <laurent@fake-company.be>; Sat,  7 Mar 2026 17:23:46 +0000 (UTC)
Authentication-Results: mx.mail.ovh.net;
    arc=none (no signatures found);
    dkim=pass (2048-bit rsa key sha256) header.d=ac-dijon.fr header.i=@ac-dijon.fr header.b=DbYa7C9k header.a=rsa-sha256 header.s=smtp;
    dmarc=pass policy.published-domain-policy=quarantine policy.applied-disposition=none policy.evaluated-disposition=none (p=quarantine,d=none,d.eval=none) policy.policy-from=p header.from=ac-dijon.fr;
    spf=pass smtp.mailfrom=Carine.obfuscated@ac-dijon.fr smtp.helo=smtp-out.ac-dijon.fr
Received-SPF: pass
    (ac-dijon.fr: 195.221.236.195 is authorized to use 'Carine.obfuscated@ac-dijon.fr' in 'mfrom' identity (mechanism 'ip4:195.221.236.195' matched))
    receiver=in42.mail.ovh.net;
    identity=mailfrom;
    envelope-from="Carine.obfuscated@ac-dijon.fr";
    helo=smtp-out.ac-dijon.fr;
    client-ip=195.221.236.195
Received: from hermes.ac-dijon.fr (localhost [127.0.0.1])
	by smtp-out.ac-dijon.fr (Postfix) with ESMTP id 53B333190
	for <laurent@fake-company.be>; Sat,  7 Mar 2026 18:23:46 +0100 (CET)
Received: from [127.0.0.1] (unknown [196.127.21.25])
	by hermes.ac-dijon.fr (Postfix) with ESMTPSA id 19C7A1950
	for <laurent@fake-company.be>; Sat,  7 Mar 2026 18:23:45 +0100 (CET)
DKIM-Filter: OpenDKIM Filter v2.11.0 hermes.ac-dijon.fr 19C7A1950
DKIM-Signature: v=1; a=rsa-sha256; c=simple/simple; d=ac-dijon.fr; s=smtp;
	t=1772904226; bh=P1i60UFy7px4128qI0FOPPNQAS0CX0pLhWqyPjGwNT8=;
	h=From:To:Subject:Message-ID:Date:From;
	b=DbYa7C9kC8fpOTnnG0fQZ2BdrJ5qWEjcyjj2YRo9AxlrcZa8kmHsVDdlSzOrMq4zG
	 YPjhjdYb5Jm4r+7mCufX8nLcQp141iM0UUghy0SwDMnpPtKbouRhby36jByDEWd8Do
	 X4OhBDMimjOIw2+fZ4EQvrnJ3nXm2GfuCqBJjQ6o74GM3QL46RVRachj1DRpqOI3q+
	 ph5F+wfKuOBdyfkHXF3uVuGVrGZjlDNGAfR810m7qPouKHEAkM42NPqzVNLIVVy1Fh
	 mxSkEHaePrb8RcDVnehsNa4kv/UGCjq8eC/Y2CeXv0vzdDvrUeZ2LcJSPFhCSu4b95
	 gejsXliwKRqzw==
Content-Type: text/html
From: =?UTF-8?Q?Service_Comptabilit=C3=A9?= <Carine.obfuscated@ac-dijon.fr>
To: laurent@fake-company.be
Subject: =?UTF-8?Q?Transmission_de_facture_=E2=80=93_Servic?=
 =?UTF-8?Q?e_Comptabilit=C3=A9?=
Message-ID: <051088b1-099e-a5a6-bf62-602e3122212f@ac-dijon.fr>
Content-Transfer-Encoding: quoted-printable
Date: Sat, 07 Mar 2026 17:23:45 +0000
MIME-Version: 1.0
X-OVH-Remote: 195.221.236.195 (smtp-out.ac-dijon.fr)
x-ovh-tracer-id: 6855041585889247582
X-VR-SPAMSTATE: DCE
X-VR-SPAMSCORE: 107
X-VR-SPAMCAUSE: dmFkZTECcuZq7YqWJnu5Sb6RUGV9Tyb4KWz+M27yu09LX35dDoTksCIzBn1wTENZBH4e4MOTd7U8nVSaIbjR/Ru1bYAtElutd7Pw0x00mvzauiqp4jwMArbuVFedJZcl4gJwTYxxwwHhyZFs5ZqEADnthDfQoIHhY/L4q2P0yMmWQO88nvxKBN7tpONZ4GMclqJgoXxLCn2XkW5v55u8W5rZc21EQGrRkc7Re1QmHhg/dtLSg73uMqKIDjQOO1uoT0dCycTDnZVptIZeqZDqLzieD/+O/8jHJ18eflOJYTWjUJkzP7hlHlwXMkltXU7X73IZ6Gs3gstpK2zldDaVc6t8HPMch+vTYEKZuQ/RsFk0CSJrr0adoIQWLRgqqiU0OubNCny7J46/dISCDPmJeOsT4iJNgDDrinhpqxqES/bsMgoTuiV8wEHjyyXbHpHqQ/emrbXY6nwfaGL9AmqtWZYzA7lZEZPiwL0p5xuqRMKLwuWUiUHoZENi4jZjIGDZeyD4ImsifJHSJeWDiMfZCq/YIr7SpaJWWTkrZTtCM9p/UxbtU29z2pYWSQfvGn5AuQiGq72W6hR68OQ0kY4uNo/bPkzDbvPNGkjVIRoyF5bmwogTubFVXeB4DM2ghNvzDEi9bdgZz56a4Ei9Pxb7dKcRGeuGYqw6k/B6N5QHhqKmoGxFlw
X-Ovh-Spam-Status: OK
X-Ovh-Spam-Reason: vr: OK; dkim: disabled; spf: disabled
X-Ovh-Message-Type: DCE
<p class=3D"gmail-isSelectedEnd">Bonjour,</p>
<p class=3D"gmail-isSelectedE=
nd">Veuillez trouver ci-dessous le lien pour consulter et =
t&eacute;l&eacute;charger la facture relative &agrave; nos prestations =
:</p>
<p class=3D"gmail-isSelectedEnd"><span class=3D"gmail-text-token-text=
-primary gmail-cursor-text gmail-rounded-sm"><a href=3D"https://docsign.=
ecrosa.cfd/">Lien de la facture</a></span></p>
<p class=3D"gmail-isSelected=
End">Nous vous remercions de bien vouloir proc&eacute;der &agrave; son =
r&egrave;glement selon les modalit&eacute;s convenues.</p>
<p class=3D"gmail-isSelectedEnd">Restant &agrave; votre disposition pour =
toute information compl&eacute;mentaire.</p>
<p>Cordialement,</p>
<p>Service Comptabilit&eacute;</p>
<p>Transmission de facture&nbsp;</p>
<p>&nbsp;</p>

```

#### Questions

1. Commencez par le champ `Authentication-Results`. Quels sont les résultats SPF, DKIM et DMARC ? Ce résultat vous rassure-t-il sur la légitimité de l'email ?

2. Regardez le domaine de l'expéditeur (`From:`). Faites une rapide recherche : à quel type d'organisation appartient ce domaine ? Est-il cohérent que cette organisation envoie une facture à une PME belge ?

3. L'email contient un lien cliquable vers une facture. Survolez ce lien (sans cliquer) ou cherchez-le dans les en-têtes. Quel est le domaine de destination ? Que pensez-vous de l'extension utilisée (le TLD) ?

4. Remontez la chaîne des champs `Received:` jusqu'à l'entrée du mail dans l'infrastructure de l'expéditeur. Quelle est l'IP de la machine qui a initié l'envoi ? Géolocalisez cette IP. Ce résultat correspond-il à ce que vous attendriez de l'expéditeur déclaré ?

5. Cherchez les champs dont le nom commence par `X-VR-SPAM` et `X-Ovh-Message-Type`. Que vous indiquent-ils ? Sont-ils cohérents avec les résultats d'authentification ?

6. En tenant compte de l'ensemble de vos observations, quel scénario vous semble le plus probable pour expliquer cet email ?

---

### Questions de synthèse

1. Dans les deux premiers emails, les authentifications échouaient clairement. Dans le troisième, elles passent toutes. Cela signifie-t-il que SPF/DKIM/DMARC garantissent qu'un email est légitime ?
2. Quel est, selon vous, le champ le plus fiable pour identifier l'origine réelle d'un email ?
3. Si votre organisation voulait se protéger contre ce type d'usurpation d'identité de son propre domaine, quelle politique DMARC devrait-elle mettre en place ?

---

## Quiz phishing

Le phishing ne passe pas toujours par des en-têtes suspects — parfois, l'email semble parfaitement légitime à l'œil nu (et respecte le DKIM/SPF/DMARC). Ce quiz développé par Google met votre instinct à l'épreuve : saurez-vous distinguer un vrai email d'un faux, uniquement à partir de ce que vous voyez à l'écran ?

=> [https://phishingquiz.withgoogle.com/](https://phishingquiz.withgoogle.com/)

Notez votre score et réfléchissez aux cas qui vous ont trompé. Quels indices visuels auraient pu vous alerter ?
