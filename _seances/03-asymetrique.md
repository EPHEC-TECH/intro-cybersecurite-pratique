---
layout: default
title: Chiffrement Asymétrique
nav_order: 3
---

# Séance 3 : Chiffrement Asymétrique (RSA)

La cryptographie asymétrique est le moteur de la sécurité sur Internet (HTTPS, SSH, Bitcoins). Contrairement au chiffrement symétrique (une seule clé), elle utilise un couple de clés : une **clé publique** (que l'on distribue) et une **clé privée** (que l'on garde secrète).

**Analogie :** La clé publique est un **cadenas ouvert** que vous distribuez à tout le monde. N'importe qui peut l'utiliser pour fermer une boîte contenant un message. Seule votre clé privée peut ouvrir ce cadenas.

---

## Mission 1 : Génération de la paire de clés

Pour commencer, nous allons créer notre propre "cadenas" et sa "clé". Nous utilisons l'outil standard **OpenSSL**.

1.  **Générer la clé privée :**
    ```bash
    openssl genrsa -out ma_cle.priv 2048
    ```
2.  **Extraire la clé publique correspondante :**
    ```bash
    openssl rsa -in ma_cle.priv -pubout -out ma_cle.pub
    ```

### 🔍 Questions d'analyse
*   Affichez le contenu des deux fichiers avec `cat`. À quoi ressemblent-ils ?
*   Utilisez la commande suivante pour inspecter les "entrailles" mathématiques de votre clé :
    ```bash
    openssl rsa -in ma_cle.priv -text -noout
    ```
    Trouvez le **modulus** (noté `n`) et l'**exposant public** (noté `e`). Lequel de ces deux éléments se retrouve aussi dans la clé publique ? (Vérifiez avec la même commande sur `ma_cle.pub`).

---

## Mission 2 : Chiffrement et Secret Partagé

Le but de l'asymétrique est de pouvoir envoyer un secret à quelqu'un sans avoir besoin de se rencontrer au préalable.

**Le scénario :** Votre voisin(e) veut vous envoyer un message secret.
1.  **Échange :** Donnez votre fichier `ma_cle.pub` à votre voisin (via clé USB, mail, ou simple copier-coller).
2.  **Chiffrement :** Votre voisin écrit un message dans `secret.txt` et le chiffre avec **VOTRE** clé publique :
    ```bash
    openssl rsautl -encrypt -pubin -inkey ma_cle.pub -in secret.txt -out message.enc
    ```
3.  **Déchiffrement :** Récupérez le fichier `message.enc` et déchiffrez-le avec **VOTRE** clé privée :
    ```bash
    openssl rsautl -decrypt -inkey ma_cle.priv -in message.enc
    ```

### 🔍 Questions d'analyse
*   Que se passe-t-il si votre voisin essaie de déchiffrer `message.enc` avec sa propre clé privée ?
*   Pourquoi est-il crucial de ne jamais partager le fichier `.priv` ?

---

## Mission 3 : La Signature Numérique

La signature numérique ne sert pas à cacher un message, mais à **prouver qui l'a écrit** et à garantir qu'il n'a pas été modifié (intégrité).

1.  **Signer un document :**
    ```bash
    echo "Ceci est un document officiel" > document.txt
    openssl dgst -sha256 -sign ma_cle.priv -out signature.bin document.txt
    ```
2.  **Vérifier la signature :**
    Partagez le `document.txt`, la `signature.bin` et votre `ma_cle.pub`. Le destinataire vérifie avec :
    ```bash
    openssl dgst -sha256 -verify ma_cle.pub -signature signature.bin document.txt
    ```

### 🔍 Défi Hacker
Modifiez un seul caractère dans le fichier `document.txt` (utilisez `nano` ou `echo`). Relancez la commande de vérification. Que se passe-t-il ? Pourquoi est-ce vital pour la sécurité des mises à jour logicielles ?

---

## Mission 4 : L'attaque (Cryptanalyse RSA)

La sécurité de RSA repose sur la difficulté de factoriser un grand nombre $N$ en deux nombres premiers $P$ et $Q$. Si $N$ est trop petit ou mal choisi, RSA s'effondre.

### Cas 1 : La factorisation par base de données
Imaginez que vous interceptiez une clé publique dont le Modulus ($N$) est le suivant :
`00:c3:a3:d5:b0:14:f3:95:6b` (en hexadécimal).

1.  Convertissez-le en décimal (ou récupérez un $N$ plus long via une clé de 512 bits).
2.  Allez sur le site [FactorDB.com](http://factordb.com). Copiez votre nombre $N$.
3.  Si le site trouve $P$ et $Q$, vous pouvez reconstruire la clé privée et lire tous les messages.

### Cas 2 : L'outil automatisé (Docker)
Les hackers utilisent des outils comme **RsaCtfTool** pour tester automatiquement des dizaines de faiblesses.

Si vous avez une clé faible et un message chiffré, vous pouvez tenter le "tout pour le tout" :
```bash
docker run --rm -v $(pwd):/data rsactftool/rsactftool --publickey /data/cle_faible.pub --uncipher /data/secret.enc
```

---

## Pour aller plus loin (Bonus)
*   **GPG :** Essayez d'importer une clé publique depuis un serveur de clés (ex: `keys.openpgp.org`).
*   **SSH :** Regardez dans votre dossier `~/.ssh/`. Reconnaissez-vous vos paires de clés asymétriques ?
