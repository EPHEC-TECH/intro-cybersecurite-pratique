---
layout: default
title: Chiffrement symétrique
nav_order: 1
has_children: false
---

# TP 1 : Opération "Black Chamber"
{: .no_toc }

## Introduction à la Cryptographie Symétrique
{: .fs-9 }

Bienvenue, Recrues. 
Vous intégrez aujourd'hui la **Division de Sécurité Offensive**. Votre mission : comprendre comment protéger des informations critiques et, surtout, comment les attaquants brisent les protections obsolètes.

Dans ce TP, nous n'allons pas faire de mathématiques complexes. Nous allons manipuler la matière première de l'informatique : l'information.

**Outils requis :**
* [CyberChef](https://gchq.github.io/CyberChef/) (Un outil "Couteau Suisse" pour le chiffrement)
* Microsoft Teams (Canal de classe) pour l'échange de données.

---

## 1. L'Illusion de la Sécurité (Encodage)
{: .d-inline-block }
Durée : 10-15 min
{: .label .label-yellow }

Dans le monde de la cybersécurité, la première règle est de savoir distinguer ce qui est **protégé** de ce qui est simplement **transporté**.

### Objectif Pédagogique
Comprendre par la pratique la différence entre **Encodage** (formatage publique) et **Chiffrement** (secret mathématique).

### Phase A : L'Investigation
Vous avez intercepté cette étrange chaîne de caractères sur le réseau interne de l'école :

`TW9uIG1vdCBkZSBwYXNzZSBlc3QgOiAxMjM0NTY=`

**Votre mission :**
Trouvez ce que signifie ce message sans qu'on vous dise quel outil utiliser.
* *Indice 1 :* Observez la fin de la chaîne. Ce caractère `=` est souvent une signature.
* *Indice 2 :* Dans CyberChef, il existe un outil nommé "Magic" (la baguette magique) qui tente de deviner le format pour vous. Ou alors, demandez à une IA quel est ce format.

### Phase B : L'Intrusion
Maintenant que vous avez compris comment traduire ce langage machine :
1.  Utilisez CyberChef pour **Encoder** (Attention, pas chiffrer!) une phrase contenant : `VotrePrénom : VotrePlatPréféré`.
2.  Postez cette chaîne incompréhensible dans le canal **Teams** de la classe.
3.  Copiez la chaîne d'un **autre étudiant** et décodez-la pour découvrir ce qu'il mange.


> **À rendre sur Moodle :**
> 1. Le plat préféré de l'étudiant que vous avez "espionné" (indiquez son prénom).
> 2. Est-ce une bonne méthode de chiffrage ?


---

## 2. L'Attaque Fréquentielle : La langue laisse des traces
{: .d-inline-block }
Durée : 15 min
{: .label .label-red }

Les méthodes simples de chiffrement (remplacer une lettre par une autre) ont été utilisées pendant des siècles. Mais elles ont une faille fatale : la structure même de la langue française.

### Objectif Pédagogique
Comprendre intuitivement comment casser un code sans avoir la clé, simplement en analysant les statistiques du texte (Analyse Fréquentielle).

### Phase A : Le Déchiffrement (Cassage de Code)
Le QG a intercepté un message crypté provenant d'un ancien système. Ce n'est pas du César (le décalage n'est pas constant), c'est une **Substitution Mono-alphabétique** (chaque lettre a été remplacée par une autre de façon mélangée).

**Texte intercepté :**
`X'PUPXZKX KRXVWXUJTXXXX GXLUXJ CX CXYTUXL CXK XJJJLXK. KT YBUK XTKXW ZX UXKKPUX, YBUK PYXW ZBVFCLK CX GLTYZTGX. GBU ZBQITLWXL : CXK VBWK CXK GXDK VBVLTUJK KBUJ YBJJLX GBUUBCX.`

**Votre mission :** Retrouvez le texte original.

**Conseils d'investigation :**
1.  Utilisez l'outil `Frequency Analysis` dans CyberChef.
2.  Repérez la lettre qui revient le plus souvent dans le code (le pic le plus haut). En français, quelle est la lettre la plus courante ? (C'est probablement elle !).
3.  Utilisez l'outil `Substitute` pour remplacer les lettres codées par les lettres réelles.
    * *Astuce :* Commencez par remplacer la plus fréquente. Puis regardez les mots courts de 2 ou 3 lettres (LE, LA, DE, LES...) pour deviner la suite. C'est comme le jeu du pendu.

### Phase B : L'Infiltration (Envoi de message)
Maintenant que vous avez identifié quelles lettres remplacent quelles autres (vous avez "cassé" l'alphabet de substitution), vous devez vous faire passer pour l'ennemi.

1.  Utilisez l'alphabet de substitution que vous venez de découvrir pour **chiffrer** un court message (ex: "La cible est ici").
2.  Postez ce message chiffré dans le chat **Teams**.
3.  Si vos camarades ont réussi la Phase A, ils devraient être capables de lire votre message instantanément.

### 📝 Le Délivrable
Pour prouver que vous avez cassé le code, vous devez rendre **votre propre Prénom chiffré** avec cet alphabet spécifique.

> **À rendre sur la plateforme :**
> * Votre Prénom chiffré (Exemple : si *Paul* devient *Gxwj*, rendez *Gxwj*).
> * 
---

## 3. La Collaboration (Vigenère)
{: .d-inline-block }
Durée : 20 min
{: .label .label-yellow }

Pour contrer l'analyse fréquentielle, Blaise de Vigenère a eu une idée : utiliser une clé pour changer le décalage à chaque lettre.

### Objectif Pédagogique
Expérimenter la nécessité d'une **Clé Secrète Partagée** et comprendre ses limites.

### 3.1 L'Échange (Travail en binôme)
1.  Mettez-vous par deux (Alice et Bob).
2.  **Accordez-vous sur une CLÉ secrète** (un mot simple, ex: "LINUX"). Ne l'écrivez pas dans le chat public !
3.  Chacun écrit un message pour l'autre.
4.  Utilisez l'opération `Vigenère Encode` avec votre clé.
5.  Postez **uniquement le résultat chiffré** dans le canal Teams de la classe.
6.  Récupérez le message de votre partenaire et déchiffrez-le (`Vigenère Decode`).

### 3.2 La Faille (Démonstration)
Regardez les messages des autres groupes. Essayez l'analyse fréquentielle dessus. Le graphique est "plat", n'est-ce pas ? Le code semble incassable.

**Pourtant, Vigenère a une faiblesse : la répétition de la clé.**

Le Quartier Général Ennemi (le Professeur) a envoyé ce long message chiffré avec une clé trop faible :

`ZRWXSM KIO IWE SIVV EMJ. KIO IWE SIVV EMJ. KIO IWE SIVV EMJ. VW WIXZI FM GLMSQ QW EIVZQ. RW AWKZMJ I WWZI KIVWE.`

1.  Ouvrez un nouvel onglet CyberChef.
2.  Utilisez l'outil `Vigenère Solver` (cet outil tente de deviner la longueur de la clé mathématiquement).
3.  Regardez si CyberChef arrive à trouver la clé et le message.

---

## 4. Le Standard Moderne : AES & L'Effet Avalanche
{: .d-inline-block }
Durée : 15 min
{: .label .label-green }

Vigenère est cassable. Aujourd'hui, nous utilisons l'AES (Advanced Encryption Standard). C'est un chiffrement par bloc qui crée une "confusion" totale.

### Objectif Pédagogique
Visualiser l'**Effet Avalanche** : Un changement minuscule dans l'entrée provoque un changement total dans la sortie. C'est la signature d'un bon algorithme de chiffrement.

### Mission
Vous allez simuler le comportement d'un coffre-fort numérique.

1.  Mettez l'opération `AES Encrypt`.
2.  **Clé (Key) :** `0123456789abcdef0123456789abcdef` (copiez ceci, c'est une clé hexadécimale de 32 octets).
3.  **IV (Initialization Vector) :** `00000000000000000000000000000000`
4.  **Input 1 :** Écrivez le mot `DANGER`
    * *Observez l'Output (en Hex).* Notez les 4 premiers caractères.
5.  **Input 2 :** Changez juste une lettre : `MANGER`
    * *Observez l'Output.*

**Question :** Est-ce que seule la première lettre du code a changé (comme dans Vigenère) ou est-ce que **tout** le code est devenu totalement différent ?

**Livrable Final :** Copiez dans votre rendu les deux chaînes hexadécimales obtenues pour prouver que vous avez constaté l'effet avalanche.

---

## Devoir Maison : Le Dossier Snowden
{: .label .label-purple }

*(Disponible sur la plateforme de cours)*

Vous avez récupéré un fichier étrange laissé par un lanceur d'alerte. Il contient une succession d'énigmes :
1.  Un code binaire à déchiffrer via une opération **XOR** (Indice : la clé est une date importante).
2.  Une "Poupée Russe" cryptographique : Du Base64 qui contient du Vigenère, qui contient le message final.

Bonne chance, agents.
