---
layout: default
title: Hachage & Intégrité
order: 4
description: Hash, Sel, Rainbow tables
nav_order: 4
published: true
---

# Séance 4 : Fonctions de Hachage

{: .no_toc }

## Introduction

Recrues, l'intégrité est le deuxième pilier de la sécurité (CIA : Confidentialité, Intégrité, Disponibilité). 
Le **hachage** (hashing) ne sert pas à cacher un message, mais à lui donner une **empreinte numérique** unique. Si le message change, ne serait-ce que d'un minuscule point, l'empreinte change totalement.

{: .note }
**Analogie :** Une fonction de hachage est comme un mixeur. Vous pouvez y mettre des fruits pour faire un smoothie (le hash), mais vous ne pourrez jamais retrouver les fruits entiers à partir du smoothie.

**Outils requis :**
- Terminal Linux
- Outils `md5sum`, `sha256sum`
- [CyberChef](https://gchq.github.io/CyberChef/)

---

## Exercice 1 <span class="label label-green">À faire en autonomie</span> : L'Effet Avalanche

{: .d-inline-block }
Durée estimée : 10 min
{: .label .label-green }

### Contexte
> Une bonne fonction de hachage doit être sensible au moindre changement. C'est ce qu'on appelle l'effet avalanche.

1.  **Générez un hash simple :**
    ```bash
    echo "Agent 007" | sha256sum
    ```
2.  **Provoquez l'avalanche :**
    Changez juste un caractère (ex: "agent 007" avec un 'a' minuscule) et comparez le résultat.
    ```bash
    echo "agent 007" | sha256sum
    ```

### Questions d'analyse
*   Les deux empreintes se ressemblent-elles ?
*   Est-il possible de deviner le message original en regardant simplement le hash ?
*   Pourquoi est-ce utile pour vérifier que personne n'a modifié un fichier pendant son téléchargement ?

---

## Exercice 2 <span class="label label-green">À faire en autonomie</span> : Casser un Hash (Rainbow Tables)

{: .d-inline-block }
Durée estimée : 15 min
{: .label .label-green }

### Contexte
> Le hachage est "à sens unique" (on ne peut pas revenir en arrière mathématiquement). Cependant, si un attaquant possède une liste de milliards de mots de passe et leurs hashs correspondants (une **Rainbow Table**), il peut retrouver votre mot de passe en une fraction de seconde.

1.  **Le défi :** On vous a transmis ce hash MD5 intercepté sur un vieux serveur : `01a2da07bf36766155f48fc670d53fe8`
2.  **L'attaque :**
    *   Allez sur [CyberChef](https://gchq.github.io/CyberChef/).
    *   Cherchez si une opération peut vous aider, ou utilisez un service en ligne comme [CrackStation](https://crackstation.net/).
3.  **Analyse :** Essayez de faire la même chose avec un hash SHA-256 d'une phrase très longue et complexe que vous inventez.

### Questions d'analyse
*   Quel était le mot de passe caché derrière le hash MD5 ?
*   Pourquoi le site CrackStation a-t-il trouvé le premier mais pas le second ?
*   {: .important } MD5 est-il encore considéré comme sûr aujourd'hui ? Pourquoi ?

---

## Exercice 3 <span class="label label-green">À faire en autonomie</span> : Le Sel (Salt) — La contre-mesure

{: .d-inline-block }
Durée estimée : 10 min
{: .label .label-green }

### Contexte
> Pour empêcher l'utilisation des Rainbow Tables, les administrateurs ajoutent un **"Sel"** (une chaîne de caractères aléatoire) au mot de passe avant de le hacher.
> `Hash(MotDePasse + Sel)`

### Mission 3.A : Réflexion
Deux utilisateurs, Alice et Bob, utilisent le même mot de passe : `123456`.
1.  Sans sel, leurs hashs dans la base de données seront **identiques**.
2.  Si on ajoute le sel `alice_78` pour Alice et `bob_22` pour Bob :
    *   Alice : `sha256("123456" + "alice_78")`
    *   Bob : `sha256("123456" + "bob_22")`

### Questions d'analyse
*   Les hashs finaux seront-ils identiques ou différents ?
*   Pourquoi cela rend-il le travail d'un attaquant beaucoup plus difficile ?

---

## Exercice 4 <span class="label label-green">À faire en autonomie</span> : Vérification d'Intégrité (Checksum)

{: .d-inline-block }
Durée estimée : 10 min
{: .label .label-green }

### Contexte
> Lorsque vous téléchargez un logiciel sensible (comme une ISO Linux ou un outil de sécurité), le site fournit souvent un "Checksum" (une empreinte SHA256).

1.  **Simulez un téléchargement :**
    ```bash
    echo "Ceci est un logiciel de sécurité légitime" > logiciel.exe
    sha256sum logiciel.exe > checksum.txt
    ```
2.  **L'attaque :** Modifiez le contenu de `logiciel.exe` (ajoutez un espace, une lettre...) pour simuler l'injection d'un virus.
3.  **La vérification :**
    ```bash
    sha256sum -c checksum.txt
    ```

### Questions d'analyse
*   Quel message affiche le terminal ?
*   Pourquoi est-il important de récupérer le checksum sur un canal différent (ex: HTTPS) de celui du téléchargement du fichier ?

---

## Exercice 5 <span class="label label-green">À faire en autonomie</span> : Déduplication avec `fdupes`

{: .d-inline-block }
Durée estimée : 10 min
{: .label .label-green }

### Contexte
> Le hachage est aussi utilisé pour gagner de la place. Si deux fichiers ont le même hash, ils sont identiques, quel que soit leur nom.

1.  **Installation :** `sudo apt install fdupes -y`
2.  **Préparez le terrain :**
    ```bash
    echo "Identique" > fichier1.txt
    echo "Identique" > fichier2.txt
    echo "Différent" > fichier3.txt
    ```
3.  **Lancez le scan :** `fdupes .`

### Questions d'analyse
*   Quels fichiers l'outil a-t-il regroupés ?
*   Comment l'outil sait-il qu'ils sont identiques sans comparer chaque lettre une par une ?

---

## Pour aller plus loin : Signature Numérique (GPG)

{: .d-inline-block }
Durée estimée : 5 min
{: .label .label-green }

> Le hachage est la base de la **signature GPG**. On hache le message, puis on chiffre ce hash avec sa clé privée (vue au TP3). C'est ce qui garantit que le message n'a pas été modifié ET qu'il vient bien de vous.
