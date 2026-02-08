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

Apprendre à analyser et comprendre le fonctionnement d'une attaque par dictionnaire sur une application web. Vous allez utiliser un environnement sécurisé pour observer comment un attaquant peut automatiser des milliers d'essais de mots de passe pour forcer un accès.

---

## 1. Architecture du laboratoire

Pour ce TP, nous allons utiliser une architecture spécifique car les PC de l'école ne permettent pas de lancer directement les outils d'attaque.

1.  **Votre PC (Windows) :** L'hôte physique.
2.  **La VM (Linux Ubuntu) :** Votre poste de travail. C'est ici que vous lancerez vos outils (Navigateur, Hydra).
3.  **Le Conteneur Docker (DVWA) :** Une "mini-machine" isolée qui tourne *à l'intérieur* de votre VM et qui contient le site web vulnérable que nous allons attaquer.

> **Note sur Docker :** Considérez Docker comme un système permettant de lancer une application (ici, un site web) avec toutes ses dépendances en une seule ligne de commande, sans rien installer de complexe sur la VM.

---

## 2. Préparation de l’environnement
> **Note 1:** On utilisera ce setup pour de prochain TP également, donc assurez vous de comprendre ce que vous faites (pour le reproduire aux prochains TP)

> **Note 2:** Si vous voulez utiliser votre ordinateur, on vous conseille d'installer docker (ne le faite pas au TP, vous n'avez pas le temps) ou d'utiliser une VM linux qui a déjà docker installé (docker sera vu en profondeur l'année prochaine, en Admin 2)


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
> 1. **La Méthode :** Dans l'onglet "En-têtes" (Headers), vérifiez si c'est du **GET** ou du **POST**. *(Note : DVWA utilise souvent GET ici, ce qui expose le mot de passe dans l'URL !)*.
> 2. **Les Paramètres :** Trouvez les noms exacts des variables envoyées (ex: `username`, `password`, `Login`).
> 3. **Le Cookie :** Trouvez la ligne `Cookie`. Vous verrez `PHPSESSID=...` et `security=low`. 
>    * **Notez votre PHPSESSID.** Hydra en aura besoin pour simuler votre session.
> 4. **Le Message d'échec :** Quel texte exact s'affiche en rouge sur la page après l'erreur ? (ex: `Username and/or password incorrect.`). 
>    * Hydra utilisera ce texte pour savoir qu'il s'est trompé.

---

## 4. Phase de "Weaponization" (Préparation du dictionnaire)

Une attaque par dictionnaire n'est efficace que si vos "munitions" (les mots de passe à tester) sont pertinentes. Au lieu d'utiliser un fichier de 14 millions de lignes, nous allons créer notre propre liste ciblée.

### 4.1. Créer sa liste de mots de passe
1. Ouvrez un terminal dans votre VM.
2. Créez un fichier nommé `pass.txt` avec l'éditeur de texte `nano` :
   ```bash
   nano pass.txt
   ```
3. Tapez une dizaine de mots de passe, un par ligne. Soyez créatifs, mais **insérez le mot de passe "password"** quelque part dans la liste (pour être sûr que l'attaque réussisse).
   * *Exemple :* `123456`, `azerty`, `admin`, `password`, `soleil`, `matin123`...
4. Sauvegardez et quittez (`Ctrl+O`, `Entrée`, puis `Ctrl+X`).

---

## 5. L'Attaque avec Hydra (Ligne de commande)

Hydra est l'un des outils les plus puissants pour automatiser les tentatives de connexion sur de nombreux protocoles (HTTP, SSH, FTP, etc.).

### 5.1. Installer Hydra
Si ce n'est pas déjà fait, installez l'outil dans votre VM :
```bash
sudo apt update && sudo apt install hydra -y
```

### 5.2. Construire la commande
Lancer une attaque sur un formulaire web demande une syntaxe très précise. Voici à quoi elle ressemble (à adapter avec vos infos) :

```bash
hydra -l admin -P pass.txt localhost http-get-form "/vulnerabilities/brute/:username=^USER^&password=^PASS^&Login=Login:F=Username and/or password incorrect.:H=Cookie: PHPSESSID=VOTRE_COOKIE; security=low"
```

**Explication des paramètres :**
*   `-l admin` : On cible l'utilisateur `admin`.
*   `-P pass.txt` : On utilise notre liste de mots de passe.
*   `localhost` : La cible (notre Docker).
*   `http-get-form` : Le module Hydra pour les formulaires envoyés en GET.
*   `"/vulnerabilities/brute/..."` : L'URL et les paramètres (séparés par des `:`).
    *   `^USER^` et `^PASS^` seront remplacés par Hydra.
    *   `F=...` : Le message d'échec (**F**ailed).
    *   `H=Cookie: ...` : On passe notre cookie de session pour avoir accès à la page.

---

## 6. Comprendre les attaques par force brute (Synthèse)

Une attaque par force brute repose sur le principe suivant :
> **Essayer automatiquement un très grand nombre de combinaisons jusqu’à trouver la bonne.**

Plus le mot de passe est court, simple ou récurrent, plus l’attaque sera rapide.

**Facteurs importants :**
*   Vitesse de réponse du serveur
*   Absence de protections
*   Structure des requêtes HTTP

---

## 8. Types d’attaques par force brute (synthèse)

| Type d’attaque | Description |
| :--- | :--- |
| **Simple brute force** | Teste toutes les combinaisons possibles. |
| **Hybrid brute force** | Mélange logique + variations systématiques. |
| **Dictionary attack** | Utilise une liste de mots de passe plausibles. |
| **Rainbow table** | Tente de retrouver un mot de passe à partir d’un hash. |
| **Reverse brute force** | Un mot de passe contre beaucoup d’utilisateurs. |
| **Credential stuffing** | Réutilise des identifiants volés. |

*Source : Fortinet – Attaque par force brute*

---

## 9. Outils connus pour analyser ou comprendre ces attaques

*   **Hydra**
*   **John the Ripper**
*   **Hashcat**
*   **Aircrack-ng**
*   **Ncrack**
*   **L0phtCrack**

Chaque outil illustre une catégorie d’attaque ou de test de résistance.

---

## 10. Défenses essentielles contre la force brute

| Défense | Effet |
| :--- | :--- |
| **Mots de passe forts** | Rend le dictionnaire inefficace. |
| **Limitation des tentatives** | Bloque après X échecs. |
| **CAPTCHA** | Empêche l’automatisation. |
| **MFA (2FA)** | Ajoute un facteur impossible à deviner. |
| **Verrouillage temporaire** | Ralentit drastiquement les essais. |