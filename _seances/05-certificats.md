---
layout: default
title: Pratique & Certificats
order: 5
description: Diffie-Hellman, SSH, TLS, Wireshark
nav_order: 5
published: true
---

# Séance 5 : Mise en pratique et Certificats
{: .no_toc }

## Table des matières
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Objectifs pédagogiques

À la fin de la séance, l'étudiant sera capable de :

- Comprendre le principe de l'échange de clés Diffie-Hellman.
- Expliquer comment le chiffrement asymétrique permet d'échanger une clé symétrique.
- Comprendre la différence entre Telnet et SSH.
- Observer dans Wireshark la différence entre trafic chiffré et non chiffré.
- Comprendre le rôle d'une PKI et des certificats TLS.
- Identifier les étapes principales du TLS Handshake.
- Comprendre la chaîne de confiance (Chain of Trust).

---

## Rappel : Échange de clés symétriques

Une clé symétrique et une clé asymétrique sont deux façons différentes de chiffrer et déchiffrer des données. La différence fondamentale tient au nombre de clés utilisées et à la façon dont elles sont partagées.

### Clé symétrique : une seule clé pour tout

La cryptographie symétrique utilise une seule clé pour chiffrer et déchiffrer.

| | |
|---|---|
| **Principe** | Même clé pour les deux opérations |
| **Exemples** | AES, DES, ChaCha20 |
| **Avantages** | Très rapide, efficace pour chiffrer de gros volumes de données |
| **Inconvénients** | Il faut partager la clé en toute sécurité ; si elle fuit, tout est compromis |

{: .note }
**Analogie :** C'est comme une maison avec une seule clé. Si tu la donnes à quelqu'un, il peut entrer et sortir.

### Clé asymétrique : une paire de clés différentes

La cryptographie asymétrique utilise deux clés différentes mais liées mathématiquement :

- **Clé publique** — peut être partagée avec tout le monde.
- **Clé privée** — doit rester secrète.

Ce qui est chiffré avec l'une ne peut être déchiffré qu'avec l'autre.

| | |
|---|---|
| **Exemples** | RSA, ECC, Diffie-Hellman |
| **Avantages** | Pas besoin d'échanger un secret au départ ; permet signatures, authentification, échanges sécurisés |
| **Inconvénients** | Plus lent, plus coûteux en calcul |

{: .note }
**Analogie :** Une boîte aux lettres. Tout le monde peut y mettre un message (clé publique), mais seul le propriétaire peut l'ouvrir (clé privée).

### Comment les deux s'utilisent ensemble ?

Dans la pratique (HTTPS, VPN, SSH…), on combine les deux :

- **Asymétrique** pour échanger une clé symétrique en toute sécurité.
- **Symétrique** pour chiffrer le reste de la communication (rapide et efficace).

---

## 1. Diffie-Hellman

### 1.1 Problème

{: .highlight }
> **Comment deux personnes peuvent-elles partager une clé secrète si quelqu'un écoute le réseau ?** Si on envoie la clé directement → elle peut être interceptée !!

### 1.2 Principe de Diffie-Hellman (DH)

Deux personnes peuvent créer une clé commune **sans jamais l'envoyer sur le réseau**.

