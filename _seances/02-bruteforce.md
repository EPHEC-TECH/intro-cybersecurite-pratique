---
layout: default
title: Brute Force & Dictionnaire
order: 2
description: Analyse d'attaque par dictionnaire sur DVWA
nav_order: 2
has_children: false
---

# Séance 2 : Analyse et compréhension d'une attaque par dictionnaire

{: .no_toc }

## Objectif
{: .no_toc .text-delta }

Apprendre à analyser et comprendre le fonctionnement d'une attaque par dictionnaire sur une application web. Vous allez opérer dans un **environnement isolé** pour découvrir comment un attaquant peut automatiser des milliers d'essais de mots de passe pour forcer un accès.

---

## 1. Architecture et "Isolation" du laboratoire

Pour ce TP, nous allons utiliser une architecture spécifique car les PC de l'école ne permettent pas de lancer directement les outils d'attaque ou docker.

1.  **Votre PC (Windows) :** L'hôte physique.
2.  **La VM (Linux Ubuntu) :** Votre poste de travail. C'est ici que vous lancerez vos outils (Navigateur, Hydra).
3.  **Le Conteneur Docker (DVWA) :** Une "mini-machine" isolée qui tourne *à l'intérieur* de votre VM et qui contient le site web vulnérable que nous allons attaquer.

> **Note sur Docker :** Considérez Docker comme un système permettant de lancer une application (ici, un site web) avec toutes ses dépendances en une seule ligne de commande, sans rien installer de complexe sur la VM.

---

## 2. Préparation de l’environnement

{: .d-inline-block }
Durée : 15-20 min
{: .label .label-yellow }

> **Note 1:** On utilisera ce setup pour de prochain TP également, donc assurez vous de comprendre ce que vous faites (pour le reproduire aux prochains TP)

> **Note 2:** Si vous voulez utiliser votre ordinateur (ex: pour faire l'exercice en autonomie), vous pouvez installer une VM linux ayant docker déjà installé dessus.  Vous pouvez aussi installer docker sur votre machine et installer les outils 'attaquant' sur votre ordinateur (passez par wsl si vous êtes sur windows).  Note: On travaillera Docker en profondeur en deuxième (au cours d'Admin 2) et ce n'est pas necessaire de comprendre docker pour ce cours.


### 2.1. Lancer votre poste de travail (VM)

1.  Sur le PC Windows, lancez votre logiciel de virtualisation (VMware) comme vous avez déjà fait en TP d'OS.
2.  Démarrez la VM appelée **“system admin 2024”** (ou celle indiquée par votre professeur).

TODO: je ne connais pas les identifiants de cette VM ni si il faut la dezip avant...
4. Ouvrez une session. C'est depuis cette VM que vous ferez tout le travail.

### 2.2. Lancer la cible (DVWA via Docker)

Dans la VM, ouvrez un terminal et lancez le serveur vulnérable avec la commande suivante :

```bash
docker run -d -p 80:80 vulnerables/web-dvwa
```
*(L'option `-d` permet de lancer le serveur en arrière-plan pour garder votre terminal libre).*

**Vérification :**
Pour vérifier que le serveur tourne bien, tapez :
```bash
docker ps
```
Vous devriez voir une ligne avec `vulnerables/web-dvwa`. Si la liste est vide, demandez de l'aide.

---

## 3. Phase de "Reconnaissance" (Analyse du formulaire)

{: .d-inline-block }
Durée : 15-20 min
{: .label .label-yellow }

Avant de lancer une attaque automatique, un attaquant doit comprendre précisément comment sa cible communique. Nous allons analyser techniquement ce qui se passe quand on valide le formulaire.

### 3.1. Accéder au module de test
1. Assurez-vous d'être connecté à DVWA (**admin** / **password**).
2. Dans le menu de gauche, cliquez sur **Brute Force**.
3. Vous voyez un nouveau formulaire de connexion au centre de la page. C'est celui-là que nous allons tenter de "casser".

### 3.2. Analyser la requête (Outils de développement)
Nous allons utiliser les outils intégrés à Firefox pour voir "sous le capot".

1. Appuyez sur **F12** (ou clic droit -> Inspecter) pour ouvrir les outils de développement de Firefox.
2. Allez dans l'onglet **Réseau** (Network).
3. Dans le formulaire de la page, tapez des identifiants au hasard :
   * **Username :** `toto`
   * **Password :** `pipo123`
4. Cliquez sur **Login**.

### 3.3. Collecter les informations pour l'attaque
Dans l'onglet Réseau, une nouvelle ligne est apparue (nommée `index.php?...`). Cliquez dessus pour voir les détails à droite.

> **📝 Mission d'analyse : Notez les éléments suivants (indispensables pour l'étape suivante) :**
>
> 1. **La Méthode :** Dans l'onglet "En-têtes" (Headers), vérifiez si c'est du **GET** ou du **POST**.
    *   *(Note importante : Pour cet exercice spécifique de vulnérabilité, DVWA utilise le moins adequat des deux ==> celui qui expose le mot de passe dans l'URL. Dans la "vraie vie", ce n'est normalement pas ainsi ).*
