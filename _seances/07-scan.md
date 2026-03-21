---
layout: default
title: Reconnaissance Réseau
order: 7
description: NMAP, Zenmap
nav_order: 7
published: false
---

# Séance 7 : Scan de Réseau

> **Fil conducteur :** *Comment un attaquant voit votre réseau ?*
> Vous allez jouer le rôle d'un attaquant qui découvre une cible à distance, sans autorisation d'accès préalable.

**Cible du TP :** `scanme.nmap.org` — serveur officiel Nmap, **explicitement autorisé** pour les scans d'apprentissage.

---

## Partie 1 — OSINT passif (sans toucher la cible)

L'OSINT (*Open Source Intelligence*) consiste à collecter des informations **publiquement disponibles**, sans envoyer le moindre paquet vers la cible.

### Exercice 1 — Qui est `scanme.nmap.org` ?

1. Rendez-vous sur [https://www.shodan.io](https://www.shodan.io) et recherchez `scanme.nmap.org`
   - Quels ports et services sont visibles ?
   - Depuis quand ce serveur est-il indexé ?

2. Effectuez une recherche WHOIS : [https://whois.domaintools.com/scanme.nmap.org](https://whois.domaintools.com/scanme.nmap.org)
   - Qui possède ce domaine ?
   - Où est hébergé le serveur ?

3. Résolution DNS depuis votre terminal Linux :
   ```bash
   nslookup scanme.nmap.org
   ```
   - Quelle est l'adresse IP du serveur ?

> 💡 **Conclusion :** Avant même de scanner une machine, un attaquant dispose déjà d'une quantité significative d'informations publiques.

---

## Partie 2 — Comprendre Nmap : le TCP Three-Way Handshake

Pour comprendre comment Nmap "voit" un port, il faut comprendre comment TCP établit une connexion.

### Le Three-Way Handshake TCP

```
Client          Serveur
  |                |
  |---- SYN ------>|   "Je veux me connecter"
  |                |
  |<-- SYN-ACK ----|   "OK, je suis là" (port OUVERT)
  |                |
  |---- ACK ------>|   "Reçu, connexion établie"
```

### Ce que Nmap en fait : le SYN Scan (`-sS`)

Nmap **n'envoie que le SYN** et analyse la réponse :

| Réponse reçue | Interprétation |
|---|---|
| `SYN-ACK` | Port **ouvert** — un service écoute |
| `RST` (Reset) | Port **fermé** — rien n'écoute |
| Pas de réponse | Port **filtré** — pare-feu bloque |

> 💡 **Pourquoi c'est "furtif" ?** En n'envoyant jamais le `ACK` final, Nmap ne complète pas la connexion TCP. L'application serveur ne loggue rien car aucune session n'a été ouverte.
>
> ⚠️ Ce type de scan (`-sS`) nécessite les droits **root/sudo**.

---

## Partie 3 — Nmap en pratique

### Vérifier que Nmap est disponible

```bash
which nmap
nmap --version
```

Si absent : `sudo apt install nmap`

### Exercice 2 — Scan progressif de `scanme.nmap.org`

**Étape 1 — Scan basique** (ports les plus courants)
```bash
nmap scanme.nmap.org
```
- Quels ports sont ouverts ?
- Quels services sont associés à ces ports ?

**Étape 2 — Détection de version des services**
```bash
nmap -sV scanme.nmap.org
```
- Quelle version du serveur SSH tourne ?
- Quelle version du serveur web ?

**Étape 3 — Détection du système d'exploitation**
```bash
sudo nmap -O scanme.nmap.org
```
- Quel OS tourne sur ce serveur ?

**Étape 4 — Scan complet (tous les ports)**
```bash
nmap -p- scanme.nmap.org
```
- Y a-t-il des ports ouverts inattendus ?

### Exercice 3 — Synthèse : la "fiche identité" de la cible

À partir de vos découvertes OSINT + Nmap, complétez cette fiche :

| Champ | Valeur |
|---|---|
| Adresse IP | |
| Propriétaire (WHOIS) | |
| Système d'exploitation | |
| Ports ouverts | |
| Services détectés | |
| Versions des services | |

---

## Bonus — Visualiser les paquets avec Wireshark

Si Wireshark est disponible, lancez une capture sur votre interface réseau **pendant** un scan Nmap :

```bash
sudo nmap -sS scanme.nmap.org
```

Filtrez dans Wireshark : `tcp and host scanme.nmap.org`

Observez les échanges SYN / SYN-ACK / RST et comparez avec la théorie du handshake.

---

## Ressources

- [https://nmap.org/book/man.html](https://nmap.org/book/man.html) — Manuel officiel Nmap
- [https://shodan.io](https://shodan.io) — Moteur de recherche OSINT
- [https://scanme.nmap.org](https://scanme.nmap.org) — Page officielle de la cible autorisée
