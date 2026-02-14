---
layout: default
title: Chiffrement Asymétrique
order: 3
description: Clés publiques/privées, Signature, Attaque RSA
nav_order: 3
has_children: false
published: false
---

# Séance 3 : Chiffrement Asymétrique (RSA)

{: .no_toc }

## Introduction

Recrues, nouvelle mission.
Jusqu'ici, vous avez travaillé avec le chiffrement **symétrique** : une seule clé pour chiffrer et déchiffrer. Le problème ? Il faut trouver un moyen sûr de transmettre cette clé à l'autre personne. Sur Internet, c'est impossible — vous ne pouvez pas "rencontrer" chaque serveur web avant de lui envoyer un mot de passe.

La cryptographie **asymétrique** résout ce problème en utilisant un couple de clés :
- Une **clé publique** que vous distribuez à tout le monde.
- Une **clé privée** que vous gardez secrète.

**Analogie :** La clé publique est un **cadenas ouvert** que vous distribuez. N'importe qui peut l'utiliser pour fermer une boîte contenant un message. Seule votre clé privée peut ouvrir ce cadenas.

<!-- SUGGESTION: Si tu veux renforcer l'intuition mathématique sans entrer dans les formules,
tu pourrais ajouter un paragraphe du type :
"Le principe repose sur un problème mathématique simple à comprendre :
multiplier deux grands nombres premiers ensemble est instantané,
mais retrouver ces deux nombres à partir du résultat (factoriser) est
extrêmement long. C'est cette asymétrie qui donne son nom au chiffrement."
Je ne l'ai pas mis car c'est un choix pédagogique — peut-être trop tôt ici,
et tu pourrais préférer le garder pour la Mission 4 (attaque). -->

**Outils requis :**
- Un terminal Linux (VM ou WSL)
- **OpenSSL** (déjà installé sur la plupart des distributions Linux)

---

## Mission 1 : Génération de la paire de clés

{: .d-inline-block }
Durée : 10-15 min
{: .label .label-yellow }

### Contexte

> Pour participer à un échange sécurisé, chaque agent doit d'abord se créer son propre "cadenas" (clé publique) et sa "clé" (clé privée). Nous utilisons l'outil standard **OpenSSL**.

---

1.  **Générer la clé privée :**
    ```bash
    openssl genrsa -out ma_cle.priv 2048
    ```
2.  **Extraire la clé publique correspondante :**
    ```bash
    openssl rsa -in ma_cle.priv -pubout -out ma_cle.pub
    ```

### Questions d'analyse

*   Affichez le contenu des deux fichiers avec `cat`. À quoi ressemblent-ils ? Lequel est le plus long ?
*   Utilisez la commande suivante pour inspecter les composants mathématiques de votre clé privée :
    ```bash
    openssl rsa -in ma_cle.priv -text -noout
    ```
    Trouvez le **modulus** (noté `n`) et l'**exposant public** (noté `e`). Quelle est la valeur de `e` ?
