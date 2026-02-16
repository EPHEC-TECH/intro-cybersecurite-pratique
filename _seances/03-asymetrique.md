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

**Analogie :** La clé publique est un **cadenas ouvert** que vous distribuez. N'importe qui peut l'utiliser pour fermer une boîte contenant un message. Seule votre clé privée peut ouvrir ce cadenas.

> **Le principe mathématique (RSA en 30 secondes)**
>
> RSA repose sur une opération facile lorsque effectué dans un sens, mais quasi impossible dans lorsqu'on essaye de l'effectuer dans l'autre sens:
> - **Facile :** Multiplier deux grands nombres premiers → `P × Q = N`
> - **Beaucoup plus compliqué :** Retrouver `P` et `Q` à partir de `N` (c'est la **factorisation**)
>
> La clé publique contient `N` (le produit) et un exposant `e`. La clé privée contient `P`, `Q` et d'autres valeurs dérivées. Tant que personne ne peut factoriser `N`, la clé privée reste secrète.
>
> C'est cette **asymétrie de difficulté** qui donne son nom au chiffrement asymétrique.

**Outils requis :**
- Un terminal Linux (VM ou WSL)
- **OpenSSL** (déjà installé sur la plupart des distributions Linux)

> **Pourquoi Teams ? Et pourquoi en public ?**
>
> Durant ce TP, vous échangerez des fichiers via le canal **Teams du cours** (pas en message privé). C'est volontaire : la force du chiffrement asymétrique est justement que **la sécurité ne repose pas sur le secret du canal de communication**. Vous pouvez publier votre clé publique sur un panneau d'affichage en pleine rue — ça ne compromet rien.
>
> **Convention de nommage :** Pour éviter la confusion quand 20 personnes partagent des fichiers, **préfixez tous vos fichiers avec votre prénom** (ou pseudo). Par exemple : `alex_cle.pub`, `alex_message.enc`, `alex_signature.bin`. Dans les commandes ci-dessous, remplacez `prenom` par le vôtre.

---

## Mission 1 : Génération de la paire de clés

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

## Mission 2 : Chiffrement et Secret Partagé

{: .d-inline-block }
Durée : 15-20 min
{: .label .label-yellow }

### Contexte

> Le but de l'asymétrique est de pouvoir envoyer un secret à quelqu'un **sans avoir besoin de se rencontrer au préalable**. Votre voisin(e) veut vous envoyer un message secret.

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
*   Pourquoi est-il crucial de ne jamais partager le fichier `.priv` ?
*   Comparez avec le chiffrement symétrique du TP1 : quel est le problème de l'échange de clé avec un chiffrement symétrique que l'asymétrique résout ici ?

---

## Exercice : La Limite de RSA

{: .d-inline-block }
Durée : 5 min
{: .label .label-red }

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

## Mission 3 : La Signature Numérique

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

## Mission 4 : L'Attaque — Casser une clé RSA faible

{: .d-inline-block }
Durée : 20-30 min
{: .label .label-yellow }

### Contexte

> La sécurité de RSA repose sur un principe simple : **multiplier deux grands nombres premiers est facile, mais factoriser le résultat est extrêmement difficile**. Si les nombres premiers choisis sont trop petits ou mal choisis, RSA s'effondre.

{% comment %} CRITIQUE MAJEURE : Cette mission est la plus faible du TP dans sa version actuelle.
Voici les problèmes :

1. Cas 1 : Le modulus hex `00:c3:a3:d5:b0:14:f3:95:6b` fait seulement 8 octets (64 bits).
   C'est beaucoup trop petit pour être pris au sérieux et il n'y a pas de step-by-step
   pour convertir le hex en décimal. Les étudiants seront perdus.

2. Cas 2 : L'image Docker `rsactftool/rsactftool` n'existe pas sur Docker Hub
   (on a vérifié). Et surtout, il manque les FICHIERS d'exercice : pas de
   `cle_faible.pub` ni de `secret.enc` fournis. L'exercice est infaisable en l'état.

PROPOSITION : Remplacer par un exercice concret et auto-suffisant.
Ci-dessous, cette mission est réécrite en deux approches.
On choisira celle qui convient le mieux. {% endcomment %}

---

### Étape 1 : Générer une clé volontairement faible

Générons une clé RSA ridiculement petite (512 bits — interdite en production depuis des années) :

```bash
openssl genrsa -out cle_faible.priv 512
openssl rsa -in cle_faible.priv -pubout -out cle_faible.pub
```

Chiffrons un secret avec cette clé faible :
```bash
echo "FLAG{rsa_est_casse}" > flag.txt
openssl pkeyutl -encrypt -pubin -inkey cle_faible.pub -in flag.txt -out flag.enc
```

### Étape 2 : Extraire le modulus

Inspectez la clé publique pour trouver le **modulus** `N` :
```bash
openssl rsa -pubin -in cle_faible.pub -text -noout
```

Le modulus s'affiche en hexadécimal. **Attention :** si le premier octet est `00`, ignorez-le (c'est un marqueur de signe pour s'assurer que le nombre est positif).

Convertissez-le en décimal avec Python :
```bash
# Supprimez les ":" et les éventuels "00" en tête de ligne
python3 -c "print(int('VOTRE_HEX_ICI', 16))"
```

> **Note :** Le script ci-dessous effectue un déchiffrement RSA dit "Textbook" (mathématique pur). Comme OpenSSL utilise par défaut un **padding PKCS#1 v1.5** pour renforcer la sécurité, le résultat brut contiendra des octets de remplissage avant votre message.

{% comment %} SUGGESTION: On pourrait fournir le modulus directement pour éviter la
galère de conversion hex → décimal. Ou fournir un script Python tout fait
qui extrait N et e automatiquement. Exemple :
python3 -c "
from Crypto.PublicKey import RSA
key = RSA.import_key(open('cle_faible.pub').read())
print(f'N = {key.n}')
print(f'e = {key.e}')
"
Mais ça nécessite pycryptodome (pip install pycryptodome).
À voir si l'on veut ajouter cette dépendance. {% endcomment %}

### Étape 3 : Factoriser N

Allez sur [FactorDB.com](http://factordb.com) et collez le nombre décimal `N`.

*   Si le site affiche la factorisation `N = P × Q`, **la clé est cassée**.
*   Notez les deux facteurs `P` et `Q`.

### Étape 4 : Reconstruire la clé privée et déchiffrer

{% comment %} CRITIQUE : C'est ici que ça coince. Reconstruire manuellement la clé privée
à partir de P, Q et e demande du code Python (calculer phi, puis d = e^-1 mod phi,
puis reconstruire un fichier PEM). C'est faisable mais complexe pour des débutants.

DEUX OPTIONS :
A) Fournir un script Python prêt à l'emploi (que l'étudiant utilise comme une "boîte noire")
B) Utiliser RsaCtfTool (mais il faut l'installer, pas de Docker)

L'option A semble plus adaptée au niveau intro. Voici le script : {% endcomment %}

Si vous avez trouvé `P` et `Q`, utilisez ce script Python pour reconstruire la clé privée et déchiffrer le message :

```bash
pip install pycryptodome
```

```python
# fichier: crack_rsa.py
from Crypto.PublicKey import RSA
import math

# Remplacez par vos valeurs
p = VOTRE_P
q = VOTRE_Q
e = 65537

n = p * q
phi = (p - 1) * (q - 1)
d = pow(e, -1, phi)

key = RSA.construct((n, e, d, p, q))

with open("flag.enc", "rb") as f:
    ciphertext = f.read()

plaintext = pow(int.from_bytes(ciphertext, 'big'), d, n)
# Pour une clé de 512 bits, le bloc déchiffré fait 64 octets
decrypted_block = plaintext.to_bytes(64, 'big')
# On affiche le bloc brut pour voir le padding PKCS#1 v1.5 (00 02 ... 00 [MESSAGE])
print(f"Bloc brut : {decrypted_block.hex()}")
print(f"Message probable : {decrypted_block.split(b'\\x00')[-1].decode()}")
```

```bash
python3 crack_rsa.py
```

{% comment %} NOTE : Le script ci-dessus est volontairement simplifié.
Pour une version plus robuste (qui gère le padding PKCS#1), il faudrait
utiliser PKCS1_v1_5.new(key).decrypt(). Mais pour une clé de 512 bits
générée par openssl, le script devrait fonctionner.

ALTERNATIVE : Si l'on ne veut pas de Python, on peut installer RsaCtfTool
directement (sans Docker) :
  git clone https://github.com/RsaCtfTool/RsaCtfTool.git
  cd RsaCtfTool && pip install -r requirements.txt
  python3 RsaCtfTool.py --publickey ../cle_faible.pub --uncipherfile ../flag.enc
C'est plus "hacker" mais ajoute une dépendance lourde. {% endcomment %}

### Questions d'analyse
*   Pourquoi une clé de 512 bits est-elle dangereuse alors qu'une clé de 2048 bits est considérée comme sûre ?
*   Le site FactorDB connaissait-il déjà la factorisation, ou l'a-t-il calculée ? Qu'est-ce que cela implique ?
*   En 1999, une clé RSA de 512 bits a été cassée en 7 mois par des chercheurs. Aujourd'hui, cela prend quelques secondes. Que dit cela sur la durée de vie des standards de sécurité ?

---

## Pour aller plus loin (Bonus)

{: .d-inline-block }
Optionnel
{: .label .label-green }

{% comment %} CRITIQUE : La section bonus actuelle est trop mince (2 bullet points sans
contexte). Elle est étoffée ci-dessous avec des pistes concrètes.
On peut garder ce qui est pertinent et supprimer le reste. {% endcomment %}

*   **Vos clés SSH :** Regardez dans votre dossier `~/.ssh/`. Si vous avez déjà utilisé SSH, vous y trouverez vos paires de clés asymétriques (`id_rsa` / `id_rsa.pub` ou `id_ed25519` / `id_ed25519.pub`). C'est exactement le même principe que ce TP !
*   **Limitation de RSA :** Essayez de chiffrer un fichier de plus de 245 octets avec votre clé RSA 2048 bits. Que se passe-t-il ? Pourquoi en pratique, on utilise RSA pour chiffrer une **clé symétrique** (AES), et c'est AES qui chiffre les données ?
*   **CryptoHack :** Si vous voulez vous entraîner sur des challenges RSA progressifs (du débutant au difficile), essayez la plateforme gratuite [CryptoHack](https://cryptohack.org/challenges/rsa/).

{% comment %} SUGGESTION : Autres pistes bonus possibles :
- GPG : générer une clé GPG, signer un fichier, importer la clé d'un camarade
  et vérifier sa signature (mais ça fait un 2ème outil en plus d'OpenSSL)
- Visualisation : aller sur https://legacy.cryptool.org/en/cto/rsa-step-by-step
  pour voir RSA pas à pas avec des petits nombres
- Attaque de Wiener : fournir une clé avec un exposant privé trop petit
  et utiliser RsaCtfTool pour la casser automatiquement
{% endcomment %}
