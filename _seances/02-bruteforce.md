---
layout: default
title: Brute Force & Dictionnaire
order: 2
description: Analyse d'attaque par dictionnaire sur DVWA
nav_order: 2
has_children: false
---

# Séance 2 : Analyse et compréhension d'une attaque par dictionnaire sur DVWA

{: .no_toc }

## Objectif
{: .no_toc .text-delta }

Apprendre à analyser et comprendre comment fonctionne une attaque par dictionnaire sur une application web vulnérable (DVWA), en utilisant un environnement isolé et sécurisé. Ce laboratoire a pour but d’expliquer les concepts et la démarche, dans une optique défensive et pédagogique.

---

## 1. Présentation du laboratoire

Dans ce laboratoire, vous travaillez sur une machine Linux vulnérable appelée **Metasploitable**, sur laquelle tourne l’application web **DVWA** (Damn Vulnerable Web Application). 
DVWA est une application volontairement vulnérable, destinée à la formation et à la recherche en cybersécurité. Elle contient de nombreuses failles simulées, dont des faiblesses au niveau du formulaire d’authentification.

L’objectif principal du lab est de comprendre comment une attaque par dictionnaire peut fonctionner, en étudiant :
*   Le fonctionnement d’un formulaire d’authentification web
*   Les mesures de sécurité absentes ou insuffisantes
*   Le rôle d’outils de tests de sécurité comme Burp Suite
*   Le comportement d’un outil d’automatisation d’essais (**Hydra**)

Ce lab fait partie d’une série consacrée aux fondamentaux de la cybersécurité réseaux.

---

## 2. Objectifs pédagogiques

À la fin de ce laboratoire, vous serez capable de :

*   ✔️ **Comprendre** comment un attaquant explore un formulaire de connexion via l’interception et l’analyse des requêtes avec Burp Suite.
*   ✔️ **Décrire** les principes d’une attaque par dictionnaire et expliquer pourquoi les mots de passe faibles sont vulnérables.
*   ✔️ **Analyser** comment un outil automatisé (Hydra) cible un service web (dans un environnement isolé), afin de comprendre les risques.
*   ✔️ **Identifier** les contre-mesures essentielles pour stopper ces attaques :
    *   Mots de passe robustes
    *   Limitation des tentatives
    *   Verrouillage temporaire
    *   Filtres CAPTCHA
    *   Authentification multifactorielle (MFA)
    *   Gestion sécurisée des sessions

---

## 3. Préparation de l’environnement

### 3.1. Cloner et configurer la machine

1.  Cloner la machine **“system admin 2024”**.
2.  Ouvrir **Manage** → **Clone** et renommer la nouvelle VM.
3.  Vérifier que **Docker** est installé dans cette VM.

---

## 4. Lancement de DVWA

Ouvrez un terminal dans la machine, puis exécutez :

```bash
docker run -it -p 80:80 vulnerables/web-dvwa
```

Ensuite :
1.  Lancer **Firefox**
2.  Accéder à : [http://localhost/setup](http://localhost/setup)
3.  Cliquer sur **Create / Reset Database**

**Identifiants DVWA par défaut :**
*   **Username :** `admin`
*   **Password :** `password`

Vous pouvez maintenant accéder au menu principal.

---

## 5. Réglage du niveau de sécurité

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