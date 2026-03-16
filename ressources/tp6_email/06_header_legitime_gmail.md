# Exemple d'en-tête légitime — Email envoyé via Gmail

**Scénario** : Alice (alice@example.com, domaine hébergé sur Google Workspace) envoie un email à Bob (bob@gmail.com).

---

## En-tête brut complet

```
Delivered-To: bob@gmail.com
Received: by 2002:a17:906:4cd6:b0:a91:7c82:9e5f with SMTP id s22csp1234567qvw;
        Mon, 16 Mar 2026 09:00:12 -0700 (PDT)
X-Received: by 2002:a17:906:3e8a:b0:a3f:1b2c:3d4e with SMTP id m10mr4567890pgb;
        Mon, 16 Mar 2026 09:00:12 -0700 (PDT)
ARC-Seal: i=1; a=rsa-sha256; t=1742137212; cv=none;
        d=google.com; s=arc-20160816;
        b=ArcSealValue==
ARC-Message-Signature: i=1; a=rsa-sha256; c=relaxed/relaxed; d=google.com; s=arc-20160816;
        h=to:subject:message-id:date:from:mime-version:dkim-signature;
        bh=47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU=;
        b=ArcMsgSigValue==
ARC-Authentication-Results: i=1; mx.google.com;
       dkim=pass header.d=example.com header.s=20230601 header.b=AbCdEfGh;
       spf=pass (google.com: domain of alice@example.com designates 209.85.220.41
             as permitted sender) smtp.mailfrom=alice@example.com;
       dmarc=pass (p=REJECT sp=REJECT dis=NONE) header.from=example.com
Return-Path: <alice@example.com>
Received: from mail-sor-f41.google.com (mail-sor-f41.google.com. [209.85.220.41])
        by mx.google.com with SMTPS id a12si1234567qkm.2026.03.16.09.00.11
        for <bob@gmail.com>
        (Google Transport Security);
        Mon, 16 Mar 2026 09:00:11 -0700 (PDT)
Received-SPF: pass (google.com: domain of alice@example.com designates
        209.85.220.41 as permitted sender) client-ip=209.85.220.41;
Authentication-Results: mx.google.com;
       dkim=pass header.d=example.com header.s=20230601 header.b=AbCdEfGh;
       spf=pass (google.com: domain of alice@example.com designates 209.85.220.41
             as permitted sender) smtp.mailfrom=alice@example.com;
       dmarc=pass (p=REJECT sp=REJECT dis=NONE) header.from=example.com
DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed;
        d=example.com; s=20230601;
        h=mime-version:from:date:message-id:subject:to;
        bh=47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU=;
        b=AbCdEfGhIjKlMnOpQrStUvWxYz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ
         abcdefghijklmnopqrstuvwxyz0123456789+/AbCdEfGhIjKlMnOpQrStUv==
X-Google-DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed;
        d=1e100.net; s=20230601;
        h=x-gm-message-state:mime-version:from:date:message-id:subject:to;
        bh=47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU=;
        b=GoogleInternalSignature==
X-Gm-Message-State: AOJu0YxBpSo1PQexampleGmailInternalState
X-Google-Smtp-Source: AGHT+IExampleSmtpSourceString
X-Received: by 2002:a17:90a:3e8a:: with SMTP id m10mr9876543pgb.2026.03.16.09.00.10;
        Mon, 16 Mar 2026 09:00:10 -0700 (PDT)
MIME-Version: 1.0
From: Alice Martin <alice@example.com>
Date: Mon, 16 Mar 2026 17:00:09 +0100
Message-ID: <CABcDeFgHiJkLmNoPqRsTuVwXyZ@mail.gmail.com>
Subject: Réunion demain à 14h
To: bob@gmail.com
Content-Type: multipart/alternative; boundary="000000000000abcdef0123456789"
```

---

## Analyse champ par champ

| Header | Valeur | Analyse |
|--------|--------|---------|
| `Delivered-To:` | `bob@gmail.com` | ✅ Destinataire final correct |
| `Return-Path:` | `<alice@example.com>` | ✅ Même domaine que le From: → SPF aligné |
| `Authentication-Results:` | `dkim=pass; spf=pass; dmarc=pass` | ✅ Triple authentification réussie |
| `DKIM-Signature: d=` | `example.com` | ✅ Même domaine que le From: → DKIM aligné |
| `DKIM-Signature: s=` | `20230601` | Info : sélecteur permettant de retrouver la clé DNS |
| `From:` | `Alice Martin <alice@example.com>` | ✅ Correspond au domaine SPF et DKIM |
| `Received:` IP | `209.85.220.41` | ✅ IP Google (vérifiable : dig ptr 41.220.85.209.in-addr.arpa) |
| `Message-ID:` | `@mail.gmail.com` | ✅ Cohérent avec l'infrastructure Google |

---

## Points clés de cet email légitime

1. **SPF=pass** : l'IP `209.85.220.41` est bien dans le SPF de `example.com` (via `include:_spf.google.com`)
2. **DKIM=pass** : la signature `d=example.com` correspond au `From: alice@example.com`
3. **DMARC=pass** : alignement vérifié — le `From:` domaine = domaine SPF = domaine DKIM
4. **Return-Path = From domaine** : pas de discordance entre enveloppe et header visible
5. **IP cohérente** : `209.85.220.41` est un serveur Google connu

---

## Vérification via MXToolbox

Pour vérifier cet email :
1. Aller sur https://mxtoolbox.com/EmailHeaders.aspx
2. Coller l'en-tête ci-dessus
3. Vérifier que tous les checks passent au vert
