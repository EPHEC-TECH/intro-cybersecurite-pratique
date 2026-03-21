# Nmap Cheatsheet — Commandes Essentielles pour Débutants

Voici une sélection des commandes Nmap les plus utiles pour un étudiant débutant en cybersécurité.

## 1. Scan de base (découverte d'hôtes et de ports)

- **Scan basique d'une IP ou d'un hôte :**
  `nmap 192.168.1.1`
  `nmap exemple.com`
  *(Détecte les ports ouverts sur la cible)*

- **Scan de plusieurs adresses IP :**
  `nmap 192.168.1.1 192.168.1.2`
  `nmap 192.168.1.1,2,3` (scanne 192.168.1.1, .2, .3)

- **Scan de plages d'adresses IP (CIDR ou étendue) :**
  `nmap 192.168.1.0/24`
  `nmap 192.168.1.1-254`

- **Scan des 1000 ports les plus courants (par défaut) :**
  `nmap <cible>` (Pas besoin de flag, c'est le comportement par défaut)

- **Scan de ports spécifiques :**
  `nmap -p 80,443 <cible>`
  `nmap -p 20-100 <cible>`

- **Scan de tous les ports (65535) :**
  `nmap -p- <cible>`
  *(Attention, cela peut prendre beaucoup de temps !)*

## 2. Détection d'hôtes

- **Ping Scan (découverte d'hôtes actifs, sans scan de ports) :**
  `sudo nmap -sn 192.168.1.0/24`
  *(Le `sudo` est recommandé pour une meilleure précision, `-sn` désactive le scan de ports)*

## 3. Détection de services et de versions

- **Détection des versions des services sur les ports ouverts :**
  `sudo nmap -sV <cible>`
  *(Permet d'identifier le nom et la version des applications écoutant sur les ports)*

## 4. Détection du système d'exploitation (OS)

- **Détection du système d'exploitation de la cible :**
  `sudo nmap -O <cible>`
  *(Nmap tente de deviner l'OS en analysant les réponses TCP/IP)*

## 5. Scan agressif (complet)

- **Scan agressif (OS, versions, scripts par défaut, traceroute) :**
  `sudo nmap -A <cible>`
  *(Combine plusieurs options pour un rapport détaillé, inclut `-O`, `-sV`, `-sC`)*

## 6. Nmap Scripting Engine (NSE)

- **Lancer les scripts de détection de vulnérabilités par défaut :**
  `sudo nmap --script vuln <cible>`
  *(Utilise les scripts NSE pour chercher des vulnérabilités connues)*

## 7. Gestion du temps et "discrétion"

- **Utiliser des templates de timing (de T0 à T5) :**
  `sudo nmap -T4 <cible>`
  - `T0`: Paranoïaque (très lent)
  - `T1`: Furtif (lent)
  - `T2`: Poli (modéré)
  - `T3`: Normal (par défaut)
  - `T4`: Agressif (rapide, peut surcharger certains réseaux)
  - `T5`: Très agressif (très rapide, risque élevé de rater des infos ou de planter des services)
  *( `-T4` est souvent utilisé sur des réseaux de confiance pour la vitesse )*

- **Désactiver la résolution DNS (accélère le scan) :**
  `nmap -n <cible>`

## 8. Sauvegarde des résultats

- **Sauvegarder les résultats dans un fichier texte :**
  `nmap -oN scan_results.txt <cible>`

- **Sauvegarder les résultats en format XML :**
  `nmap -oX scan_results.xml <cible>`

- **Sauvegarder les résultats dans tous les formats (-oN, -oX, -oG) :**
  `nmap -oA all_formats <cible>`
  *(Crée `all_formats.nmap`, `all_formats.xml`, `all_formats.gnmap`)*

## 9. Types de scans TCP/UDP

- **Scan TCP SYN (Stealth Scan) :**
  `sudo nmap -sS <cible>`
  *(Plus discret, ne complète pas la connexion TCP. Nécessite `sudo`.)*

- **Scan TCP Connect :**
  `nmap -sT <cible>`
  *(Complète la connexion TCP, plus bruyant, pas besoin de `sudo`.)*

- **Scan UDP :**
  `sudo nmap -sU <cible>`
  *(Pour les services UDP comme DNS, DHCP. Nécessite `sudo`.)*

## Rappel Important
- **Toujours obtenir l'autorisation** avant de scanner un réseau qui ne vous appartient pas.
- `scanme.nmap.org` est une cible légale pour s'entraîner.
- L'utilisation de `sudo` est souvent nécessaire pour les scans avancés de Nmap qui manipulent les paquets réseau.