*   Faites la même chose avec la clé publique :
    ```bash
    openssl rsa -pubin -in ma_cle.pub -text -noout
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

Échangez votre fichier `ma_cle.pub` avec votre voisin(e). Vous pouvez utiliser le canal **Teams**, un `scp`, ou un simple copier-coller du contenu.

> **Rappel :** La clé publique est faite pour être partagée. C'est le "cadenas ouvert" de l'analogie.

### Étape 2 : Chiffrement

Votre voisin écrit un court message dans `secret.txt` et le chiffre avec **votre** clé publique :
```bash
echo "Mon message secret" > secret.txt
openssl pkeyutl -encrypt -pubin -inkey ma_cle.pub -in secret.txt -out message.enc
```

<!-- NOTE: j'ai remplacé `openssl rsautl` par `openssl pkeyutl`.
rsautl est DEPRECATED depuis OpenSSL 3.0 (la version installée sur Ubuntu 22.04+).
Il fonctionne encore avec un warning, mais pkeyutl est le remplaçant officiel.
La syntaxe est quasi identique. -->

### Étape 3 : Déchiffrement

Récupérez le fichier `message.enc` et déchiffrez-le avec **votre** clé privée :
```bash
openssl pkeyutl -decrypt -inkey ma_cle.priv -in message.enc
```

### Questions d'analyse
*   Que se passe-t-il si votre voisin essaie de déchiffrer `message.enc` avec **sa propre** clé privée ?
*   Pourquoi est-il crucial de ne jamais partager le fichier `.priv` ?
*   Comparez avec le chiffrement symétrique du TP1 : quel est le problème de l'échange de clé avec un chiffrement symétrique que l'asymétrique résout ici ?

<!-- SUGGESTION: La limitation de RSA est qu'on ne peut chiffrer qu'un message
plus petit que la clé (max ~245 octets pour RSA-2048). Si un étudiant tente
de chiffrer un fichier trop gros, il aura une erreur. Tu pourrais en faire
un piège pédagogique volontaire (faire essayer un long message et demander
"que se passe-t-il ?"), ou simplement le mentionner en note. -->

---

## Mission 3 : La Signature Numérique

{: .d-inline-block }
Durée : 15-20 min
{: .label .label-yellow }

### Contexte

> La signature numérique ne sert pas à cacher un message, mais à **prouver qui l'a écrit** et à garantir qu'il **n'a pas été modifié** (intégrité + authentification).

> Le principe : on calcule un **hash** du document (son empreinte), puis on **chiffre ce hash avec la clé privée**. N'importe qui peut vérifier en déchiffrant avec la clé publique et en comparant le hash.

---

1.  **Signer un document :**
    ```bash
    echo "Ceci est un document officiel" > document.txt
    openssl dgst -sha256 -sign ma_cle.priv -out signature.bin document.txt
    ```
2.  **Vérifier la signature :**
    Partagez le `document.txt`, la `signature.bin` et votre `ma_cle.pub` à votre voisin(e). Il/elle vérifie avec :
    ```bash
    openssl dgst -sha256 -verify ma_cle.pub -signature signature.bin document.txt
    ```
    Le résultat doit afficher `Verified OK`.

### Défi Hacker

> Modifiez **un seul caractère** dans le fichier `document.txt` (avec `nano` ou `echo`). Relancez la commande de vérification.

*   Que se passe-t-il ?
*   Pourquoi ce mécanisme est-il vital pour la sécurité des mises à jour logicielles ? (Pensez : que se passerait-il si quelqu'un modifiait un fichier `.exe` que vous téléchargez ?)

<!-- SUGGESTION: Tu pourrais ajouter un mini-exercice "à l'envers" où un étudiant
signe un document et l'envoie à son voisin. Le voisin modifie le document
et tente de vérifier → échec. Puis le voisin signe avec SA propre clé → ça passe,
mais ce n'est plus la signature de l'auteur original. Ça illustre bien
l'authentification en plus de l'intégrité. -->

---

## Mission 4 : L'Attaque — Casser une clé RSA faible

{: .d-inline-block }
Durée : 20-30 min
{: .label .label-yellow }

### Contexte

> La sécurité de RSA repose sur un principe simple : **multiplier deux grands nombres premiers est facile, mais factoriser le résultat est extrêmement difficile**. Si les nombres premiers choisis sont trop petits ou mal choisis, RSA s'effondre.

<!-- CRITIQUE MAJEURE : Cette mission est la plus faible du TP dans sa version actuelle.
Voici les problèmes :

1. Cas 1 : Le modulus hex `00:c3:a3:d5:b0:14:f3:95:6b` fait seulement 8 octets (64 bits).
   C'est beaucoup trop petit pour être pris au sérieux et il n'y a pas de step-by-step
   pour convertir le hex en décimal. Les étudiants seront perdus.

2. Cas 2 : L'image Docker `rsactftool/rsactftool` n'existe pas sur Docker Hub
   (j'ai vérifié). Et surtout, il manque les FICHIERS d'exercice : pas de
   `cle_faible.pub` ni de `secret.enc` fournis. L'exercice est infaisable en l'état.

PROPOSITION : Remplacer par un exercice concret et auto-suffisant.
Ci-dessous, j'ai réécrit cette mission en deux approches.
Tu choisis celle qui te convient le mieux. -->

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

Le modulus s'affiche en hexadécimal. Convertissez-le en décimal avec Python :
```bash
python3 -c "print(int('COPIEZ_LE_HEX_ICI_SANS_LES_DEUX_POINTS', 16))"
```

<!-- SUGGESTION: Tu pourrais fournir le modulus directement pour éviter la
galère de conversion hex → décimal. Ou fournir un script Python tout fait
qui extrait N et e automatiquement. Exemple :
python3 -c "
from Crypto.PublicKey import RSA
key = RSA.import_key(open('cle_faible.pub').read())
print(f'N = {key.n}')
print(f'e = {key.e}')
"
Mais ça nécessite pycryptodome (pip install pycryptodome).
À toi de voir si tu veux ajouter cette dépendance. -->

### Étape 3 : Factoriser N

Allez sur [FactorDB.com](http://factordb.com) et collez le nombre décimal `N`.

*   Si le site affiche la factorisation `N = P × Q`, **la clé est cassée**.
*   Notez les deux facteurs `P` et `Q`.

### Étape 4 : Reconstruire la clé privée et déchiffrer

<!-- CRITIQUE : C'est ici que ça coince. Reconstruire manuellement la clé privée
à partir de P, Q et e demande du code Python (calculer phi, puis d = e^-1 mod phi,
puis reconstruire un fichier PEM). C'est faisable mais complexe pour des débutants.

DEUX OPTIONS :
A) Fournir un script Python prêt à l'emploi (que l'étudiant utilise comme une "boîte noire")
B) Utiliser RsaCtfTool (mais il faut l'installer, pas de Docker)

Option A me semble plus adaptée au niveau intro. Voici le script : -->

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
print(plaintext.to_bytes(256, 'big').strip(b'\x00').decode())
```

