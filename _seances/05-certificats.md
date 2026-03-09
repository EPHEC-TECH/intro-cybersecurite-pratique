---
layout: default
title: Pratique & Certificats
order: 5
description: Diffie-Hellman, SSH, TLS, Wireshark
nav_order: 5
published: false
---

# Séance 5 : Mise en pratique et Certificats

## 1. Échange de clés symétriques
* **Diffie-Hellman (DH) :** Comprendre la mathématique de l'échange sans transfert de secret.
* Utilisation du chiffrement asymétrique pour échanger une clé symétrique (Enveloppe numérique).

## 2. Accès distant sécurisé
* **Telnet** (non sécurisé) vs **SSH** (sécurisé).
* **Exercice :** Capture de trafic Telnet vs SSH avec **Wireshark**.

## 3. Infrastructure à Clés Publiques (PKI)
* **TLS 1.2 / 1.3 :** Analyse du Handshake.
* **Wireshark :** Décorticage d'une connexion HTTPS.
* **Chain of Trust :** Autorités de Certification (CA), Root, Intermédiaire.
* **CSR :** Certificate Signing Request.
# Séance 5 — Mise en pratique et Certificats

## 1. Objectifs pédagogiques

À la fin de la séance, l’étudiant sera capable de :

- Comprendre le principe de l’échange de clés Diffie-Hellman.
- Expliquer comment le chiffrement asymétrique permet d’échanger une clé symétrique.
- Comprendre la différence entre Telnet et SSH.
- Observer dans Wireshark la différence entre trafic chiffré et non chiffré.
- Comprendre le rôle d’une PKI et des certificats TLS.
- Identifier les étapes principales du TLS Handshake.
- Comprendre la chaîne de confiance (Chain of Trust).

---

## 2. Échange de clés symétriques

### Clé symétrique
- Une seule clé pour chiffrer/déchiffrer.
- Exemples : AES, DES, ChaCha20.
- Avantages : rapide, efficace.
- Inconvénients : la clé doit être partagée en sécurité.

### Clé asymétrique
- Une paire : clé publique + clé privée.
- Exemples : RSA, ECC, Diffie-Hellman.
- Avantages : pas besoin d’échanger un secret au départ.
- Inconvénients : plus lent.

### Combinaison des deux
Utilisé dans HTTPS, VPN, SSH :
- Asymétrique pour échanger une clé symétrique.
- Symétrique pour chiffrer les données.

---

## 3. Diffie–Hellman (DH)

Objectif : créer une clé secrète commune **sans jamais l’envoyer** sur le réseau.

### Paramètres publics
- Un nombre premier `p`
- Un générateur `g`

### Étapes
1. Alice choisit un secret `a` et envoie `A = g^a mod p`.
2. Bob choisit un secret `b` et envoie `B = g^b mod p`.
3. Les deux calculent la même clé :
   - Alice : `K = B^a mod p`
   - Bob : `K = A^b mod p`

### Pourquoi c’est sécurisé ?
Eve voit `p`, `g`, `A`, `B` mais ne peut pas retrouver `a` ou `b` (logarithme discret).

---

## 4. Exercice Diffie–Hellman (OpenSSL)

### Étape 1 — Paramètres DH
Créer `dhparams.pem` et coller les paramètres fournis.

### Étape 2 — Génération des clés privées
```bash
openssl genpkey -paramfile dhparams.pem -out alice_private.pem
openssl genpkey -paramfile dhparams.pem -out bob_private.pem
### Étape 3 — Génération des clés publiques
openssl pkey -in alice_private.pem -pubout -out alice_public.pem
openssl pkey -in bob_private.pem -pubout -out bob_public.pem



