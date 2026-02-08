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

## 3. Premier accès à la cible

Même si le site tourne "dans Docker", il est accessible depuis le navigateur de votre VM.

1.  Ouvrez **Firefox** dans votre VM.
2.  Accédez à l'adresse : [http://localhost](http://localhost)
3.  Si c'est votre première connexion, allez sur [http://localhost/setup](http://localhost/setup) et cliquez sur le bouton **"Create / Reset Database"** en bas de page.
4.  Connectez-vous avec les identifiants par défaut :
    *   **Username :** `admin`
    *   **Password :** `password`

Une fois connecté, allez dans l'onglet **"DVWA Security"** dans le menu de gauche et vérifiez que le niveau est sur **"Low"**. Cliquez sur "Submit" pour valider.

---

## 4. Réglage du niveau de sécurité

Dans le menu de gauche → **DVWA Security**

Le niveau par défaut est *Impossible*. Pour les exercices de compréhension, choisir un niveau faible :
**Security Level : Low** ou **Medium**

---

## 6. Installation de Hydra (version graphique)

Dans le terminal :

```bash
sudo apt update
sudo apt install hydra-gtk
```

Hydra est un outil qui permet de comprendre les risques d’un formulaire dépourvu de protections anti-automatisation.

---

## 7. Comprendre les attaques par force brute

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