> 2. **Les Paramètres :** Trouvez les noms exacts des variables envoyées (ex: `username`, `password`, `Login`).
> 3. **Le Cookie :** Trouvez la ligne `Cookie`. Vous verrez `PHPSESSID=...` et `security=low`. 
>    * **Notez votre PHPSESSID.** Hydra en aura besoin pour simuler votre session.
> 4. **Le Message d'échec :** Quel texte exact s'affiche en rouge sur la page après l'erreur ? (ex: `Username and/or password incorrect.`). 
>    * Hydra utilisera ce texte pour savoir qu'il s'est trompé.

---

## 4. Préparation du dictionnaire (Liste de mots de passe)

{: .d-inline-block }
Durée : 15-20 min
{: .label .label-yellow }

Une attaque par dictionnaire consiste à tester une liste prédéfinie de mots de passe. Plus la liste est "intelligente" et ciblée, plus l'attaque a de chances de réussir rapidement.

### 4.1. L'Ingénierie Sociale et le "Profiling"
Dans la réalité, un attaquant ne choisit pas ses mots au hasard. Il utilise l'**Ingénierie Sociale** pour profiler sa cible :
*   Il observe le vocabulaire utilisé sur le site web de l'entreprise.
*   Il cherche les noms des projets, des slogans, ou des dirigeants sur LinkedIn.
*   **Pourquoi ?** Car les humains ont tendance à choisir des mots de passe liés à leur environnement quotidien (ex: le nom d'un logiciel interne, le slogan de l'entreprise, etc.). Un dictionnaire de 500 mots "locaux" est souvent plus efficace qu'un dictionnaire générique de 10 millions de mots.

> **Le saviez-vous ?** Le dictionnaire générique le plus célèbre s'appelle **rockyou.txt**. Il contient 14 millions de mots de passe issus d'une fuite réelle de 2009. C'est une base, mais le "profiling" sur mesure reste plus redoutable.

### 4.2. Générer un dictionnaire automatique avec CeWL
**CeWL** (Custom Word List generator) est un outil qui "aspire" un site web pour en extraire tous les mots uniques et créer un dictionnaire sur mesure.

1. **Installer CeWL dans votre VM :**
   ```bash
   sudo apt update && sudo apt install cewl -y
   ```

2. **Aspirer les mots du site DVWA :**
   Nous allons demander à CeWL de créer un fichier `custom_pass.txt` à partir des mots présents sur la page d'accueil :
   ```bash
   cewl -w custom_pass.txt -d 1 -m 5 http://localhost
   ```
   *   `-w custom_pass.txt` : Enregistre le résultat dans ce fichier.
   *   `-d 1` : Profondeur de recherche (s'arrête à la première page).
   *   `-m 5` : Ne récupère que les mots d'au moins 5 lettres.

3. **Vérifier le résultat :**
   Affichez le contenu de votre nouveau dictionnaire :
   ```bash
   cat custom_pass.txt
   ```
TODO: il faut qu'on leur donne un site ayant le mot de passe dedans ! (ce qui n'est pas le cas ici)

---

## 5. L'Attaque avec Hydra

{: .d-inline-block }
Durée : 20 min
{: .label .label-yellow }

Hydra est un outil capable d'automatiser des tentatives de connexion sur des dizaines de protocoles différents (HTTP, SSH, FTP, etc.).

### 5.1. Attention aux erreurs fréquentes (⚠️ À lire avant de lancer)
La commande Hydra est extrêmement sensible. Une seule erreur et rien ne fonctionnera :
*   **Les deux-points (`:`) :** Ils servent de séparateurs pour Hydra. N'en ajoutez pas et n'en enlevez pas dans la chaîne de paramètres.
*   **Espaces :** Il n'y a **aucun espace** autour des deux-points (`:`).
*   **Exactitude :** Le message d'échec (`F=...`) doit être rigoureusement identique au texte vu dans votre navigateur.
*   **Session :** Si vous mettez trop de temps, votre `PHPSESSID` peut expirer. Si l'attaque échoue sans raison, rafraîchissez la page dans Firefox et récupérez le nouveau cookie.

### 5.2. Construire la commande
Lancer une attaque sur un formulaire web demande une syntaxe précise. Voici la commande à adapter avec **votre PHPSESSID** noté à l'étape 3 :

```bash
hydra -l admin -P custom_pass.txt localhost http-get-form "/vulnerabilities/brute/:username=^USER^&password=^PASS^&Login=Login:F=Username and/or password incorrect.:H=Cookie: PHPSESSID=VOTRE_COOKIE; security=low"
```

