

---
layout: default
title: "TP Révision : L'Enquête Numérique"
order: 14
description: Synthèse pratique — séances 1, 2 et 7 à 10
nav_order: 14
published: true
---

# TP Révision : L'Enquête Numérique
{: .no_toc }

## Table des matières
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Mise en situation

Une PME belge a été compromise la nuit dernière. L'attaquant a pris le large, mais les techniciens ont eu le temps de figer la machine victime et de récupérer quelques artefacts : un rapport de scan, une capture réseau de quelques paquets, une note laissée par l'attaquant, et une archive chiffrée qu'il n'a pas eu le temps d'exfiltrer.

Votre mission : **reconstituer le déroulé de l'attaque** et **récupérer le contenu de l'archive**. Aucune machine cible à compromettre — vous travaillez sur les seules traces laissées sur place. C'est exactement ce que ferait un analyste SOC le lendemain d'un incident.

{: .important }
> Cet exercice mobilise les notions des séances **1, 2, 7, 8, 9 et 10**. Toutes vos réponses peuvent être trouvées avec les outils déjà installés sur votre VM et un navigateur web. **Aucune installation requise.**

---

## Outils nécessaires

Sur votre VM Linux (terminal uniquement) :

- `base64`, `md5sum`, `openssl` (déjà présents sur toute distribution Ubuntu)
- `tshark` ou `wireshark` pour lire les captures réseau
- Un éditeur de texte (`nano`, `cat`)

Dans votre navigateur (optionnel, pour confort) :

