---
layout: default
title: Chiffrement Asymétrique
order: 3
description: Clés publiques/privées, Signature, Attaque RSA
nav_order: 3
has_children: false
published: true
---

# Séance 3 : Chiffrement Asymétrique (RSA)

{: .no_toc }

## Introduction

Recrues, nouvelle mission.
Jusqu'ici, vous avez travaillé avec le chiffrement **symétrique** : une seule clé pour chiffrer et déchiffrer. Le problème ? Il faut trouver un moyen sûr de transmettre cette clé à l'autre personne. Sur Internet, c'est impossible — vous ne pouvez pas "rencontrer" chaque serveur web avant de lui envoyer un mot de passe.

La cryptographie **asymétrique** résout ce problème en utilisant une **paire de clés** :
- Une **clé publique** que vous distribuez à tout le monde.
- Une **clé privée** que vous gardez secrète.

{: .note }
**Analogie :** La clé publique est un **cadenas ouvert** que vous distribuez. N'importe qui peut l'utiliser pour fermer une boîte contenant un message. Seule votre clé privée peut ouvrir ce cadenas.

> **Le principe mathématique (RSA en 30 secondes)**
>
> RSA repose sur une opération facile lorsque effectuée dans un sens, mais quasi impossible lorsqu'on essaye de l'effectuer dans l'autre sens :
> - **Facile :** Multiplier deux grands nombres premiers → $P \times Q = N$
> - **Beaucoup plus compliqué :** Retrouver $P$ et $Q$ à partir de $N$ (c'est la **factorisation**)
>
> La clé publique contient $N$ (le produit) et un exposant $e$. La clé privée contient $P$, $Q$ et d'autres valeurs dérivées. Tant que personne ne peut factoriser $N$, la clé privée reste secrète.
>
> C'est cette **asymétrie de difficulté** qui donne son nom au chiffrement asymétrique.

**Outils requis :**
- Un terminal Linux (VM ou WSL)
- **OpenSSL** (déjà installé sur la plupart des distributions Linux)

{: .important }
> **Pourquoi Teams ? Et pourquoi en public ?**
> Durant ce TP, vous échangerez des fichiers via le canal **Teams du cours**. C'est volontaire : la force du chiffrement asymétrique est que **la sécurité ne repose pas sur le secret du canal de communication**. Vous pouvez publier votre clé publique sur un panneau d'affichage en pleine rue — ça ne compromet rien.

---

## Exercice 1 : Génération de la paire de clés

{: .d-inline-block }
Durée : 10-15 min
{: .label .label-yellow }

### Contexte
> Pour participer à un échange sécurisé, chaque agent doit d'abord se créer son propre "cadenas" (clé publique) et sa "clé" (clé privée). Nous utilisons l'outil standard **OpenSSL**.

---

1.  **Générer la clé privée (placez vous dans un dossier approprié) :**
    ```bash
    openssl genrsa -out prenom_cle.priv 2048
    ```
2.  **Extraire la clé publique correspondante :**
    ```bash
    openssl rsa -in prenom_cle.priv -pubout -out prenom_cle.pub
    ```

### Questions d'analyse
*   Affichez le contenu des deux fichiers avec `cat`. À quoi ressemblent-ils ? Lequel est le plus long ?
*   Utilisez la commande suivante pour inspecter les composants mathématiques de votre clé privée :
    ```bash
    openssl rsa -in prenom_cle.priv -text -noout
    ```
    Trouvez le **modulus** (noté `n`) et l'**exposant public** (noté `e`). Quelle est la valeur de `e` ?
*   Faites la même chose avec la clé publique :
    ```bash
    openssl rsa -pubin -in prenom_cle.pub -text -noout
    ```
    Quels éléments sont présents dans la clé publique ? Lesquels sont absents par rapport à la clé privée ? Pourquoi ?

---

## Exercice 2 : Chiffrement et Secret Partagé

{: .d-inline-block }
Durée : 15-20 min
{: .label .label-yellow }

### Contexte
> Le but de l'asymétrique est de pouvoir envoyer un secret à quelqu'un **sans avoir besoin de se rencontrer au préalable**.

---

### Étape 1 : L'échange de clés publiques

Échangez votre fichier `prenom_cle.pub` avec votre voisin (ou un autre élève avec qui vous faites l'exercice. Ce n'est pas grave si, pour une question de facilité de gestion, vous participez à plusieurs échanges).
Vous utiliserez uniquement le canal **Teams** pour vos échanges avec votre 'voisin' (vous pouvez le tagguer pour plus de simplicité).

> **Rappel :** La clé publique est faite pour être partagée. C'est le "cadenas ouvert" de l'analogie.

### Étape 2 : Chiffrement

Votre voisin écrit un court message dans `prenom_secret.txt` et le chiffre avec **votre** clé publique :
```bash
echo "Mon message secret" > prenom_secret.txt
openssl pkeyutl -encrypt -pubin -inkey prenom_cle.pub -in prenom_secret.txt -out prenom_message.enc
```

Il vous envoie le fichier `prenom_message.enc` sur **Teams**.

### Étape 3 : Déchiffrement

Récupérez le fichier `prenom_message.enc` de votre voisin et déchiffrez-le avec **votre** clé privée :
```bash
openssl pkeyutl -decrypt -inkey prenom_cle.priv -in prenom_message.enc
```

### Questions d'analyse
*   Que se passe-t-il si votre voisin essaie de déchiffrer `message.enc` avec **sa propre** clé privée ?
*    {: .warning }  Pourquoi est-il crucial de ne jamais partager le fichier `.priv` ?
*   Comparez avec le chiffrement symétrique du TP1 : quel est le problème de l'échange de clé avec un chiffrement symétrique que l'asymétrique résout ici ?

---

## Exercice : La Limite de RSA

{: .d-inline-block }
Durée : 5 min
{: .label .label-yellow }

### Contexte
> Lors de la Mission 2, vous avez chiffré un court message. Mais que se passe-t-il si le message est plus long ?

### Mission

1. Générez un fichier contenant un texte assez long (plusieurs phrases). Par exemple avec cette commande (mais vous pouvez juste copier-coller un 'long texte', tel que ce TP, dans le fichier long_message.txt) :
    ```bash
    python3 -c "print('A' * 500)" > long_message.txt
    ```
2. Tentez de le chiffrer avec votre clé publique RSA 2048 bits, comme vous l'avez fait à la Mission 2.

### Questions d'analyse
*   Quelle erreur obtenez-vous ?
*   D'après l'encart mathématique de l'introduction, pourquoi RSA ne peut-il pas chiffrer un message plus grand que la clé ?
*   En pratique, on n'utilise **jamais** RSA pour chiffrer directement des données. À la place, on chiffre une **clé symétrique** (AES -- vu au précédent TP) avec RSA, puis on chiffre les données avec AES. Pourquoi cette combinaison est-elle le meilleur des deux mondes ?

---

## Exercice 3 : La Signature Numérique

{: .d-inline-block }
Durée : 15-20 min
{: .label .label-yellow }

### Contexte

> La signature numérique ne sert pas à cacher un message, mais à **prouver qui l'a écrit** et à garantir qu'il **n'a pas été modifié** (intégrité + authentification).

> Le principe : on calcule un **hash** du document (une empreinte unique -- mais on y reviendra dans la suite du cours), puis on utilise la **clé privée** pour générer une preuve mathématique appelée **signature**. N'importe qui peut vérifier cette signature avec la **clé publique** pour s'assurer que le document provient bien de l'auteur et n'a pas été altéré.

---

1.  **Signer un document :**
    ```bash
    echo "Ceci est un document officiel: moi [pseudo/nom] affirme la chose suivante: xxxx_a_completer_xxxx " > prenom_document.txt
    openssl dgst -sha256 -sign prenom_cle.priv -out prenom_signature.bin prenom_document.txt
    ```
2.  **Vérifier la signature :**
    Partagez `prenom_document.txt`, `prenom_signature.bin` et votre `prenom_cle.pub` à votre voisin (via **Teams** toujours). Il vérifie avec :
    ```bash
    openssl dgst -sha256 -verify prenom_cle.pub -signature prenom_signature.bin prenom_document.txt
    ```
    Le résultat doit afficher `Verified OK`.

### Exercice d'application : Falsification et Usurpation

> Un message signé de votre voisin traîne sur le canal Teams. Vous allez tenter de le falsifier.

1. **Attaque sur l'intégrité :** Récupérez le `prenom_document.txt` et le `prenom_signature.bin` d'un camarade. Modifiez **un seul caractère** dans son document (avec `nano` ou `echo`). Vérifiez la signature avec sa clé publique. Que se passe-t-il ?

2. **Tentative d'usurpation :** La signature est invalide... Qu'à cela ne tienne : re-signez le document modifié avec **votre propre** clé privée et publiez le tout sur Teams (le document modifié + votre nouvelle signature). Prévenez vos camarades que vous avez "mis à jour" le message.

3. **Détection :** Vos camarades doivent vérifier ce message. Tomberont-ils dans le piège ? Comment peuvent-ils détecter la supercherie ?

### Questions d'analyse
*   Pourquoi la vérification échoue-t-elle à l'étape 1, même pour un changement minuscule ?
*   À l'étape 2, la signature est techniquement valide — mais elle prouve quoi exactement ? Est-ce que le message vient toujours de l'auteur original ?
*   Comment un destinataire peut-il se protéger contre ce type d'attaque ? (Indice : que faut-il vérifier **en plus** de la validité de la signature ?)
*   Pourquoi ce mécanisme est-il vital pour la sécurité des mises à jour logicielles ? (Pensez : que se passerait-il si quelqu'un modifiait un `.exe` que vous téléchargez ?)

---

## Exercice 4 <span class="label label-green">À faire en autonomie</span> : Le casse du siècle (RSA à la main)

{: .d-inline-block }
Durée : 15 min
{: .label .label-yellow }

### Contexte
> On vous a dit que RSA était "impossible" à casser. C'est vrai, mais seulement si les nombres premiers sont gigantesques. Si un agent utilise des nombres trop petits, n'importe qui peut retrouver sa clé privée en quelques secondes.

**Objectif :** Factoriser un modulus $N$ et reconstruire la clé privée pour lire un message intercepté.

---

### Étape 1 : L'interception
Vous avez intercepté une clé publique très faible et un message chiffré :
*   **Modulus ($N$) :** `3233`
*   **Message chiffré ($c$) :** `1317`

### Étape 2 : Le calcul
1.  **Factorisez $N$ :** Trouvez les deux nombres premiers $P$ et $Q$ tels que $P \times Q = 3233$.
    *(Indice : l'un des deux est 61. À vous de trouver l'autre !)*
2.  **Ouvrez l'outil visuel :** [RSA Calculator Tool](https://raw.githack.com/mlgarrett/rsa-calculator-tool/master/index.html) ([source GitHub](https://github.com/mlgarrett/rsa-calculator-tool)).
3.  **Reconstruisez la clé :**
    *   Entrez vos valeurs $P$ et $Q$ dans les cases.
    *   Cliquez successivement sur les boutons **calculate n**, **calculate φ**, **choose e**, puis **calculate d**.
    *   Notez les valeurs de $e$ et $d$ que l'outil a calculées.
4.  **Déchiffrez :** Entrez le ciphertext `1317` dans la case "ciphertext number" et cliquez sur **decrypt**.

### Questions d'analyse
*   Quelles sont les valeurs de $e$ et $d$ calculées par l'outil ?
*   Quel était le message secret caché derrière le nombre `1317` ? *(Indice : pensez au code ASCII)*
*   Pourquoi est-ce que cette attaque devient impossible si $N$ possède 600 chiffres au lieu de 4 ?

---

## Exercice 5: Le secret de la vitesse (Le Chiffrement Hybride)

{: .d-inline-block }
Durée : 15 min
{: .label .label-yellow }

### Contexte
> Vous l'avez vu : RSA ne peut pas chiffrer de longs messages. De plus, il est environ 1000 fois plus lent que l'AES. Alors, comment fait Netflix pour vous envoyer des films entiers de manière sécurisée ?
> Ils utilisent le **Chiffrement Hybride** (ou Enveloppe Numérique).

**Le concept :** On utilise RSA (lent mais pratique) pour protéger une clé AES (rapide mais difficile à partager).

---

### Étape 1 : L'envoi (vous)
Vous allez simuler l'envoi d'un fichier "lourd" à votre voisin.

1.  **Préparez le colis (AES) :**
    Générez une clé symétrique au hasard et chiffrez votre fichier avec AES :
    ```bash
    # On crée une clé AES de 256 bits
    openssl rand -hex 32 > prenom_cle_aes.txt

    # On chiffre le fichier lourd avec cette clé
    openssl enc -aes-256-cbc -pbkdf2 -in long_message.txt -out prenom_colis.enc -pass file:./prenom_cle_aes.txt
    ```

2.  **Préparez l'enveloppe (RSA) :**
    Maintenant, chiffrez **uniquement la petite clé AES** avec la clé publique de votre voisin :
    ```bash
    openssl pkeyutl -encrypt -pubin -inkey voisin_cle.pub -in prenom_cle_aes.txt -out prenom_enveloppe.enc
    ```

3.  **L'envoi :**
    Envoyez les deux fichiers (`prenom_colis.enc` et `prenom_enveloppe.enc`) à votre voisin sur Teams.

### Étape 2 : La réception (votre voisin)

1.  **Ouvrir l'enveloppe :** Déchiffrez la clé AES avec votre clé privée :
    ```bash
    openssl pkeyutl -decrypt -inkey prenom_cle.priv -in voisin_enveloppe.enc -out cle_recue.txt
    ```

2.  **Ouvrir le colis :** Déchiffrez le fichier avec la clé AES récupérée :
    ```bash
    openssl enc -aes-256-cbc -pbkdf2 -d -in voisin_colis.enc -out message_recu.txt -pass file:./cle_recue.txt
    ```

3.  Vérifiez le contenu avec `cat message_recu.txt`.

### Questions d'analyse
*   Pourquoi cette méthode est-elle plus efficace que d'essayer de tout chiffrer en RSA ?
*   Si un pirate intercepte `prenom_colis.enc` mais n'a pas la clé privée du destinataire, peut-il retrouver le contenu ?
*   **Synthèse :** Expliquez pourquoi on dit que RSA sert de "porte-clé" pour AES.

---

## Le saviez-vous ?

### Vos clés GitHub sont publiques

Si vous avez configuré une clé SSH sur GitHub, **n'importe qui** peut la consulter à l'adresse :

```
https://github.com/VOTRE_USERNAME.keys  (à condition qu'une clé aie été créé par l'utilisateur)
```



Essayez avec votre propre compte, ou avec celui d'un camarade. Vous y verrez la clé publique SSH en clair — c'est normal et voulu, exactement comme le "cadenas ouvert" de ce TP.

#### Mini-défi (hors TP): Message secret via GitHub

{: .d-inline-block }
Optionnel
{: .label .label-green }

> Envoyez un message chiffré à un camarade **en utilisant uniquement sa clé publique GitHub** — sans qu'il ne vous ait rien transmis au préalable.

1. Récupérez la clé publique SSH de votre cible :
    ```bash
    curl https://github.com/USERNAME.keys > cible.pub
    ```
2. Cette clé est au format SSH. Convertissez-la au format PEM (compatible OpenSSL) :
    ```bash
    ssh-keygen -f cible.pub -e -m PKCS8 > cible_pkcs8.pub
    ```
3. Chiffrez votre message :
    ```bash
    echo "Ton message secret ici" > msg.txt
    openssl pkeyutl -encrypt -pubin -inkey cible_pkcs8.pub -in msg.txt -out msg.enc
    ```
4. Encodez le résultat en **base64** pour obtenir du texte lisible (et partageable via Teams, un email, ou même un post-it) :
    ```bash
    openssl base64 -in msg.enc
    ```
5. Envoyez ce texte base64 à votre cible. De son côté, il devra décoder le base64 et déchiffrer avec sa clé privée SSH. À lui de trouver comment !

### Votre carte d'identité belge aussi

Votre **eID belge** contient elle aussi des clés asymétriques, stockées directement dans la puce de la carte. Elle en contient même **trois paires** : une pour l'**authentification** (prouver votre identité en ligne), une pour la **signature numérique** (signer des documents avec valeur légale), et une pour le **chiffrement**.

Les clés privées ne quittent **jamais** la puce — elles sont générées sur la carte et y restent. Quand vous utilisez Itsme ou que vous signez un document via un lecteur de carte, c'est la puce qui effectue le calcul cryptographique en interne. Seul le résultat (la signature) sort de la carte.

Les certificats (contenant les clés publiques) sont lisibles sans code PIN par n'importe quel lecteur de carte. Par contre, contrairement à GitHub, il n'existe pas de site web public où consulter le certificat de quelqu'un.

---

## Pour aller plus loin (Hors TP)

{: .d-inline-block }
Optionnel
{: .label .label-green }

*   **Vos clés SSH :** Regardez dans votre dossier `~/.ssh/`. Si vous avez déjà utilisé SSH, vous y trouverez vos paires de clés asymétriques (`id_rsa` / `id_rsa.pub` ou `id_ed25519` / `id_ed25519.pub`). C'est exactement le même principe que ce TP !
*   **CryptoHack :** Si vous voulez vous entraîner sur des challenges RSA progressifs (du débutant au difficile), essayez la plateforme gratuite [CryptoHack](https://cryptohack.org/challenges/rsa/).
