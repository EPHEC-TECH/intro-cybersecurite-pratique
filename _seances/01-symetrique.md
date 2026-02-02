---
layout: default
title: Chiffrement symétrique
nav_order: 1
has_children: false
---

# TP 1 : De Jules César à l'AES
{: .no_toc }

## Introduction à la Cryptographie Symétrique
{: .fs-9 }

Bienvenue, Recrues. 
Vous intégrez aujourd'hui la **Division de Sécurité Offensive**. Votre mission : comprendre comment protéger des informations critiques et, surtout, comment les attaquants brisent les protections obsolètes.


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



---
## 2.  Chiffrement de César

**Un informateur anonyme a déposé un pli scellé dans votre casier numérique. Il contient les preuves d'une fuite de données imminente, mais le contenu est illisible. Votre mission est de percer ce secret avant qu'il ne soit trop tard.**

### 1. Le Code César (Théorie)
Depuis l’antiquité, les hommes ont toujours éprouvé le besoin de modifier un texte afin de le dissimuler. Le code de César consiste à décaler chaque lettre de l’alphabet d’un certain nombre de rangs (la **clé**). 

Par exemple, avec une clé de 3, A devient D, B devient E, et ainsi de suite.

### 2. Manipulation avec CyberChef
Pour cet exercice, nous allons utiliser l'outil **CyberChef**, un "couteau suisse" de la cryptographie.

1. Ouvrez [CyberChef](https://gchq.github.io/CyberChef/).
2. Dans la barre de recherche "Operations" (en haut à gauche), tapez **"Caesar"**.
3. Glissez l'opération **"Caesar Decode"** dans la zone centrale "Recipe".

### Mission A : Interceptions de routine
* **Décodage (Clé 3) :** Retrouvez le sens de cette consigne de sécurité :  
  `GDQV OD YLH LO IDXW VDYRLU FRPSWHU PDLV SDV VXU OHV DXWUHV`
* **Codage (Clé 17) :** Chiffrez le message suivant pour le transmettre en toute discrétion :  
  `LES PETITS RUISSEAUX FONT DE GRANDES RIVIERES`

### Mission B : Analyse de la Fuite (Cryptanalyse)
Vous avez intercepté ce mémo circulant sur un canal non sécurisé. Le décalage utilisé est inconnu :

`VO WOCCKQO AEO FYEC VYCOJ OCDC ZBYDOQO ZKB EX MYNO KXDSAEO WKSC FYDBO MEBSYCSDO OCDC ZVEC PYBDO.`  
`KOKC FYEC NOFOJ PBKSCOXD PBKDMKCC OB MO COMBOD ZYEB MYWZB OXNBO VK PYBMO NO V'KOKV ICB PBOM EODDS OVVO.`

**Indices pour la Mission B :**
* Vous ne connaissez pas la clé (le shift).
* **L'indice de fréquence :** Mais vous savez que le message est en francais et qu'elle pourrait être la lettre la plus fréequente en francais ? et dans ce message ?  
* Testez votre calcul dans CyberChef en ajustant le "Shift Amount".

---

## Questions d’analyse

1. **Fiabilité statistique :** Pourquoi l'analyse fréquentielle (chercher la lettre la plus commune) est-elle beaucoup plus efficace sur un long texte que sur un message de seulement deux ou trois mots ?
2. **Structure du langage :** Le chiffrement de César ne modifie ni les espaces ni la ponctuation. En quoi la conservation de la longueur des mots et de la structure des phrases aide-t-elle un cryptanalyste à casser le code ?
3. **Complexité :** Si l'alphabet compte 26 lettres, quel est le nombre maximum d'essais nécessaires pour trouver la clé par "Force Brute" ? Pourquoi ce nombre est-il considéré comme dérisoire pour un ordinateur moderne ?
4. **Vulnérabilité :** Une fois que vous avez identifié qu'une seule lettre (par exemple le 'E') a été décalée d'une valeur X, est-il nécessaire d'analyser le reste des lettres pour connaître la clé ? Pourquoi ?



## [Exercice Bonus]  L'Attaque Fréquentielle : La langue laisse des traces
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





## [Exercice Bonus]  (Vigenère)
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




## 3.  Le chiffrement XOR et le One-Time Pad (OTP)

**Objectif :** Découvrir l'opération logique XOR (OU exclusif) et comprendre le principe du masque jetable, l'un des rares systèmes de chiffrement théoriquement incassables.



## 1. Le principe du XOR
En cryptographie, l'opération **XOR** est fondamentale. Elle compare les bits de deux données (le texte et la clé) selon une règle simple : si les bits sont identiques, le résultat est 0 ; s'ils sont différents, le résultat est 1.

Pour cet exercice, nous allons utiliser des chaînes de caractères comme clés.

* **Exercice N°1 : Manipulation simple**
  En utilisant CyberChef, chiffrez le mot `SECRET` avec la clé `KEY`. Notez le résultat obtenu (qui peut contenir des caractères non imprimables ou des symboles étranges).
  
* **Exercice N°2 : Le Masque Jetable (One-Time Pad)**
  Le principe du One-Time Pad est d'utiliser une clé de la même longueur que le message, utilisée une seule fois.
  Chiffrez le message : `INCASSABLE`
  Avec la clé : `XQZRTPLMKB`
  Observez le résultat. Tentez maintenant de déchiffrer ce résultat en utilisant la même opération et la même clé.

* **Exercice N°3 : Le mystère du texte hexadécial**
  On vous intercepte le message suivant (en format Hexadécimal) : `0b1c0c1b1f13`
  On sait que la clé utilisée est le mot : `BRAVO`
  Retrouvez le message original.

---

## Étapes à suivre avec CyberChef

1.  Ouvrez [CyberChef](https://gchq.github.io/CyberChef/).
2.  Dans la liste des opérations, cherchez **"XOR"**.
3.  Configurez l'opération :
    * **Key** : Saisissez votre clé (Format : UTF8 par défaut).
    * **Input Format** : UTF8 (sauf pour l'exercice 3 où vous devrez peut-être traiter de l'Hexadécimal).
4.  Pour l'exercice 3, vous devrez peut-être ajouter l'opération **"From Hex"** avant l'opération **XOR** dans votre "Recipe".

---

## Questions d’analyse

1. Que remarquez-vous après avoir chiffré puis déchiffré avec la même clé ?
2. Pourquoi XOR permet-il de récupérer le texte original ?
3. Quel est l’impact du choix de la clé sur le résultat ?
4. Un chiffrement XOR avec une clé trop simple est-il sûr ? (expliquez)






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


