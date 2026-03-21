---
layout: default
title: Reconnaissance Réseau
order: 7
description: OSINT, NMAP, TCP Handshake
nav_order: 7
published: false
---

# Séance 7 : Reconnaissance & Scan Réseau
{: .no_toc }

## Table des matières
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Objectifs pédagogiques

À la fin de la séance, l'étudiant sera capable de :

- Collecter des informations sur une cible de manière **passive** (OSINT), sans envoyer de paquets vers elle.
- Expliquer le fonctionnement du **TCP Three-Way Handshake** et son lien avec la détection de ports.
- Utiliser **Nmap** pour scanner une cible et interpréter les résultats.
- Distinguer un port **ouvert**, **fermé** et **filtré**.
- Dresser une "fiche identité" d'une machine distante à partir d'informations publiques.

---

## Introduction : voir sans être vu

Avant toute attaque, un attaquant commence par la **reconnaissance** : collecter un maximum d'informations sur sa cible, idéalement sans déclencher d'alarme.

Cette phase se divise en deux grandes étapes :

| Phase | Description | Interaction réseau ? |
|---|---|---|
| **OSINT passif** | Exploitation de sources publiques (DNS, Shodan, WHOIS…) | ❌ Aucune |
| **Scan actif** | Envoi de paquets vers la cible pour découvrir ses services | ✅ Oui |

