---
layout: default
title: "TP Révision : L'Enquête Numérique"
order: 14
description: Synthèse pratique — séances 1, 2, 7, 8 et 9
nav_order: 14
published: true
---

# TP Révision : L'Enquête Numérique

{: .no_toc }

---

## Mise en situation

Une PME belge a été compromise la nuit dernière. L'attaquant a pris le large, mais les techniciens ont eu le temps de figer la machine victime et de récupérer quelques artefacts : un rapport de scan, une capture réseau de quelques paquets, une note laissée par l'attaquant, et une archive chiffrée qu'il n'a pas eu le temps d'exfiltrer.

Votre mission : **reconstituer le déroulé de l'attaque** et **récupérer le contenu de l'archive**. Aucune machine cible à compromettre — vous travaillez sur les seules traces laissées sur place. C'est exactement ce que ferait un analyste SOC le lendemain d'un incident.

{: .important }
> Cet exercice mobilise les notions des séances **1, 2, 7, 8 et 9**. Toutes les réponses peuvent être trouvées avec les outils déjà à votre disposition. **Aucune installation, aucun accès internet requis.**

---

## Environnement de travail

Vous travaillez sur **deux machines** :

| Environnement | Rôle dans ce TP |
|---|---|
| **PC Windows de l'école** | Wireshark (interface graphique) pour analyser la capture réseau |
| **VM Ubuntu (accès SSH)** | Outils CLI : `base64`, `md5sum`, `openssl`, `unzip`, `cat`, `nano` |


---

## 0. Récupération du dossier d'investigation

{: .d-inline-block }
Durée : 5 min
{: .label .label-green }

1. Sur le **PC Windows**, téléchargez [`enquete.zip`]({{ site.baseurl }}/ressources/tp12_revisions/enquete.zip) (également disponible sur Moodle) et placez-le sur votre **bureau**.
2. Décompressez l'archive (clic droit → *Extraire tout*). Vous obtenez un dossier `enquete/` contenant :

   ```
   scan.txt             note_attaquant.txt
   capture_1.pcap       capture_2.pcap      
   archive.enc
   ```

3. **Les deux fichiers `capture_*.pcap` restent sur Windows** (on les ouvrira avec Wireshark).
4. **Les trois autres fichiers doivent être transférés vers la VM Ubuntu**, dans votre dossier `home`. Deux méthodes au choix :

   - **PowerShell (le plus simple, intégré à Windows 10/11)** — depuis le dossier `enquete/` :
     ```powershell
     scp scan.txt note_attaquant.txt archive.enc VOTRE_USER@IP_DE_LA_VM:~/
     ```

5. Connectez-vous en SSH à la VM et vérifiez :

   ```bash
   cd ~
   ls scan.txt note_attaquant.txt archive.enc
   ```

   Les trois fichiers doivent être listés sans erreur.

{: .warning }
> Avant de continuer, vérifiez que les fichiers font bien la même taille sur la VM que sur Windows (`ls -l` côté VM vs propriétés du fichier côté Windows). Un transfert tronqué ferait échouer le déchiffrement final.

---

## 1. Lecture du rapport de reconnaissance

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

1. Listez les services exposés (nom + version). Combien y en a-t-il ?
2. **Repérez les 2 services qui devraient vous faire bondir.** Justifiez : pourquoi sont-ils particulièrement préoccupants ? *(Indice : pensez à la séance 9 — l'un d'eux a une histoire célèbre de backdoor introduite dans le code source officiel.)*
3. Pour chacun, **citez une mesure concrète** qu'un administrateur aurait dû prendre pour réduire la surface d'attaque.

---

## 2. Anatomie du trafic intercepté

{: .d-inline-block }
Durée : 15 min
{: .label .label-yellow }

Deux fichiers `capture_1.pcap` et `capture_2.pcap` contiennent des paquets capturés sur le réseau de la victime au moment de l'intrusion. Vous allez les ouvrir avec **Wireshark sur Windows** (double-cliquez sur le fichier).

### Mission — Partie A : Forensic d'une attaque

Ouvrez `capture_1.pcap`. Quel **type d'attaque** est en cours dans cette capture ? Quel élément vous a permis de le déduire ?

### Mission — Partie B : le paquet HTTP

Ouvrez maintenant `capture_2.pcap`. Dans la barre de filtre de Wireshark, tapez :

```
http
```

Repérez une requête `GET` envoyée par le client. Faites un **clic droit dessus → Follow → HTTP Stream** : une fenêtre s'ouvre avec le contenu complet de la requête en clair.

#### Questions

3. Trouvez la ligne `Authorization: Basic ...`. Que représente la longue chaîne après le mot `Basic` ?
4. **Décodez-la.** Sur la VM Ubuntu :

   ```bash
   echo -n "LA_CHAINE_ICI" | mettre_le_bon_outil_ici -d
   ```

   *(Indice : séance 1 — le caractère `=` en fin de chaîne, ça vous dit quelque chose ?)*

{: .warning }
> Notez précieusement le **mot de passe** que vous venez de récupérer (la partie après le `:`). Il va vous servir dans la suite.

### Pour réfléchir

 Cette authentification HTTP Basic est très répandue. Le mot de passe est-il **chiffré** ? Si non, qu'est-il alors ? Quelle est la différence ?


---

## 3. Le message du complice

{: .d-inline-block }
Durée : 5 min
{: .label .label-green }

L'attaquant a laissé une note sur la machine, mais l'a "protégée" à sa façon. Affichez-la :

```bash
cat note_attaquant.txt
```

Vous voyez une chaîne de caractères apparemment incompréhensible. Mais vous connaissez maintenant ce format.

### Mission

Décodez la note :

