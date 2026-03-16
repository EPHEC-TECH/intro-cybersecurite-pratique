# Exemple d'en-tête légitime — Email envoyé via Microsoft 365

**Scénario** : Un email légitime envoyé depuis un domaine corporate utilisant Microsoft 365 (contoso.com) vers un destinataire Office 365.

---

## En-tête brut complet

```
Delivered-To: recipient@fabrikam.com
Received: from BN6PR09MB3220.namprd09.prod.outlook.com
 (2603:10b6:405:64::31) by BN6PR09MB3220.namprd09.prod.outlook.com with HTTPS
 via BN6PR09CA0002.namprd09.prod.outlook.com; Mon, 16 Mar 2026 09:15:33 +0000
ARC-Seal: i=1; a=rsa-sha256; s=arcselector9901; d=microsoft.com; cv=none;
 b=ArcSealFromMicrosoft==
ARC-Message-Signature: i=1; a=rsa-sha256; c=relaxed/relaxed; d=microsoft.com;
 s=arcselector9901;
 h=From:Date:Subject:Message-ID:Content-Type:MIME-Version;
 bh=bodyHashValue=;
 b=ArcMsgSigFromMicrosoft==
ARC-Authentication-Results: i=1; mx.microsoft.com 1; spf=pass
 smtp.mailfrom=contoso.com; dmarc=pass action=none header.from=contoso.com;
 dkim=pass header.d=contoso.com; arc=none
Authentication-Results: spf=pass (sender IP is 40.107.92.56)
 smtp.mailfrom=contoso.com; dkim=pass (signature was verified)
 header.d=contoso.com;dmarc=pass action=none header.from=contoso.com;
 compauth=pass reason=100
Received-SPF: Pass (protection.outlook.com: domain of contoso.com designates
 40.107.92.56 as permitted sender) receiver=protection.outlook.com;
 client-ip=40.107.92.56; helo=mail.contoso.com;
Received: from mail.contoso.com (40.107.92.56) by
 BN6EUR03FT018.mail.protection.outlook.com (10.152.28.28) with Microsoft SMTP
 Server (version=TLS1_2, cipher=TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384)
 id 15.20.9999.001 via Frontend Transport; Mon, 16 Mar 2026 09:15:28 +0000
DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed; d=contoso.com;
 s=selector1; h=From:Date:Subject:Message-ID:Content-Type:MIME-Version:
 X-MS-Exchange-SenderADCheck;
 bh=bodyHashValue=;
 b=dkimSignatureValue==
X-Microsoft-Antispam-PRVS: <GUID@BN6PR09MB3220.namprd09.prod.outlook.com>
X-Forefront-Antispam-Report:
 CIP:40.107.92.56;CTRY:US;LANG:en;SCL:1;SRV:;IPV:NLI;SFV:NSPM;H:mail.contoso.com;PTR:mail.contoso.com;CAT:NONE;SFS:();DIR:INB;
X-Microsoft-Antispam: BCL:0;
X-MS-PublicTrafficType: Email
X-MS-Office365-Filtering-Correlation-Id: GUID-correlation-id
X-MS-Exchange-SenderADCheck: 1
X-MS-Exchange-AntiSpam-Relay: 0
X-Microsoft-Antispam-Message-Info: ExtendedAntiSpamInfo==
Return-Path: bounce@contoso.com
From: John Smith <john.smith@contoso.com>
To: recipient@fabrikam.com
Subject: Budget Q2 2026 - Pour validation
Date: Mon, 16 Mar 2026 09:15:25 +0000
Message-ID: <BN6PR09MB3220AbCdEfGh@BN6PR09MB3220.namprd09.prod.outlook.com>
MIME-Version: 1.0
Content-Type: multipart/mixed; boundary="----=_Part_12345_67890.1742138125000"
X-Originating-IP: [40.107.92.56]
X-MS-Exchange-CrossTenant-OriginalArrivalTime: 16 Mar 2026 09:15:28.1234
X-MS-Exchange-CrossTenant-FromEntityHeader: Internet
```

---

## Analyse des headers Microsoft 365

### Authentication-Results + compauth

```
Authentication-Results: spf=pass (sender IP is 40.107.92.56)
 smtp.mailfrom=contoso.com; dkim=pass (signature was verified)
 header.d=contoso.com;dmarc=pass action=none header.from=contoso.com;
 compauth=pass reason=100
```

| Champ | Valeur | Signification |
|-------|--------|---------------|
| `spf=` | `pass` | ✅ IP `40.107.92.56` autorisée par SPF de `contoso.com` |
| `dkim=` | `pass` | ✅ Signature DKIM valide pour `contoso.com` |
| `dmarc=` | `pass` | ✅ Alignement vérifié, politique `action=none` |
| `compauth=` | `pass` | ✅ Authentification composite Microsoft : email légitime |
| `reason=` | `100` | Code : SPF pass OU DKIM pass avec domaines alignés |

### X-Forefront-Antispam-Report décrypté

```
CIP:40.107.92.56    → IP connectante
CTRY:US             → Pays source (États-Unis)
LANG:en             → Langue détectée : anglais
SCL:1               → Spam Confidence Level = 1 (très bas, pas du spam)
IPV:NLI             → IP non trouvée sur des listes de réputation négatives
SFV:NSPM            → Spam filtering : Non-SPaM (pas du spam)
CAT:NONE            → Aucune catégorie de menace détectée
DIR:INB             → Direction : email entrant (INBound)
```

**Valeurs SCL** :
| SCL | Signification |
|-----|---------------|
| -1 | Liste blanche (skip du filtre) |
| 0-1 | Probablement pas spam |
| 5-6 | Probablement spam |
| 7-9 | Certainement spam |

### X-Microsoft-Antispam : BCL

```
BCL:0
```
**BCL (Bulk Complaint Level)** : mesure si l'email ressemble à de l'emailing en masse.
- 0 = pas de bulk mail
- 7-9 = fort bulk mail (newsletters agressives, marketing)

---

## Codes `reason` compauth (référence)

| Code | Signification |
|------|---------------|
| `100` | SPF pass ou DKIM pass avec domaines alignés |
| `101` | Message signé DKIM par le domaine du From: |
| `102` | Domaines MAIL FROM et From: alignés, SPF pass |
| `000` | Échec DMARC avec politique `reject` ou `quarantine` |
| `001` | Échec authentification implicite (pas d'enregistrements) |
| `010` | Échec DMARC sur un domaine interne à l'organisation |

---

## Points clés de cet email légitime Microsoft 365

1. **Triple pass** : SPF, DKIM, DMARC tous passants
2. **compauth=pass reason=100** : Microsoft confirme l'authenticité
3. **SCL:1** : score spam très bas
4. **BCL:0** : pas de bulk mail
5. **IP cohérente** : `40.107.92.56` est une IP Microsoft Exchange Online connue
6. **Message-ID** : domaine `BN6PR09MB3220.namprd09.prod.outlook.com` → infrastructure Microsoft authentique