> ⚠️ **Rappel légal :** Scanner un système sans autorisation est illégal dans la plupart des pays (en Belgique : loi du 28 novembre 2000 sur la criminalité informatique). Dans ce TP, nous utilisons **uniquement** `scanme.nmap.org`, un serveur mis à disposition par les créateurs de Nmap **explicitement** pour l'apprentissage.
>
> Source : [https://scanme.nmap.org](https://scanme.nmap.org) — *"You are authorized to scan this machine with Nmap or other port scanners."*

---

## Partie 1 — OSINT : reconnaissance passive

{: .d-inline-block }
Durée estimée : 10–15 min
{: .label .label-yellow }

{: .highlight }
> **Aucune installation requise.** Tout se fait depuis un navigateur web et le terminal Linux.

### Qu'est-ce que l'OSINT ?

L'**Open Source Intelligence** (OSINT) désigne la collecte d'informations à partir de sources **publiquement accessibles** : DNS, WHOIS, moteurs de recherche spécialisés, réseaux sociaux, certificats TLS…

L'idée clé : **avant même de toucher une cible, une quantité considérable d'informations la concernant est déjà publique**.

---

### Exercice 1 — Qui est `scanme.nmap.org` ? (sans toucher le serveur)

#### Étape 1 — Résolution DNS

Depuis votre terminal Linux, sans rien envoyer au serveur cible :

```bash
nslookup scanme.nmap.org
```

> ❓ Quelle est l'adresse IP de `scanme.nmap.org` ? Dans quel pays/réseau est-elle hébergée (vous pouvez vérifier sur [https://ipinfo.io](https://ipinfo.io)) ?

---

#### Étape 2 — WHOIS : qui possède ce domaine ?

Rendez-vous sur [https://whois.domaintools.com/nmap.org](https://whois.domaintools.com/nmap.org) (ou utilisez `whois nmap.org` dans le terminal).

> ❓ Qui est l'organisation propriétaire du domaine `nmap.org` ? Depuis quand est-il enregistré ?

---

#### Étape 3 — Shodan : ce que l'internet "sait" déjà

Rendez-vous sur [https://www.shodan.io](https://www.shodan.io) (compte gratuit suffisant) et recherchez :

```
scanme.nmap.org
```

> ❓ Quels ports et services Shodan a-t-il déjà indexés ? Depuis quand ce serveur est-il connu de Shodan ?
>
> ❓ Shodan vous donne-t-il des informations sur les versions des services ? Lesquelles ?

{: .note }
> **Shodan en quelques mots :** C'est un moteur de recherche qui scanne en permanence l'ensemble d'Internet et indexe les services exposés (web, SSH, bases de données, caméras IP, etc.). Il ne scanne pas à votre demande — il vous montre ce qu'il a **déjà collecté**. C'est pourquoi c'est de l'OSINT **passif** de votre côté.
>
> Source : [Shodan — The Search Engine for the Internet of Things](https://www.shodan.io/about/products)

---

#### Synthèse OSINT

Complétez ce tableau uniquement avec les informations OSINT (sans avoir lancé Nmap) :

| Champ | Valeur |
|---|---|
| Adresse IP | |
| Propriétaire du domaine | |
| Pays d'hébergement | |
| Ports déjà connus (Shodan) | |
| Services détectés (Shodan) | |

> 💡 **Conclusion :** Sans envoyer le moindre paquet vers la cible, vous disposez déjà d'un profil partiel. Un attaquant patient peut construire ce profil sans déclencher aucune alerte.

---

## Partie 2 — Comprendre Nmap : le TCP Three-Way Handshake

{: .d-inline-block }
Durée estimée : 5–10 min
{: .label .label-green }

Avant d'utiliser Nmap, il est essentiel de comprendre **ce qu'il mesure réellement** — et pour cela, il faut comprendre comment TCP établit (ou n'établit pas) une connexion.

### Le Three-Way Handshake TCP

Lorsqu'un client veut se connecter à un serveur, TCP utilise un mécanisme en 3 étapes :

```
Client                    Serveur
  |                          |
  |-------- SYN ----------->|   "Je veux me connecter au port X"
  |                          |
  |<------- SYN-ACK ---------|   "OK, je suis là, je t'attends" (port OUVERT)
  |                          |
  |-------- ACK ----------->|   "Reçu. Connexion établie."
  |                          |
```

> Source : RFC 793 — [https://www.rfc-editor.org/rfc/rfc793](https://www.rfc-editor.org/rfc/rfc793)

---

### Ce que Nmap "voit" selon la réponse

Nmap envoie un paquet **SYN** et analyse la réponse pour déterminer l'état du port :

| Réponse reçue | État du port | Signification |
|---|---|---|
| `SYN-ACK` | **Ouvert** | Un service écoute et répond |
| `RST` (Reset) | **Fermé** | Rien n'écoute sur ce port |
| Pas de réponse / `ICMP unreachable` | **Filtré** | Un pare-feu bloque le trafic |

---

### Le Scan SYN (`-sS`) : furtivité par demi-connexion

Le scan le plus courant de Nmap, appelé **SYN scan** ou *stealth scan*, exploite le handshake de manière incomplète :

```
Nmap                      Serveur
  |                          |
  |-------- SYN ----------->|
  |                          |
  |<------- SYN-ACK ---------|   (port ouvert détecté ✓)
  |                          |
  |-------- RST ----------->|   Nmap coupe la connexion ici
  |                          |   (pas de connexion complète)
```

**Pourquoi c'est "furtif" ?** En n'envoyant jamais le `ACK` final, Nmap ne complète pas la connexion TCP. L'application serveur ne "voit" donc jamais une session ouverte — elle ne la loggue pas.

> ⚠️ Ce type de scan nécessite les droits **root/sudo** car il manipule directement les paquets réseau (raw sockets).

> Source : [Nmap Book — Port Scanning Techniques](https://nmap.org/book/man-port-scanning-techniques.html)

---

### Pour aller plus loin : UDP et les autres types de scan

{: .note }
> **À garder en tête (pas obligatoire pour ce TP) :**
>
> - **Scan TCP Connect** (`-sT`) : complète le handshake. Pas besoin de root, mais plus facilement détectable car une connexion réelle est établie.
> - **Scan UDP** (`-sU`) : UDP n'a pas de handshake. Nmap envoie un paquet vide et attend un message d'erreur ICMP "port unreachable" pour détecter les ports fermés. Très lent.
>
> ❓ *(Question ouverte pour la séance : vaut-il la peine d'introduire les scans UDP ? Trop complexe pour le public ?)*

---

## Partie 3 — Nmap en pratique

{: .d-inline-block }
Durée estimée : 20–25 min
{: .label .label-yellow }

{: .highlight }
> **Outil requis :** Nmap. Vérifiez qu'il est disponible : `which nmap`
> Si absent : `sudo apt install nmap`
>
> **Cible :** `scanme.nmap.org` — seul host autorisé pour ce TP.

---

### Exercice 2 — Scan progressif

#### Étape 1 — Scan de base

```bash
nmap scanme.nmap.org
```

> ❓ Quels ports sont **ouverts** ? Quels services leur sont associés par défaut (colonne `SERVICE`) ?
>
> ❓ Combien de ports Nmap a-t-il scanné par défaut ? (Lisez la ligne de résumé en bas)

---

#### Étape 2 — Détection des versions de services

```bash
nmap -sV scanme.nmap.org
```

> ❓ Quelle version du serveur SSH tourne ? (colonne `VERSION`)
>
> ❓ Quelle version du serveur web Apache ?
>
> ❓ Y a-t-il un service dont la version est marquée comme inconnue ou difficile à détecter ?

{: .note }
> La détection de version (`-sV`) établit une vraie connexion aux services ouverts et leur envoie des "sondes" pour identifier le logiciel et sa version. C'est plus bruyant qu'un simple SYN scan.

---

#### Étape 3 — Détection du système d'exploitation

```bash
sudo nmap -O scanme.nmap.org
```

> ❓ Quel système d'exploitation Nmap devine-t-il ?
>
> ❓ Avec quelle précision (pourcentage) ?
>
> ❓ Comment Nmap peut-il "deviner" l'OS sans y avoir accès ? *(Réponse attendue : en analysant les particularités de l'implémentation TCP/IP — TTL, taille de fenêtre, options TCP — propres à chaque OS)*

---

#### Étape 4 — Scan de tous les ports

```bash
nmap -p- scanme.nmap.org
```

> ⚠️ Ce scan peut prendre 5–10 minutes. Lancez-le et passez à la suite pendant qu'il tourne.
>
> ❓ Y a-t-il des ports ouverts **inattendus** que le scan de base n'avait pas trouvés ?
>
> ❓ Pourquoi Nmap ne scanne-t-il pas tous les ports par défaut ?

---

#### Étape 5 — Scan agressif (combiné)

```bash
sudo nmap -A scanme.nmap.org
```

> ❓ Que combine le flag `-A` ? (Lisez la sortie : OS, versions, scripts NSE, traceroute)
>
> ❓ Quel est l'inconvénient du scan `-A` du point de vue de la discrétion ?

---

### Exercice 3 — La "fiche identité" de la cible

À partir de vos résultats OSINT (Partie 1) **et** Nmap (Partie 3), complétez cette fiche :

| Champ | Source | Valeur |
|---|---|---|
| Adresse IP | DNS / OSINT | |
| Propriétaire du domaine | WHOIS | |
| Système d'exploitation | Nmap `-O` | |
| Ports ouverts (top 1000) | Nmap défaut | |
| Ports ouverts (tous) | Nmap `-p-` | |
| Version SSH | Nmap `-sV` | |
| Version web server | Nmap `-sV` | |
| Données déjà connues (Shodan) | Shodan | |

> 💡 **Réflexion :** Imaginez être un administrateur système. Lequel de ces éléments vous inquiéterait le plus si votre serveur était scanné ainsi par un inconnu ? Lequel seriez-vous le plus surpris de voir exposé ?

---

## Bonus — Voir les paquets avec Wireshark

{: .d-inline-block }
Optionnel
{: .label .label-blue }

Si Wireshark est disponible, ouvrez-le **avant** de lancer le scan, sur votre interface réseau principale.

Filtre à appliquer dans Wireshark :
```
tcp and host scanme.nmap.org
```

Lancez ensuite :
```bash
sudo nmap -sS scanme.nmap.org
```

> ❓ Retrouvez-vous les échanges SYN → SYN-ACK → RST décrits dans la partie théorique ?
>
> ❓ Pour un port **filtré**, que voyez-vous (ou ne voyez-vous pas) dans Wireshark ?

> *(Question ouverte : est-ce que Wireshark est installé sur les VMs étudiants ? Si non, peut-on leur montrer une capture pré-enregistrée ?)*

---

## Pour aller plus loin

{: .note }
> Ces pistes sont **optionnelles** — à intégrer ou non selon le temps disponible et le niveau des étudiants.

### Nmap Scripting Engine (NSE)

Nmap intègre un moteur de scripts permettant d'aller au-delà du simple scan de ports :

```bash
# Recherche de vulnérabilités connues
sudo nmap --script vuln scanme.nmap.org

# Informations sur le certificat HTTPS
nmap --script ssl-cert -p 443 scanme.nmap.org
```

> ❓ *(À garder ou trop avancé pour une intro ? Cela pourrait faire le lien avec la séance 9 sur l'exploitation…)*

### Shodan avancé

Shodan supporte des requêtes avancées :

```
# Trouver des serveurs Apache en Belgique
apache country:BE

# Trouver des caméras IP exposées
webcam country:BE

# Serveurs avec des ports SSH ouverts sur une plage IP
port:22 net:193.190.0.0/16
```

> Source : [100+ Shodan Queries — osintme.com](https://osintme.com/index.php/2021/01/16/ultimate-osint-with-shodan-100-great-shodan-queries/)

---

## Questions de synthèse

1. Quelle est la différence fondamentale entre la **reconnaissance passive** (OSINT) et le **scan actif** (Nmap) du point de vue de la détection par la cible ?

2. Un port est marqué **filtré** par Nmap. Cela signifie-t-il qu'aucun service n'écoute derrière ? Ou qu'il est impossible de savoir ?

3. Vous scannez un serveur et trouvez qu'il tourne **Apache 2.2.14** sur le port 80. Pourquoi cette information est-elle potentiellement dangereuse ?

4. Vous êtes administrateur d'un serveur. Que pouvez-vous faire pour **limiter les informations** qu'un scan Nmap peut révéler ?

---

## Ressources

- [Nmap Book (officiel)](https://nmap.org/book/man.html) — Manuel complet de Nmap
- [Nmap Tutorial — HackerTarget](https://hackertarget.com/nmap-tutorial/) — Tutoriel couvrant le Three-Way Handshake et les types de scans
- [100+ Shodan Queries — osintme.com](https://osintme.com/index.php/2021/01/16/ultimate-osint-with-shodan-100-great-shodan-queries/) — Requêtes Shodan avancées
- [OSINT Cheat Sheet — GitHub Jieyab89](https://github.com/Jieyab89/OSINT-Cheat-sheet) — Collection d'outils et techniques OSINT
- [Pentesting 101: Shodan pour l'OSINT — INE](https://ine.com/blog/pentesting-101-using-shodan-for-cyber-security-technical-osint) — Introduction pratique à Shodan
- [RFC 793 — Transmission Control Protocol](https://www.rfc-editor.org/rfc/rfc793) — Spécification originale du TCP (référence pour le handshake)
- [scanme.nmap.org](https://scanme.nmap.org) — Cible officielle et légale pour les exercices Nmap
