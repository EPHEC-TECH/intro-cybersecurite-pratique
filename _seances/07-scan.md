---
layout: default
title: Reconnaissance Réseau
order: 7
description: OSINT, NMAP, TCP Handshake
nav_order: 7
published: true
nav_exclude: true
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

- Collecter des informations sur une cible de manière **passive** (OSINT), sans envoyer de paquets directement vers elle.
- Expliquer le fonctionnement du **TCP Three-Way Handshake** et son lien avec la détection de ports.
- Utiliser **Nmap** pour scanner une cible et interpréter les résultats.
- Distinguer un port **ouvert**, **fermé** et **filtré**.
- Dresser une "fiche identité" d'une machine distante à partir d'informations publiques et de scans.

---

## Introduction : voir avant d'agir

Avant toute attaque, un attaquant commence par la **reconnaissance** : collecter un maximum d'informations sur sa cible, idéalement sans déclencher d'alarme.

Cette phase se divise en deux grandes étapes :

| Phase | Description | Contact direct avec la cible ? |
|---|---|---|
| **OSINT passif** | Exploitation de sources publiques (DNS, Shodan, WHOIS…) | ❌ Non |
| **Scan actif** | Envoi de paquets vers la cible pour découvrir ses services | ✅ Oui |

> ⚠️ **Rappel légal :** Scanner un système sans autorisation est illégal dans la plupart des pays (en Belgique : loi du 28 novembre 2000 sur la criminalité informatique). Dans ce TP, nous utilisons **uniquement** `scanme.nmap.org`, un serveur mis à disposition par les créateurs de Nmap **explicitement** pour l'apprentissage.
>
> Source : [https://scanme.nmap.org](https://scanme.nmap.org) — *"You are authorized to scan this machine with Nmap or other port scanners."*

---

## Partie 1 — OSINT : reconnaissance passive

{: .d-inline-block }
Durée estimée : 15–20 min
{: .label .label-yellow }

{: .highlight }
> **Aucune installation requise.** Tout se fait depuis un navigateur web et le terminal Linux.

### Qu'est-ce que l'OSINT ?

L'**Open Source Intelligence** (OSINT) désigne la collecte d'informations à partir de sources **publiquement accessibles** : DNS, WHOIS, moteurs de recherche spécialisés, réseaux sociaux, certificats TLS…

Avant même de toucher une cible, une quantité considérable d'informations la concernant est déjà publique. C'est le point de départ de toute reconnaissance sérieuse.

---

### Exercice 1 — Qui est `scanme.nmap.org` ?

#### Étape 1 — Résolution DNS

Depuis votre terminal Linux :

```bash
dig scanme.nmap.org
```

La réponse se trouve dans la section `ANSWER SECTION` — cherchez la ligne avec le type `A` qui contient l'adresse IPv4.

Sur Windows (PowerShell ou CMD) :
```
nslookup scanme.nmap.org
```

{: .note }
> `dig` envoie une requête à votre résolveur DNS (souvent votre FAI ou 8.8.8.8), qui contacte ensuite les serveurs DNS de `nmap.org`. Vous n'envoyez rien *directement* à la cible, mais cette requête laisse des traces chez les intermédiaires — c'est une reconnaissance indirecte, pas totalement invisible.

Vérifiez dans quel pays est hébergée l'adresse IP obtenue : [https://ipinfo.io](https://ipinfo.io)

---

#### Étape 2 — WHOIS

Rendez-vous sur [https://whois.domaintools.com/nmap.org](https://whois.domaintools.com/nmap.org) (ou `whois nmap.org` dans le terminal).

Notez qui est l'organisation propriétaire du domaine et depuis quand il est enregistré.

---

#### Étape 3 — Shodan

Avant de chercher votre cible, prenez 2 minutes pour mesurer l'étendue de ce que Shodan indexe. Rendez-vous sur [https://www.shodan.io](https://www.shodan.io) et essayez :

```
webcam country:BE
```

```
org:EPHEC
```

Cherchez ensuite votre cible :

```
scanme.nmap.org
```

{: .note }
> Shodan est un moteur de recherche qui scanne en permanence l'ensemble d'Internet et indexe les services exposés (serveurs web, SSH, bases de données, caméras IP, IoT…). Il ne scanne pas à votre demande — il vous montre ce qu'il a **déjà collecté**. Vous n'envoyez rien vers la cible.
>
> Source : [Shodan — The Search Engine for the Internet of Things](https://www.shodan.io/about/products)

{: .warning }
> L'historique complet n'est visible qu'avec un compte payant. Avec le compte gratuit, vous voyez la dernière capture et les ports principaux — c'est suffisant.

---

#### Synthèse OSINT

Complétez ce tableau **avant** de lancer Nmap :

| Champ | Valeur |
|---|---|
| Adresse IP | |
| Propriétaire du domaine | |
| Pays d'hébergement | |
| Ports déjà connus (Shodan) | |
| Services détectés (Shodan) | |

Gardez ce tableau sous la main — vous le compléterez avec les résultats Nmap à la fin.

---

## Partie 2 — Comprendre Nmap : le TCP Three-Way Handshake

{: .d-inline-block }
Durée estimée : 10 min
{: .label .label-green }

Avant de lancer Nmap, il faut comprendre ce qu'il mesure réellement — et pour cela, comprendre comment TCP établit (ou n'établit pas) une connexion.

### Le Three-Way Handshake TCP

Lorsqu'un client veut se connecter à un serveur, TCP utilise un mécanisme en 3 étapes :

```
Client                    Serveur
  |                          |
  |-------- SYN ----------->|   "Je veux me connecter au port X"
  |                          |
  |<------- SYN-ACK ---------|   "OK, je suis là" (port OUVERT)
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

Notez que l'état **filtré** ne permet pas de savoir si un service écoute derrière — c'est précisément l'intention d'un pare-feu bien configuré.

---

### Le Scan SYN (`-sS`) : la demi-connexion

Le scan par défaut de Nmap (avec sudo) est le **SYN scan**, qui n'établit jamais la connexion TCP complète :

```
Nmap                      Serveur
  |                          |
  |-------- SYN ----------->|
  |                          |
  |<------- SYN-ACK ---------|   (port ouvert détecté ✓)
  |                          |
  |-------- RST ----------->|   Nmap interrompt ici
```

**Ce que cela signifie concrètement :**
- L'**application** serveur (Apache, SSH…) ne voit jamais de connexion établie — elle ne la loggue pas.
- En revanche, le **système d'exploitation** du serveur et les **équipements réseau** (firewall, IDS) voient les SYN entrants et peuvent les détecter. Un SYN scan n'est pas invisible — il est simplement moins bruyant qu'une connexion complète.

> ⚠️ Le SYN scan nécessite **sudo** car il manipule directement les paquets réseau (raw sockets).

> Source : [Nmap Book — Port Scanning Techniques](https://nmap.org/book/man-port-scanning-techniques.html)

---

## Partie 3 — Nmap en pratique

{: .d-inline-block }
Durée estimée : 25–30 min
{: .label .label-yellow }

{: .highlight }
> **Outil requis :** Nmap. Vérifiez : `which nmap`
> Si absent : `sudo apt install nmap`
>
> **Cible :** `scanme.nmap.org` — seul host autorisé pour ce TP.

---

### Exercice 2 — Scan progressif

#### Étape 1 — Scan de base

```bash
nmap scanme.nmap.org
```

Observez la sortie : quels ports sont ouverts, quels services leur sont associés (colonne `SERVICE`), combien de ports ont été scannés au total (ligne de résumé en bas).

---

#### Étape 2 — Détection des versions de services

```bash
nmap -sV scanme.nmap.org
```

Notez les versions des services détectés (colonne `VERSION`). Certaines peuvent être indéterminées.

{: .note }
> `-sV` établit de vraies connexions aux services ouverts et leur envoie des "sondes" pour identifier le logiciel et sa version. C'est plus lent et plus visible qu'un SYN scan simple. Comptez 1–3 minutes.

---

#### Étape 3 — Détection du système d'exploitation

```bash
sudo nmap -O scanme.nmap.org
```

Nmap tente d'identifier l'OS en analysant les particularités de l'implémentation TCP/IP de la cible : valeur du TTL, taille de la fenêtre TCP, options activées. Chaque système d'exploitation a ses propres "empreintes" dans ces paramètres. Nmap peut proposer plusieurs candidats avec un niveau de confiance variable.

---

#### Étape 4 — Scan agressif

```bash
sudo nmap -A scanme.nmap.org
```

Le flag `-A` combine la détection d'OS (`-O`), la détection de versions (`-sV`), les scripts NSE par défaut (`-sC`) et un traceroute. La sortie est plus riche mais le scan est nettement plus visible sur le réseau.

{: .note }
> Comptez 3–5 minutes pour ce scan.

---

### Exercice 3 — La "fiche identité" de la cible

Complétez ce tableau en croisant vos résultats OSINT et Nmap :

| Champ | Source | Valeur |
|---|---|---|
| Adresse IP | DNS | |
| Propriétaire du domaine | WHOIS | |
| Système d'exploitation | Nmap `-O` | |
| Ports ouverts (top 1000) | Nmap défaut | |
| Version SSH | Nmap `-sV` | |
| Version serveur web | Nmap `-sV` | |
| Données déjà connues avant le scan | Shodan | |

En tant qu'administrateur de ce serveur : lequel de ces éléments vous inquiéterait le plus si un inconnu l'avait collecté ? Que feriez-vous pour limiter cette exposition ?

---

## Voir les paquets avec Wireshark

{: .d-inline-block }
Optionnel
{: .label .label-blue }

Ouvrez Wireshark sur votre interface réseau principale **avant** de lancer le scan. Appliquez ce filtre :

```
tcp and host scanme.nmap.org
```

Puis lancez :

```bash
sudo nmap -sS scanme.nmap.org
```

Observez les échanges SYN / SYN-ACK / RST et comparez avec le schéma de la partie 2. Pour les ports filtrés, notez ce que Wireshark affiche — ou n'affiche pas.

---

## Questions de synthèse

1. Quelle est la différence fondamentale entre la reconnaissance passive (OSINT) et le scan actif (Nmap) du point de vue de la détection par la cible ?

2. Un port est marqué **filtré** par Nmap. Peut-on en déduire qu'aucun service n'écoute derrière ?

3. Vous scannez un serveur et relevez qu'il tourne Apache 2.2.14 sur le port 80. En quoi cette information est-elle problématique pour l'administrateur ?

4. Quelles mesures un administrateur peut-il mettre en place pour réduire les informations qu'un scan Nmap révèle sur son serveur ?

---

## Ressources

- [Nmap Book (officiel)](https://nmap.org/book/man.html) — Manuel complet de Nmap
- [Nmap Tutorial — HackerTarget](https://hackertarget.com/nmap-tutorial/) — Tutoriel avec explication du Three-Way Handshake
- [Shodan](https://www.shodan.io) — Moteur de recherche OSINT
- [RFC 793 — TCP](https://www.rfc-editor.org/rfc/rfc793) — Spécification originale du handshake TCP
- [scanme.nmap.org](https://scanme.nmap.org) — Cible officielle autorisée
- Cheatsheet Nmap complète : [ressources/seance7/nmap-cheatsheet.md](../ressources/seance7/nmap-cheatsheet.md)