- [CyberChef](https://gchq.github.io/CyberChef/) si vous préférez le visuel

{: .note }
> Si `tshark` n'est pas installé : `sudo apt install tshark -y`. Cette commande est rapide et fiable (paquet standard Ubuntu).

---

## 0. Récupération du dossier d'investigation

Vous trouverez `enquete.zip` sur Moodle :  Téléchargez-le et décompressez-le dans votre dossier de travail :

```bash
cd ~
unzip enquete.zip
cd enquete
ls
```

Vous devez voir quatre fichiers :

```
scan.txt           note_attaquant.txt
capture.pcap       archive.enc
```

---

## 1. Phase de reconnaissance "live" (échauffement)

{: .d-inline-block }
Durée : 5 min
{: .label .label-green }

Avant de plonger dans les artefacts, échauffez-vous avec une recon active sur la seule cible publique autorisée pour ce TP :

```bash
nmap -sV scanme.nmap.org
```

### Questions

1. Quels ports sont ouverts ? Quel rôle joue cette machine ?
2. Quelle est la **différence fondamentale** entre ce que vous venez de faire (recon active) et l'analyse des artefacts que vous allez faire dans la suite (recon passive sur traces) ?

{: .highlight }
> **Pas le temps ?** Cette étape est optionnelle. Si vous êtes serrés, passez directement au point 2.

---

## 2. Lecture du rapport de reconnaissance

{: .d-inline-block }
Durée : 10 min
{: .label .label-yellow }

L'attaquant a manifestement scanné la cible avant de l'attaquer. Le rapport qu'il a laissé derrière lui est dans `scan.txt`.

```bash
cat scan.txt
```

### Mission

Vous êtes l'administrateur de cette machine. Vous découvrez ce rapport sur le poste compromis. Analysez-le **comme s'il s'agissait de votre serveur**.

### Questions

1. Combien de services sont exposés ? Lesquels ?
2. **Repérez les 2 services qui devraient vous faire bondir.** Justifiez : pourquoi sont-ils particulièrement préoccupants ? (Indice : pensez à la séance d'exploitation — l'un d'eux a une histoire célèbre.)
3. Pour chacun, **citez une mesure concrète** qu'un administrateur aurait dû prendre pour réduire la surface d'attaque.

---

## 3. Anatomie du trafic intercepté

{: .d-inline-block }
Durée : 15 min
{: .label .label-yellow }

Le fichier `capture.pcap` contient quelques paquets qui ont été capturés sur le réseau de la victime au moment de l'intrusion.

```bash
tshark -r capture.pcap
(ou wireshark dans votre Windows) 
```

Pour un affichage plus détaillé :

```bash
tshark -r capture.pcap -V
(ou wireshark dans votre Windows) 
```

### Mission

Trois paquets seulement. Lisez-les attentivement.

### Questions

1. **Les deux premiers paquets** sont du protocole **ARP**. Regardez le contenu : que prétend la machine `192.168.1.50` ? Quel type d'attaque cela évoque-t-il dans le cours ? *(Indice : séance 8.)*
2. Pourquoi ces deux paquets ARP sont-ils une condition nécessaire pour pouvoir intercepter le 3ème paquet ?
3. **Le troisième paquet** est une requête HTTP. Affichez son contenu complet (`-V` ou `-x`) et trouvez la ligne `Authorization: Basic ...`. Que représente cette chaîne mystérieuse à la fin ?
4. **Décodez-la.** Avec quelle commande ? *(Indice : séance 1 — `=` en fin de chaîne, ça vous dit quelque chose ?)*

{: .warning }
> Notez précieusement le **mot de passe** que vous venez de récupérer. Il va vous servir dans la suite.

### Pour réfléchir

5. Cette authentification HTTP Basic est très répandue. Le mot de passe est-il **chiffré** ? Si non, qu'est-il alors ? Quelle est la différence ?
6. Comment l'attaquant a-t-il probablement deviné ce mot de passe au départ ? *(Indice : séance 2.)*

---

## 4. Le message du complice

{: .d-inline-block }
Durée : 5 min
{: .label .label-green }

L'attaquant a laissé une note sur la machine, mais l'a "protégée" à sa façon. Affichez-la :

```bash
cat note_attaquant.txt
```

Vous voyez une longue chaîne de caractères apparemment incompréhensible. Mais vous connaissez maintenant ce format.

### Mission

Décodez la note.

```bash
base64 -d note_attaquant.txt
```

### Questions

1. Que dit la note ?
2. **L'attaquant pense avoir "caché" son message.** A-t-il raison ? Pourquoi le Base64 n'est-il pas un mécanisme de protection ?
3. Quel mécanisme **aurait réellement** protégé cette note si l'attaquant l'avait voulu ?

---

## 5. La clé du coffre-fort

{: .d-inline-block }
Durée : 5 min
{: .label .label-green }

La note vous indique comment fabriquer la clé qui ouvrira l'archive : **le hash MD5 (en hexadécimal) du mot de passe intercepté dans le trafic.**

### Mission

Calculez ce hash. La commande est simple :

```bash
echo -n "le_mot_de_passe_intercepte" | md5sum
```

{: .warning }
> Le `-n` est **crucial** : sans lui, `echo` ajoute un saut de ligne, et le hash sera complètement différent. Si votre déchiffrement échoue à l'étape suivante, c'est probablement ça.

### Questions

1. Notez le hash obtenu (les 32 caractères hexadécimaux, sans le `-` à la fin).
2. Est-ce qu'il serait possible, à partir de ce hash, de **retrouver le mot de passe d'origine** par un calcul direct ? Pourquoi ?
3. Et pourtant, en pratique, des sites comme CrackStation retrouvent en quelques secondes le mot de passe correspondant à de très nombreux hashs MD5. **Comment font-ils ?** *(Indice : séance 2, principe du dictionnaire.)*

---

## 6. Ouverture du coffre-fort

{: .d-inline-block }
Durée : 5 min
{: .label .label-green }

Vous avez la clé. Il ne reste qu'à ouvrir l'archive, qui a été chiffrée en AES-256-CBC.

### Mission

```bash
openssl enc -aes-256-cbc -pbkdf2 -d -in archive.enc -out flag.txt -k "VOTRE_HASH_ICI"
cat flag.txt
```

Remplacez `VOTRE_HASH_ICI` par le hash calculé à l'étape 5 (les 32 caractères hex, entre guillemets).

### Questions

1. Quel est le contenu du fichier ? Notez-le précieusement — c'est votre **preuve de résolution** du TP.
2. Pourquoi AES est-il dit **symétrique** ? Quelle est la différence avec RSA ?
3. Si l'attaquant avait utilisé un mot de passe **fort** (long, aléatoire, jamais réutilisé), même en connaissant la méthode de chiffrement (AES-256), auriez-vous pu déchiffrer l'archive avec votre approche ? Pourquoi ?

---

## 7. Rapport d'incident

{: .d-inline-block }
Durée : 15 min
{: .label .label-yellow }

C'est l'étape la plus importante du TP. Vous êtes maintenant l'analyste qui doit rendre son rapport à la direction de la PME.

### Mission

Rédigez un **bref rapport d'incident** (dans un fichier `rapport.md`) structuré ainsi :

#### A. Chronologie de l'attaque

Reconstituez les étapes que l'attaquant a probablement suivies, dans l'ordre. Pour chaque étape, indiquez la **séance du cours** à laquelle elle se rapporte. Au minimum :

1. Phase de reconnaissance — comment l'attaquant a-t-il découvert la cible et ses services ?
2. Positionnement réseau — comment s'est-il mis en mesure d'intercepter le trafic ?
3. Récolte d'identifiants — qu'a-t-il intercepté, et pourquoi est-ce arrivé si facilement ?
4. Accès au système — qu'a-t-il fait des identifiants récupérés ?

#### B. Recommandations défensives

Pour **chacune** des 4 étapes ci-dessus, citez **une mesure concrète** qui aurait stoppé ou ralenti significativement l'attaquant. Soyez précis : pas "améliorer la sécurité", mais par exemple "activer le DHCP Snooping sur les switches" ou "imposer HTTPS avec HSTS".

#### C. Question ouverte

L'attaquant aurait également pu utiliser une attaque de type **Rogue DHCP** (séance 9) pour se positionner en Man-in-the-Middle. **Quelle aurait été la différence** par rapport à l'attaque ARP réellement utilisée ? Donnez un avantage et un inconvénient de chaque approche du point de vue de l'attaquant.

---

## Critères de réussite

Vous avez réussi le TP si :

- ✅ Vous avez ouvert l'archive et récupéré le flag.
- ✅ Vous pouvez expliquer **chaque commande** que vous avez tapée (un examen oral pourrait vous le demander).
- ✅ Votre rapport d'incident lie chaque action de l'attaquant à une séance du cours **et** à une défense concrète.

Si vous bloquez à une étape pendant plus de 10 minutes, **passez à la suivante** et revenez plus tard. Toutes les étapes sont indépendantes pour les questions, seule la chaîne de récupération du flag (étapes 3 → 5 → 6) est strictement séquentielle.

---

## Pour aller plus loin (hors TP)

{: .d-inline-block }
Optionnel
{: .label .label-blue }

- **Refaire l'attaque "live"** : montez DVWA dans une VM, repérez le formulaire, capturez le trafic avec Wireshark sur votre propre interface, et reconstituez la chaîne complète vous-même.
- **Pousser le pcap** : ouvrez `capture.pcap` dans **Wireshark** (interface graphique) et explorez les paquets ARP en détail. Repérez le champ `opcode = 2` (gratuitous ARP) et comprenez pourquoi un switch sans DAI ne peut pas s'en protéger.
- **Tester la solidité de votre propre mot de passe** : `echo -n "votre_mot_de_passe" | md5sum`, puis collez le résultat dans CrackStation. Si vous le retrouvez en clair, changez-le.