```bash
python3 crack_rsa.py
```

<!-- NOTE : Le script ci-dessus est volontairement simplifié.
Pour une version plus robuste (qui gère le padding PKCS#1), il faudrait
utiliser PKCS1_v1_5.new(key).decrypt(). Mais pour une clé de 512 bits
générée par openssl, le script devrait fonctionner.

ALTERNATIVE : Si tu ne veux pas de Python, tu peux installer RsaCtfTool
directement (sans Docker) :
  git clone https://github.com/RsaCtfTool/RsaCtfTool.git
  cd RsaCtfTool && pip install -r requirements.txt
  python3 RsaCtfTool.py --publickey ../cle_faible.pub --uncipherfile ../flag.enc
C'est plus "hacker" mais ajoute une dépendance lourde. -->

### Questions d'analyse
*   Pourquoi une clé de 512 bits est-elle dangereuse alors qu'une clé de 2048 bits est considérée comme sûre ?
*   Le site FactorDB connaissait-il déjà la factorisation, ou l'a-t-il calculée ? Qu'est-ce que cela implique ?
*   En 1999, une clé RSA de 512 bits a été cassée en 7 mois par des chercheurs. Aujourd'hui, cela prend quelques secondes. Que dit cela sur la durée de vie des standards de sécurité ?

---

## Pour aller plus loin (Bonus)

{: .d-inline-block }
Optionnel
{: .label .label-green }

<!-- CRITIQUE : La section bonus actuelle est trop mince (2 bullet points sans
contexte). Je l'ai étoffée ci-dessous avec des pistes concrètes.
Tu peux garder ce qui t'intéresse et supprimer le reste. -->

*   **Vos clés SSH :** Regardez dans votre dossier `~/.ssh/`. Si vous avez déjà utilisé SSH, vous y trouverez vos paires de clés asymétriques (`id_rsa` / `id_rsa.pub` ou `id_ed25519` / `id_ed25519.pub`). C'est exactement le même principe que ce TP !
*   **Limitation de RSA :** Essayez de chiffrer un fichier de plus de 245 octets avec votre clé RSA 2048 bits. Que se passe-t-il ? Pourquoi en pratique, on utilise RSA pour chiffrer une **clé symétrique** (AES), et c'est AES qui chiffre les données ?
*   **CryptoHack :** Si vous voulez vous entraîner sur des challenges RSA progressifs (du débutant au difficile), essayez la plateforme gratuite [CryptoHack](https://cryptohack.org/challenges/rsa/).

<!-- SUGGESTION : Autres pistes bonus possibles :
- GPG : générer une clé GPG, signer un fichier, importer la clé d'un camarade
  et vérifier sa signature (mais ça fait un 2ème outil en plus d'OpenSSL)
- Visualisation : aller sur https://legacy.cryptool.org/en/cto/rsa-step-by-step
  pour voir RSA pas à pas avec des petits nombres
- Attaque de Wiener : fournir une clé avec un exposant privé trop petit
  et utiliser RsaCtfTool pour la casser automatiquement
-->