**Participants :**
- Alice
- Bob
- Eve (l'attaquant qui écoute)

### L'échange de clés Diffie-Hellman

L'objectif de Diffie–Hellman est le suivant :

> Permettre à deux personnes (Alice et Bob) de créer une clé secrète commune en ne s'échangeant publiquement que des données non secrètes, même en présence d'un espion (Eve).

Cette clé commune servira ensuite à chiffrer leurs communications.

Diffie–Hellman repose sur une propriété mathématique très utile : **il est facile de faire des exponentiations modulo un nombre, mais très difficile de retrouver l'exposant** (problème du logarithme discret).

#### Les ingrédients de départ

Alice et Bob choisissent (ou utilisent des paramètres publics standards) :
- un grand nombre premier : **p**
- une base (appelée générateur) : **g**

Ces deux valeurs **ne sont pas secrètes**.

#### Étapes de l'échange

**1 — Alice choisit un secret**

Elle prend un nombre secret **a** (privé).

Elle calcule : `A = g^a mod p`

Elle envoie **A** à Bob (public).

**2 — Bob choisit un secret**

Il prend un nombre secret **b** (privé).

Il calcule : `B = g^b mod p`

Il envoie **B** à Alice (public).

**3 — Ils calculent chacun la clé partagée**

| Côté Alice | Côté Bob |
|---|---|
| `s = B^a mod p` | `s = A^b mod p` |

**Résultat :** Alice et Bob obtiennent la **même clé secrète**. Eve, qui n'a vu que `p`, `g`, `A` et `B`, ne peut pas retrouver `s`.

#### Pourquoi c'est sécurisé ?

Eve dispose de :
- `p` (public)
- `g` (public)
- `A = g^a mod p` (intercepté)
- `B = g^b mod p` (intercepté)

Mais retrouver **a** ou **b** à partir de ces valeurs est pratiquement impossible avec de grands nombres — c'est le **problème du logarithme discret**.

{: .important }
> **Pourquoi Diffie–Hellman est important ?**
> - Première méthode publique permettant d'établir un secret partagé à travers un réseau non sécurisé.
> - Utilisé dans : TLS/HTTPS, SSH, VPN
> - Signal, WhatsApp (via une variante : ECDH sur courbes elliptiques)

---

## Exercice 1 : Échange Diffie-Hellman avec OpenSSL

{: .d-inline-block }
Durée estimée : 30 min
{: .label .label-yellow }

{: .highlight }
> Vous allez travailler sur votre VM Linux ou sur [Killercoda](https://killercoda.com/playgrounds/scenario/ubuntu) (Linux dans le navigateur). Vous pourrez échanger les fichiers via copier-coller dans Teams.

Dans cet exercice, vous allez reproduire le principe utilisé dans HTTPS, SSH ou les VPN pour établir une clé secrète. **Deux utilisateurs (Alice et Bob)** vont :

1. Générer chacun une clé privée
2. Échanger uniquement leur clé publique
3. Calculer une clé secrète commune

La clé finale sera identique pour les deux utilisateurs, **sans jamais avoir été transmise sur le réseau**. C'est le principe de l'algorithme Diffie–Hellman.

**Répartition dans chaque groupe :**

| Étudiant 1 | Étudiant 2 |
|---|---|
| Alice | Bob |

---

### Étape 1 — Création des paramètres Diffie-Hellman

L'enseignant fournit un fichier contenant les **paramètres publics DH**. Ces paramètres doivent être identiques pour Alice et Bob.

Sur **les deux machines**, créez le fichier suivant :

```bash
nano dhparams.pem
```

Collez le contenu suivant :

```
-----BEGIN DH PARAMETERS-----
MIIBCAKCAQEA7adkL/pcJz8I/VVYaIJCK36B739i5FgXMCmLYyROCZXl4AiBp/JN
5jx36ZCb4vNfGTmDaUe87lC+r2Uph3N3Uw8S+NFTbbvSaDGS2hmuNvpURQXoAZQa
o96wkbSh+Yk2QSUtAHSJJpH862uF+cQBFhaoE90IhS6iPNY2TIeLu2XujP4euj6L
7vQlo5aex9TtJcmFKrOGy94FvKTKqe93gzRWGIfqWlH+4lm48jOBqfVadGeL8bJs
Ks6NVnup81vxY87NUPLSV3z8pYUK+bTb9YGeeHX4kJDaJqb+vUF4eiSpECw2AJEi
MtbhUbp1ftvV6+5Uv/uCOxqkpURc9rQ8BwIBAg==
-----END DH PARAMETERS-----
```

Sauvegardez (`Ctrl+O`, `Entrée`, `Ctrl+X`).

{: .note }
Ces paramètres sont **publics** et identiques pour tous.

---

### Étape 2 — Génération de la clé privée

Chaque étudiant génère sa propre clé privée.

{: .warning }
> **Cette clé ne doit jamais être partagée.**

| Alice | Bob |
|---|---|
| `openssl genpkey -paramfile dhparams.pem -out alice_private.pem` | `openssl genpkey -paramfile dhparams.pem -out bob_private.pem` |

**Vérification :**
```bash
ls
```
Vous devriez voir `alice_private.pem` (pour Alice) ou `bob_private.pem` (pour Bob).

---

### Étape 3 — Génération de la clé publique

À partir de la clé privée, chaque étudiant génère une clé publique. C'est la **seule information qui sera échangée**.

| Alice | Bob |
|---|---|
| `openssl pkey -in alice_private.pem -pubout -out alice_public.pem` | `openssl pkey -in bob_private.pem -pubout -out bob_public.pem` |

---

### Étape 4 — Échange des clés publiques

**Alice envoie sa clé publique à Bob :**

```bash
cat alice_public.pem
```

Copiez le contenu et envoyez-le à Bob via Teams.

**Bob envoie sa clé publique à Alice :**

```bash
cat bob_public.pem
```

Copiez le contenu et envoyez-le à Alice via Teams.

**Enregistrer la clé reçue :**

- Alice crée le fichier : `nano bob_public.pem`
- Bob crée le fichier : `nano alice_public.pem`

Collez le contenu reçu puis sauvegardez.

---

### Étape 5 — Calcul du secret partagé

Chaque étudiant va maintenant calculer la clé secrète commune.

**Côté Alice :**

```bash
openssl pkeyutl -derive \
  -inkey alice_private.pem \
  -peerkey bob_public.pem \
  -out alice_shared.bin
```

**Côté Bob :**

```bash
openssl pkeyutl -derive \
  -inkey bob_private.pem \
  -peerkey alice_public.pem \
  -out bob_shared.bin
```

---

### Étape 6 — Vérification du secret

Nous allons comparer les empreintes SHA-256.

| Alice | Bob |
|---|---|
| `sha256sum alice_shared.bin` | `sha256sum bob_shared.bin` |

{: .important }
> **Résultat attendu :** Les deux valeurs doivent être **exactement identiques**.

---

### Questions

Répondez brièvement aux questions suivantes.

1. Quels fichiers ont été échangés entre Alice et Bob ?
2. Pourquoi les clés privées ne doivent-elles jamais être partagées ?
3. Un attaquant qui intercepte les clés publiques peut-il retrouver la clé finale ?
4. Dans les protocoles réels (HTTPS, VPN), à quoi sert la clé secrète Diffie-Hellman ?

---

## Exercice 2 : Pour aller plus loin — ECDH (Courbes elliptiques)

{: .d-inline-block }
À faire en autonomie
{: .label .label-blue }

Utiliser une version moderne de Diffie-Hellman basée sur les **courbes elliptiques** (ECDH).

```bash
openssl genpkey -algorithm X25519 -out private.pem
```

{: .note }
Cette méthode est : plus rapide, plus sécurisée, et utilisée dans **TLS 1.3**.

---

## L'enveloppe numérique

Dans la pratique, on utilise souvent :
- Le **chiffrement asymétrique** pour envoyer la clé
- Le **chiffrement symétrique** pour les données

**Pourquoi ?** — La cryptographie asymétrique est trop lente pour chiffrer de gros volumes.

**Processus :**

1. Le client génère une clé symétrique (AES)
2. Il la chiffre avec la clé publique du serveur
3. Le serveur la déchiffre avec sa clé privée

Ensuite : communication symétrique rapide.

---

## 2. Accès distant sécurisé

### 2.1 Telnet

Telnet permet d'administrer un serveur à distance et d'envoyer des commandes.

{: .warning }
> **Problème :** aucun chiffrement — tout passe **en texte clair**.

### 2.2 SSH — Secure Shell

SSH apporte : **chiffrement, authentification, intégrité**. Les données sont illisibles sur le réseau.

---

## Exercice 3 : Telnet vs SSH + Wireshark

{: .d-inline-block }
Durée estimée : 30 min
{: .label .label-yellow }

{: .highlight }
> **Linux requis (VM).** Cet exercice nécessite Wireshark et un accès réseau local.

### Étape 1 — Vérifier si Wireshark est installé

```bash
wireshark --version
```

Si Wireshark n'est **pas** installé :

```bash
sudo apt update
sudo apt install -y wireshark
sudo usermod -aG wireshark $USER
```

{: .note }
Il faut se déconnecter / reconnecter pour activer le groupe.

---

### Étape 2 — Installer les serveurs Telnet et SSH

**Installer un serveur Telnet (non sécurisé) :**

```bash
sudo apt install -y telnetd
sudo systemctl status inetutils-inetd
```

**Installer OpenSSH Server (sécurisé) :**

```bash
sudo apt install -y openssh-server
sudo systemctl status ssh
```

---

### Étape 3 — Préparer un utilisateur de test

```bash
sudo adduser etu
```

Mot de passe simple pour l'exercice : `user1234`

---

### Étape 4 — Capture du trafic Telnet (mot de passe en clair)

1. Ouvrir Wireshark : `wireshark &`
2. Sélectionner l'interface réseau **ens33**
3. Démarrer la capture
4. Dans un autre terminal, lancer Telnet vers soi-même :

```bash
telnet 127.0.0.1
```

Identifiants :
```
login: etu
password: user1234
```

Faites une courte commande :
```bash
echo test
exit
```

5. Arrêter la capture dans Wireshark
6. Filtrer : `telnet`

**Ce que vous devez observer :**
- Le nom d'utilisateur apparaît en clair.
- Le mot de passe apparaît en clair, caractère par caractère.
- Chaque touche pressée traverse le réseau sans chiffrement.

---

### Étape 5 — Capture du trafic SSH

1. Redémarrer la capture Wireshark
2. Se connecter en SSH :

```bash
ssh etu@127.0.0.1
```

Tapez le mot de passe : `user1234`

Faites une commande courte :
```bash
hostname
exit
```

3. Filtrer le trafic SSH dans Wireshark : `ssh`

**Ce que vous devez observer :**
- Le contenu des paquets est **illisible**.
- Aucune information sur le login, ni le mot de passe.
- Le trafic est marqué `Encrypted packet`.

### Questions

1. Quelle différence observe-t-on entre les paquets Telnet et SSH dans Wireshark ?
2. Pourquoi peut-on voir le mot de passe en Telnet mais pas en SSH ?
3. Pourquoi Telnet ne doit-il plus jamais être utilisé sur un vrai réseau ?

---

## 4. Infrastructure à Clés Publiques (PKI)

{: .highlight }
> **Problème :** Comment être sûr que la clé publique du serveur est **authentique** ?
>
> **Solution :** Les certificats numériques.

### 4.1 PKI — Public Key Infrastructure

Une PKI contient :
- Des **autorités de certification**
- Des **certificats**
- Des **mécanismes de validation**

### 4.2 Autorité de certification (CA)

Une CA vérifie l'identité d'un site et signe son certificat.

**Exemples de CA reconnues :**
- DigiCert
- GlobalSign
- Let's Encrypt

### 4.3 Chaîne de confiance

```
Root CA
  ↓
Intermediate CA
  ↓
Certificat du site
```

Le navigateur :
1. Vérifie la signature
2. Remonte jusqu'au Root CA

Si le Root CA est dans le système → **confiance accordée**.

---

## 5. TLS Handshake

Lorsqu'on ouvre `https://google.com`, une négociation démarre.

**Étapes simplifiées :**

| # | Message | Contenu |
|---|---|---|
| 1 | **Client Hello** | Version TLS proposée, algorithmes supportés |
| 2 | **Server Hello** | Certificat, algorithme choisi |
| 3 | **Vérification du certificat** | Signature CA, validité |
| 4 | **Échange de clé** | Diffie-Hellman ou RSA |
| 5 | **Communication chiffrée** | Données envoyées avec AES |

---

## 6. Analyse TLS dans Wireshark

1. Lancer Wireshark
2. Accéder à : `https://epec.be`
3. Filtrer : `tls`
4. Observer les messages :
   - **Client Hello**
   - **Server Hello**
   - **Certificate**
   - **Key Exchange**

**Ce qu'il faut comprendre :**
- Le navigateur vérifie le certificat
- Il négocie un algorithme
- Il crée une clé symétrique
- Il chiffre la communication

---

## 7. CSR — Certificate Signing Request

Lorsqu'un serveur veut un certificat, il génère une **CSR**.

**Une CSR contient :**
- Nom du domaine
- Clé publique
- Informations sur l'organisation

Elle est envoyée à la CA, qui :
1. Vérifie l'identité
2. Signe le certificat

---

## Exercice 4 : Voir les certificats HTTPS dans le navigateur

{: .d-inline-block }
Durée estimée : 20 min
{: .label .label-green }

### Voir le certificat dans le navigateur

**Sur Chrome / Edge :**
1. Aller sur un site HTTPS : `https://ephec.be`
2. Cliquer sur le cadenas 🔒 dans la barre d'adresse
3. Cliquer sur *Connection is secure* / *Connexion sécurisée*
4. Cliquer sur *Certificate is valid* / *Certificat*

S'affiche :
- Certificat serveur
- Certificat intermédiaire
- Root CA
- Validité
- Algorithme de signature (RSA / ECDSA)
- Clé publique
- Extensions (SAN, Key Usage, etc.)

**Sur Firefox :**
Cadenas → *Connexion sécurisée* → *Plus d'informations* → *Voir le certificat*

---

### Étapes à suivre

**Étape 1 — Ouvrir le site**
- Ouvrir un navigateur (Firefox ou Chrome)
- Aller sur : `https://www.ephec.be`

**Étape 2 — Voir le certificat**

Firefox :
1. Cliquer sur le cadenas → *Connexion sécurisée*
2. Cliquer sur *Plus d'informations* → *Afficher le certificat*

Chrome :
1. Cadenas → *Connection is secure* → *Certificate is valid*

**Étape 3 — Identifier les informations importantes**

Relevez :
- **Subject** (le site concerné) → doit contenir `www.ephec.be`
- **Issuer** (l'autorité qui signe) → typiquement GlobalSign, Sectigo, Let's Encrypt…
- **Validité** → dates *Not Before* / *Not After*
- **Chaîne de certificats** → Root CA → Intermediate CA → `www.ephec.be`

**Étape 4 — Vérifier la chaîne de confiance**

Questions à répondre :
1. Pourquoi le navigateur fait-il confiance à la Root CA ?
2. Que se passe-t-il si l'intermédiaire manque ?
3. Pourquoi le certificat serveur n'est-il pas autosigné ?

---

### Exercice A — Trouver la chaîne PKI d'un site

1. Quelle est la Root CA ?
2. Quelle est la CA intermédiaire ?
3. Quel est le Common Name (CN) du serveur ?
4. Quelle est la suite cryptographique utilisée ? *(dans Chrome : F12 → Security)*

### Exercice B — Voir si le site est en TLS 1.2 ou 1.3

Afficher les infos de sécurité dans les DevTools :

**Chrome → F12 → onglet Security**

On voit :
- TLS version : TLS 1.3 ou TLS 1.2
- Cipher suite
- Key exchange (X25519 / ECDHE)
- Certificat

---

## TLS 1.2 / TLS 1.3 — Handshake simplifié

### Comparaison des handshakes

| TLS 1.2 | TLS 1.3 |
|---|---|
| ClientHello | ClientHello |
| ServerHello | ServerHello |
| Certificat du serveur | *(inclus dans ServerHello chiffré)* |
| Échange de clés | — |
| Chiffrement activé | Chiffrement activé (plus rapide) |

### Questions

1. Pourquoi TLS 1.3 est-il plus rapide ?
2. Pourquoi TLS 1.3 est-il plus sécurisé ?
3. Pourquoi le certificat n'est-il pas envoyé en clair dans TLS 1.3 ?

---

## Wireshark — Analyse d'une connexion HTTPS

### Étapes à suivre (Ubuntu)

**Étape 1 — Lancer Wireshark**

```bash
wireshark &
```

**Étape 2 — Filtrer le trafic**

Dans la barre de filtre : `tls`

**Étape 3 — Accéder au site**

Dans le navigateur : `https://www.ephec.be`

**Étape 4 — Identifier les messages**

Trouvez dans Wireshark :

- **ClientHello**
  - Versions supportées
  - Cipher suites proposées
  - Extension SNI (nom du site demandé)
- **ServerHello**
  - Version choisie
  - Cipher suite retenue
- **Certificate**
  - Certificat du serveur
  - Chaîne de certificats

**Étape 5 — Vérifier la version TLS**

Dans le ClientHello → extension `supported_versions` → vérifier si TLS 1.3 est proposé.

Dans le ServerHello → version choisie.

---

## Windows + Active Directory : Les autorités racines

### Étape 1 — Ouvrir la console des certificats

```
Win + R → certmgr.msc
```

### Étape 2 — Trouver les autorités racines

Dans la console :
- *Trusted Root Certification Authorities*
- *Intermediate Certification Authorities*

**Questions :**
1. Pourquoi Windows possède-t-il déjà des Root CA ?
2. Pourquoi l'utilisateur ne doit-il rien configurer pour HTTPS ?

### Étape 3 — Vérifier le certificat de www.ephec.be

1. Ouvrir le navigateur
2. Afficher le certificat
3. Vérifier que l'Issuer est bien présent dans les autorités du système