```bash
base64 -<a_trouver_la_bonne_option> note_attaquant.txt
```
hint: ```man base64``` devrait vous aider a trouver la bonne option 
### Questions

1. Que dit la note ?
2. **L'attaquant pense avoir "caché" son message.** A-t-il raison ? Pourquoi le Base64 n'est-il pas un mécanisme de protection ?
3. Quel mécanisme **aurait réellement** protégé cette note si l'attaquant l'avait voulu ?

---

## 4. La clé du coffre-fort

{: .d-inline-block }
Durée : 5 min
{: .label .label-green }

La note (décodée à l'étape 3) vous indique comment fabriquer la clé qui ouvrira l'archive : **le hash MD5 (en hexadécimal) du mot de passe mentionné dans cette note.**

{: .note }
> Attention : ce mot de passe est **différent** de celui intercepté dans `capture_2.pcap`. La §2 et la §4 sont deux exercices indépendants.

### Mission

Calculez ce hash sur la VM :

```bash
echo -n "le_mot_de_passe_intercepte" | a_mettre_le_bon_outil_ici
```

{: .warning }
> Le `-n` est **crucial** : sans lui, `echo` ajoute un saut de ligne invisible, et le hash sera complètement différent. Si votre déchiffrement échoue à l'étape suivante, c'est probablement ça.

La sortie ressemble à ceci :

```
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx  -
```

La clé est constituée des **32 caractères hexadécimaux** au début. Le tiret et les espaces qui suivent ne font **pas** partie de la clé.

### Questions

1. Notez la clé obtenue (les 32 caractères hex).
2. Serait-il possible, à partir de ce hash, de **retrouver le mot de passe d'origine** par un calcul mathématique direct ? Pourquoi ?
3. Et pourtant, en pratique, des sites comme CrackStation retrouvent en quelques secondes le mot de passe correspondant à de très nombreux hashs MD5. **Comment font-ils ?** *(Indice : séance 2, principe du dictionnaire.)*

---

## 5. Ouverture du coffre-fort

{: .d-inline-block }
Durée : 5 min
{: .label .label-green }

Vous avez la clé. Il ne reste qu'à ouvrir l'archive, qui a été chiffrée en AES-256-CBC.

### Mission

Sur la VM :

```bash
openssl enc -aes-256-cbc -pbkdf2 -d -in archive.enc -out flag.txt -k "VOTRE_CLE_ICI"
cat flag.txt
```

Remplacez `VOTRE_CLE_ICI` par les 32 caractères hexadécimaux calculés à l'étape 4 (entre guillemets droits, sans espace).

{: .note }
> Si openssl répond `bad decrypt`, c'est presque toujours dû à une clé incorrecte. Vérifiez :
> - que vous avez utilisé `echo -n` à l'étape 4 (pas de saut de ligne) ;
> - que vous n'avez pas copié le tiret ni des espaces dans la clé ;
> - que vous avez bien utilisé le mot de passe **donné dans la note** (étape 3), pas celui intercepté dans le trafic.

### Questions

1. Quel est le contenu du fichier ? Notez-le précieusement — c'est votre **preuve de résolution** du TP.
2. AES est un chiffrement **symétrique**. Qu'est-ce que cela signifie concrètement (par rapport à la clé) ?
3. Si l'attaquant avait utilisé un mot de passe **fort** (long, aléatoire, jamais réutilisé), même en connaissant la méthode de chiffrement (AES-256), auriez-vous pu déchiffrer l'archive avec votre approche ? Pourquoi ?

---

## 6. Synthèse — le rapport d'incident

{: .d-inline-block }
Durée : 10 min
{: .label .label-yellow }

C'est l'étape la plus importante du TP. Répondez **par écrit** (dans un fichier texte ou sur papier) aux questions suivantes — vos réponses constituent votre rapport.

### A. Chronologie de l'attaque

Reconstituez en **4 étapes courtes** (1 phrase chacune) ce que l'attaquant a fait, dans l'ordre. Pour chaque étape, indiquez la **séance du cours** correspondante :

1. Phase de reconnaissance — comment a-t-il découvert la cible et ses services ?
2. Positionnement réseau — comment s'est-il mis en mesure d'intercepter le trafic ?
3. Récolte d'identifiants — qu'a-t-il intercepté, et pourquoi est-ce arrivé si facilement ?
4. Récupération du contenu chiffré — quelle faiblesse a rendu le déchiffrement possible *pour vous* (et donc pour lui s'il avait été plus rapide) ?

### B. Défenses

Choisissez **deux** des quatre étapes ci-dessus et citez, pour chacune, **une mesure concrète** qui aurait stoppé ou ralenti significativement l'attaquant. Soyez précis : pas « améliorer la sécurité », mais par exemple « activer le DHCP Snooping et la Dynamic ARP Inspection sur les switches » ou « imposer HTTPS au lieu de HTTP ».

### C. Question de fond

Si l'attaquant avait utilisé exactement le **même mot de passe** intercepté pour chiffrer son archive (sans le passer dans MD5), votre attaque aurait-elle quand même fonctionné ? Qu'est-ce que l'étape MD5 ajoute (ou n'ajoute pas) en termes de sécurité ?

---

## Critères de réussite

Vous avez réussi le TP si :

- ✅ Vous avez ouvert l'archive et récupéré le flag.
- ✅ Vous pouvez expliquer **chaque commande** que vous avez tapée.
- ✅ Votre synthèse (§6) lie chaque action de l'attaquant à une séance du cours.

Si vous bloquez à une étape pendant plus de 5 minutes, **passez à la suivante** et revenez plus tard. Toutes les étapes sont indépendantes les unes des autres, sauf la chaîne **3 → 4 → 5** (décoder la note → hasher le mot de passe qu'elle donne → déchiffrer l'archive), qui est strictement séquentielle.
