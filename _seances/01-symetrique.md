---
layout: default
title: Chiffrement symétrique
order: 1
description: De Jules César à l'AES
nav_order: 1
has_children: false
---

# Séance 1 : De Jules César à l'AES

{: .no_toc }

## Introduction à la Cryptographie Symétrique

Bienvenue, Recrues.
Vous intégrez aujourd'hui la **Division de Sécurité Offensive**. Votre mission : comprendre comment protéger des informations critiques et, surtout, comment les attaquants brisent les protections obsolètes.

**Outils requis :**

*   [CyberChef](https://gchq.github.io/CyberChef/) (Un outil "Couteau Suisse" pour le chiffrement)
*   Microsoft Teams (Canal de classe) pour l'échange de données.

---

## Exercice 1 : L'Illusion de la Sécurité (Encodage)

{: .d-inline-block }
Durée : 10-15 min
{: .label .label-yellow }

### Contexte

> L'objectif de cet exercice est de comprendre par la pratique la différence entre **Encodage** (un formatage public) et **Chiffrement** (un secret mathématique).

---

### Mission 1.A : Investigation

> Vous avez intercepté cette étrange chaîne de caractères sur le réseau interne de l'école :
>
> `TW9uIG1vdCBkZSBwYXNzZSBlc3QgOiAxMjM0NTY=`
>
> **Votre mission :** Trouvez ce que signifie ce message sans qu'on vous dise quel outil utiliser.

**Indices :**
*   Observez la fin de la chaîne. Le caractère `=` est souvent une signature de ce type d'encodage.
*   Dans CyberChef, l'outil "Magic" (la baguette magique) peut tenter de deviner le format pour vous.

---

### Mission 1.B : Intrusion

> Maintenant que vous avez compris comment traduire ce "langage machine" :
>
> 1.  Utilisez CyberChef pour **encoder** (et non chiffrer) la phrase `VotrePrénom : VotrePlatPréféré`.
> 2.  Postez cette chaîne incompréhensible dans le canal **Teams** de la classe.
> 3.  Copiez la chaîne d'un **autre étudiant** et décodez-la pour découvrir son plat préféré.

---

## Exercice 2 : Chiffrement de César

{: .d-inline-block }
Durée : 20-30 min
{: .label .label-yellow }

**Contexte**
> Un informateur anonyme a déposé un pli scellé dans votre casier numérique. Il contient les preuves d'une fuite de données imminente, mais le contenu est illisible. Votre mission est de percer ce secret avant qu'il ne soit trop tard.

Le **code de César** consiste à décaler chaque lettre de l’alphabet d’un certain nombre de rangs (la **clé**). Par exemple, avec une clé de 3, A devient D. Le **ROT13** est un cas particulier où le décalage est de 13.

---

### Mission 2.A : Interceptions de routine

> *   **Décodage (Clé 3) :** Retrouvez le sens de cette consigne de sécurité :
>     `GDQV OD YLH LO IDXW VDYRLU FRPSWHU PDLV SDV VXU OHV DXWUHV`
> *   **Codage (Clé 17) :** Chiffrez le message suivant pour le transmettre en toute discrétion :
>     `LES PETITS RUISSEAUX FONT DE GRANDES RIVIERES`

**Instructions pour CyberChef :**
1.  Ouvrez [CyberChef](https://gchq.github.io/CyberChef/).
2.  Dans la barre de recherche, tapez **"ROT13"**.
3.  Glissez l'opération dans la zone "Recipe".
4.  Collez le texte dans la zone **Input**.
5.  Ajustez le décalage (le "Amount") selon la clé demandée.

> ⚠️ Pour cet exercice, vous devez utiliser l'opération **"ROT13"** de cyberchef, et ajuster le décalage (le "Amount") selon la clé demandée (positif pour chiffrer, négatif pour déchiffrer).

---

### Mission 2.B : Analyse de la Fuite (Cryptanalyse)

> Vous avez intercepté ce mémo circulant sur un canal non sécurisé. Cette fois, le décalage utilisé **n’est pas connu** :
>
> `VO WOCCKQO AEO FYEC VYCOJ OCDC ZBYDOQO ZKB EX MYNO KXDSAEO WKSC FYDBO MEBSYCSDO OCDC ZVEC PYBDO.`
> `KOKC FYEC NOFOJ PBKSCOXD PBKDMKCC OB MO COMBOD ZYEB MYWZB OXNBO VK PYBMO NO V'KOKV ICB PBOM EODDS OVVO.`

**Indices pour la Mission :**
*   Vous ne connaissez pas la clé (le décalage).
*   Vous savez que le message est en **français**.
*   Pensez à l’**analyse fréquentielle** (l'outil dans CyberChef s'appel **frequency distribution**) : quelle est la lettre la plus fréquente en français ? Est-elle aussi dominante dans ce message ?


---

### Questions d’analyse

1.  **Fiabilité statistique :** Pourquoi l'analyse fréquentielle (chercher la lettre la plus commune) est-elle beaucoup plus efficace sur un long texte que sur un message de seulement deux ou trois mots ?
2.  **Structure du langage :** Le chiffrement de César ne modifie ni les espaces ni la ponctuation. En quoi la conservation de la longueur des mots et de la structure des phrases aide-t-elle un cryptanalyste à casser le code ?
3.  **Complexité :** Si l'alphabet compte 26 lettres, quel est le nombre maximum d'essais nécessaires pour trouver la clé par "Force Brute" ? Pourquoi ce nombre est-il considéré comme dérisoire pour un ordinateur moderne ?
4.  **Vulnérabilité :** Une fois que vous avez identifié qu'une seule lettre (par exemple le 'E') a été décalée d'une valeur X, est-il nécessaire d'analyser le reste des lettres pour connaître la clé ? Pourquoi ?
5.  **Rot13 :**  Rot13 est un cas particulier de Ceasar. Pourquoi?

---

## Exercice 3 **[à faire en autonomie]** : L'Attaque Fréquentielle 

{: .d-inline-block }
Durée estimée : 15 min
{: .label .label-red }

### Contexte
> Les méthodes de chiffrement par substitution monoalphabetique (remplacer une lettre par une autre) ont une faille fatale : elles ne masquent pas les statistiques de la langue utilisée.

**Objectif :** Comprendre intuitivement comment casser un code sans avoir la clé, simplement en analysant la fréquence des lettres.

---

### Mission 3.A : Le Déchiffrement
> Le QG a intercepté un message crypté. Ce n'est pas du César, c'est une **Substitution Mono-alphabétique** (chaque lettre a été remplacée par une autre de façon mélangée).
>
> **Texte intercepté :**
> `X'PUPXZKX KRXVWXUJTXXXX GXLUXJ CX CXYTUXL CXK XJJJLXK. KT YBUK XTKXW ZX UXKKPUX, YBUK PYXW ZBVFCLK CX GLTYZTGX. GBU ZBQITLWXL : CXK VBWK CXK GXDK VBVLTUJK KBUJ YBJJLX GBUUBCX.`
>
> **Votre mission :** Retrouvez le texte original.

**Conseils d'investigation :**
1.  Utilisez l'outil `Frequency Analysis` dans CyberChef.
2.  Repérez la lettre qui revient le plus souvent dans le code. En français, quelle est la lettre la plus courante ? (C'est probablement elle !).
3.  Utilisez l'outil `Substitute` pour remplacer les lettres codées par les lettres réelles.
    *   *Astuce :* Commencez par la plus fréquente. Puis regardez les mots courts de 1, 2 ou 3 lettres pour deviner la suite.

---

### Mission 3.B : L'Infiltration
> Maintenant que vous avez "cassé" l'alphabet de substitution, vous devez vous faire passer pour l'ennemi.
>
> 1.  Utilisez l'alphabet de substitution que vous venez de découvrir pour **chiffrer** un court message (ex: "La cible est ici").
> 2.  Postez ce message chiffré dans le chat **Teams**.
> 3.  Vos camarades devraient être capables de lire votre message.

---

## Exercice 4 **[à faire en autonomie]** : Le Chiffre de Vigenère

{: .d-inline-block }
Durée : 20 min
{: .label .label-yellow }

### Contexte
> Pour contrer l'analyse fréquentielle, Blaise de Vigenère a eu une idée : utiliser une **clé** (un mot) pour changer le décalage à chaque lettre du message.

**Objectif :** Expérimenter la nécessité d'une **Clé Secrète Partagée** et comprendre ses limites.

---

### Mission 4.A : L'Échange (Travail en binôme)
> 1.  Mettez-vous par deux (Alice et Bob).
> 2.  **Accordez-vous sur une CLÉ secrète** (un mot simple, ex: "LINUX"). Ne l'écrivez pas dans le chat public !
> 3.  Chacun écrit un message secret pour l'autre.
> 4.  Utilisez l'opération `Vigenère Encode` avec votre clé.
> 5.  Postez **uniquement le résultat chiffré** dans le canal Teams (ou autre).
> 6.  Récupérez le message de votre partenaire et déchiffrez-le avec `Vigenère Decode`.

---

### Mission 4.B : La Faille (Démonstration)
> Regardez les messages des autres groupes. L'analyse fréquentielle ne fonctionne plus : le graphique est "plat". Le code semble incassable.
>
> **Pourtant, Vigenère a une faiblesse : si la clé est trop courte, elle se répète.**
>
> Le Quartier Général Ennemi (le Professeur) a envoyé ce long message chiffré avec une clé trop faible :
>
> `So rymeacvyoeowt lgi bb sbsa wsgwéhjlz tuhgl qtbl fbw ryésca ztz qdksh lh rlim xix ssh ifxzsca. Rtwixz ztz atzgpnsh zsrysiz rt Jégpy, gxtdalatuh séjoaéz rt xitsejlg alhiysh, qihxi'pbl uvfilftzgtz bjtéfxxitz qdtat s'OTZ,
  qwhejl okhbrél o éié bbt yéddugt à bbt moxiztzgt llescxaés. Al qwptuys sl Jxnscèys, pbhgltdpg hbfcvabé 'ss rowumft pbséjvxmtghpal', o xuhgvrjph a'prét k'icl qaé wcafoawvpiéhxxit, ysckoca z'puoafgt ks uyéejlbrl qahghpejl
  cqzcaèas. Evigaoca, aêbl qtaht pbvéuwtbgt téhwvrt h gjjqdtpé uhqt à s'ochznzs haoipgipejl atués ehf slg tzdgphh ifxszpuhh jcbts Roogssh Ioqiovl si Mfxlrgpqw Rohpgzp. Ojqcjyr'wbw, ah gérbfxaé rt uch jcbticpqpawdug glddzs hbf
  slg psudywioatz apavébhhxxittsca qdtdalltz ejp, hts ic ltulh pcoahbros, iyocztdyatuh ah adpbsys bvrxmwrhhxvb sb atzgpns tu ic yégjshpa fpkwrhzttsca rxmtéglbi. Jcbwfturgl qtaht owhacxys, r'lgi jcbwfturgl ejl zp zéqjywié hphvzjl
  sha ic tmios ta ejl zp zsjss rvbhaocas tzh ah bérlghphé s'bbt cwvpzpuqt lh s'bbt pbcvjpawdu dtyapuscash.`
>
> **Votre mission :**
> 1. Découvir le message originel

---

## Exercice 5 : Le Chiffrement XOR et le One-Time Pad (OTP)

{: .d-inline-block }
Durée : 15-20 min
{: .label .label-green }

### Contexte
> L'opération logique **XOR** (OU exclusif) est un pilier de la cryptographie moderne. Elle opère au niveau des bits du texte et de la clé en suivant une règle simple : le bit résultant est 1 si les bits d'entrée sont différents, et 0 s'ils sont identiques. Sa propriété magique est d'être réversible : `(Texte XOR Clé) XOR Clé = Texte`. C'est ce qui permet de chiffrer et déchiffrer avec la même clé.

**Objectif :** Découvrir l'opération XOR et comprendre le principe du **masque jetable (OTP)**, l'un des rares systèmes de chiffrement théoriquement incassables.

---

### Mission 5 Le Masque Jetable (One-Time Pad)


> Le principe du One-Time Pad est d'utiliser une clé **de la même longueur que le message**, et de ne l'utiliser **qu'une seule fois**.
> *   En utilisant CyberChef, utilisant l'opération **XOR** (mode HEX, Scheme standard)

>
> *   Chiffrez le message : `INCASSABLE`
> *   Avec la clé : `XQZRTPLMKB`
> *   Observez le résultat. Tentez ensuite de déchiffrer ce résultat en utilisant la même opération et la même clé.

---

### Mission 5.B : Le mystère du texte hexadécimal
> On vous intercepte le message suivant : `pFdd[`
> On sait que la clé utilisée est : `12345`
>
> Retrouvez le message original.


---

### Questions d’analyse
1.  Que remarquez-vous après avoir chiffré puis déchiffré avec la même clé XOR ?
2.  Pourquoi l'opération XOR permet-elle de récupérer le texte original ?
3.  Un chiffrement XOR avec une clé trop simple (ex: "abc") est-il sûr ? Expliquez pourquoi.
4.  Idéalement, une clé doit être utilisé qu'une fois, pourquoi ?

---

## Exercice 6 : Le Standard Moderne : AES & L'Effet Avalanche

{: .d-inline-block }
Durée : 15 min
{: .label .label-green }

### Contexte
> Les algorithmes classiques sont cassables. Aujourd'hui, nous utilisons des standards comme l'**AES (Advanced Encryption Standard)**. C'est un chiffrement par bloc qui vise à créer une "confusion" et une "diffusion" maximales.

**Objectif :** Visualiser l'**Effet Avalanche** : un changement minuscule dans l'entrée (un seul bit) doit provoquer un changement total dans la sortie. C'est la signature d'un bon algorithme de chiffrement.

---

### Mission : Simulation d'un coffre-fort numérique
> 1.  Dans CyberChef, ajoutez l'opération `AES Encrypt`.
> 2.  **Clé (Key) :** `0123456789abcdef0123456789abcdef` (en Hex). *C'est une clé de 128 bits (16 octets), un standard pour l'AES.*
> 3.  **IV (Initialization Vector) :** `00000000000000000000000000000000` (en Hex). *Ce vecteur initialise le chiffrement pour garantir que des messages identiques ne produisent pas le même résultat chiffré.*
> 4.  **Input 1 :** Écrivez le mot `DANGER`
>     *   *Observez l'Output (en Hex).* Notez les 4 premiers caractères.
> 5.  **Input 2 :** Changez juste une lettre : `MANGER`
>     *   *Observez le nouvel Output.*

---

### Question d'analyse
1. Qu'observez vous entre les deux output ? Si ont avait utilisé ROT13, est-ce qu'on aurait eu la même observation ?   En quoi est-ce important ?
2. Que ce passe t'il si on change que le vecteur d'initialisation ?
3. Est-ce AES est encore utilisé aujourd'hui ?  des exemples ?
4. 