**Si l'attaque réussit**, Hydra affichera le mot de passe trouvé en évidence.

**Explication des paramètres :**
*   `-l admin` : Le nom d'utilisateur cible.
*   `-P custom_pass.txt` : Le dictionnaire à utiliser.
*   `http-get-form` : Indique à Hydra que nous attaquons un formulaire web utilisant la méthode GET.
*   `F=...` : Indique le message que Hydra doit chercher pour savoir que la tentative a **échoué**.
*   `H=Cookie: ...` : Permet de passer vos informations de session (indispensable pour que DVWA vous laisse accéder à la page).

---

## 6. Défense : Pourquoi l'attaque échoue-t-elle ?

{: .d-inline-block }
Durée : 10 min
{: .label .label-green }

Le but de la cybersécurité est de rendre ce genre d'attaques impossibles ou trop lentes pour être rentables.

### 6.1. Tester la protection "High"
1. Dans DVWA, allez dans **DVWA Security** et passez le niveau sur **High**.
2. Retournez sur l'onglet **Brute Force** et relancez la **même commande Hydra** dans votre terminal.

**Observation :**
L'attaque échoue. En niveau "High", le serveur génère un code unique (Token anti-CSRF) à chaque chargement de page. Comme Hydra ne renvoie pas le bon code, le serveur rejette la tentative avant même de vérifier le mot de passe.

---

## 7. Exercice **[à faire en autonomie]** : Le Brute Force de fichiers (Fuzzing)

{: .d-inline-block }
Durée estimée : 15 min
{: .label .label-red }

### Contexte
> Le Brute Force ne s'applique pas qu'aux mots de passe. Un attaquant peut aussi tenter de deviner les noms des dossiers et des fichiers "cachés" sur un serveur (ex: `/admin`, `/backup`, `/dev`, `/config.php`). Cette technique s'appelle le **Fuzzing de répertoire**. L'administrateur pense que ces pages sont sûres car "personne ne connaît l'URL", mais un outil automatique peut les trouver en quelques secondes.

**Objectif :** Utiliser un dictionnaire de noms de dossiers courants pour découvrir l'arborescence cachée de DVWA.

---

### Mission : Exploration des dossiers "invisibles"
Pour cette mission, nous allons utiliser **dirb**, un scanner de contenu web très simple.

1. **Installer dirb dans votre VM :**
   ```bash
   sudo apt update && sudo apt install dirb -y
   ```

2. **Lancer le scan sur DVWA :**
   ```bash
   dirb http://localhost
   ```

3. **Analyse du résultat :**
   *   Observez la liste des dossiers trouvés par `dirb`.
   *   Vous verrez probablement beaucoup de codes **302** (Redirection vers login) ou **403** (Forbidden).
   *   Cherchez si des dossiers comme `/config`, `/docs` ou `/external` apparaissent.
   *   *Interprétation :* Même si vous ne pouvez pas entrer dans le dossier (Code 403), le simple fait de savoir qu'il **existe** est une faille. Un attaquant sait maintenant qu'il y a un dossier `/config` à attaquer spécifiquement.

---

## 8. Questions d'analyse

{: .d-inline-block }
Durée : 20 min
{: .label .label-yellow }

> Ces questions sont essentielles pour valider votre compréhension. Prenez le temps d'y réfléchir.

### Analyse de l'attaque
1. **Exposition des données :** Lors de l'analyse avec **F12**, vous avez vu les identifiants circuler en clair (méthode GET). Quels sont les risques si un utilisateur se connecte sur un Wi-Fi public ou si un collègue regarde l'historique du navigateur ?
2. **Authentification d'Hydra :** Pourquoi est-il indispensable de fournir le `PHPSESSID` à Hydra ? Que se passerait-il si vous tentiez l'attaque sans ce cookie ?
3. **Profiling (CeWL) :** Pourquoi un dictionnaire généré sur le site public d'une entreprise est-il souvent plus efficace que le célèbre fichier `rockyou.txt` de 14 millions de mots ?

### Analyse de la défense
4. **Automatisation vs Token :** Pourquoi le Token anti-CSRF (vu en niveau High) est-il une défense efficace contre un outil comme Hydra ?
5. **Vitesse et Verrouillage :** Hydra peut tester des centaines de mots de passe par seconde. Si le serveur ajoutait un délai de 2 secondes entre chaque tentative ou bloquait le compte après 5 échecs, l'attaque resterait-elle réaliste ?
6. **L'ultime rempart :** Même si un attaquant possède un dictionnaire parfait et que le serveur est vulnérable, quelle technologie (souvent utilisée sur vos comptes personnels) rendrait la découverte du mot de passe totalement inutile pour l'attaquant ?