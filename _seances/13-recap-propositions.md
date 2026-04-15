---
layout: default
title: "TP Récapitulatif : Préparation Examen"
order: 13
description: "Propositions de scénarios pour le TP récapitulatif final (Crypto, Réseau, Exploitation)"
nav_order: 13
published: false
---

# Analyse et Propositions pour le TP Récapitulatif (Préparation à l'Examen)

## 1. Résumé des Acquis (Séances 1 à 10)

L'analyse de l'ensemble de vos séances montre une progression pédagogique très claire, divisée en trois grands blocs de compétences que les étudiants doivent désormais maîtriser :

### Bloc A : Cryptographie Appliquée (Séances 1 à 6)
*   **Chiffrement Symétrique & Asymétrique :** AES, RSA, compréhension des clés publiques/privées.
*   **Hachage et Intégrité :** Différence entre chiffrer et hacher, MD5, SHA-256.
*   **Attaques :** Compréhension et exécution d'attaques par dictionnaire (Bruteforce).
*   **Infrastructures de Confiance :** Certificats, signatures numériques, sécurité des emails (GPG/PGP).

### Bloc B : Réseau et Sécurité Locale (Séances 7 à 9)
*   **Reconnaissance :** Utilisation de `nmap` pour scanner des ports, identifier des services et leurs versions.
*   **Attaques Locales (MITM) :** Compréhension théorique et/ou pratique de l'ARP Spoofing et de la détection de Rogue DHCP.

### Bloc C : Exploitation (Séance 10)
*   **Framework Metasploit :** `msfconsole`, recherche de vulnérabilités (`search`), configuration de modules (`show options`, `set`).
*   **Concepts de Shells :** Obtention d'un accès distant, distinction fondamentale entre Bind Shell et Reverse Shell.

---

## 2. Pistes de Réflexion & Questions Pédagogiques

Avant de choisir le scénario, voici quelques questions cruciales pour calibrer la difficulté sans introduire de nouveaux concepts :

*   **Le temps vs la difficulté :** En 1h30/2h, une attaque par dictionnaire avec `rockyou.txt` sur une machine peu performante peut prendre tout le temps du TP. *Devons-nous leur fournir un mini-dictionnaire ciblé pour accélérer cette étape ?*
*   **L'autonomie :** Devons-nous leur donner le point de départ exact (ex: "Scannez cette IP"), ou les laisser découvrir l'IP de la cible sur leur réseau Docker local par eux-mêmes ?
*   **Identification des formats :** S'ils trouvent un hash, doivent-ils deviner l'algorithme (ex: compter le nombre de caractères pour déduire du MD5) ou le leur donnons-nous ?

---

## 3. Suggestions de Scénarios pour le TP Récapitulatif

Voici trois propositions de "TP Synthèse", conçues comme un Escape Game ou un CTF (Capture The Flag). Ces scénarios lient toutes les notions vues depuis le début de l'année.

### Proposition 1 : "La Kill-Chain Complète" (Mon favori)
*L'objectif est d'enchaîner chronologiquement les trois blocs de l'année.*

1.  **Reconnaissance (Bloc B) :** L'étudiant démarre une cible Docker "boîte noire". Il doit d'abord utiliser `nmap` pour trouver les services ouverts.
2.  **Exploitation (Bloc C) :** Il identifie un FTP vulnérable ou un Samba mal configuré et utilise `msfconsole` pour obtenir un **Reverse Shell**.
3.  **Fouille (Post-Exploitation) :** Dans les fichiers de la cible (via le shell), il trouve une archive chiffrée (`secret.zip` ou `.aes`) et un fichier `hash_du_mot_de_passe.txt`.
4.  **Cassage (Bloc A) :** Il rapatrie le hash, utilise l'attaque par dictionnaire pour retrouver le mot de passe en clair.
5.  **Déchiffrement (Bloc A) :** Avec le mot de passe, il déchiffre l'archive. À l'intérieur, il trouve un message chiffré avec sa propre clé publique GPG/RSA. Il doit le déchiffrer avec sa clé privée pour valider le TP (obtenir la note finale ou le "Flag").
*   **Avantages :** Extrêmement complet, teste exactement ce qui a été vu. Rythme très satisfaisant (chaque étape débloque la suivante).
*   **Niveau :** Difficile car l'erreur à une étape bloque le reste, mais 100% faisable avec les notes de cours.

### Proposition 2 : "L'Enquête Interne" (Focus Réseau/MITM et Crypto)
*Ce scénario met plus l'accent sur les attaques réseau locales et l'analyse.*

1.  **Analyse MITM (Bloc B) :** On leur fournit un fichier `.pcap` (capture réseau). Ils l'ouvrent avec Wireshark et doivent diagnostiquer une attaque de type ARP Spoofing ou Rogue DHCP.
2.  **Extraction (Bloc B/A) :** Dans cette capture, ils isolent un échange non chiffré contenant un certificat suspect et un fichier de signature.
3.  **Vérification de Certificat (Bloc A) :** Ils doivent utiliser `openssl` pour vérifier si le certificat est valide (il ne l'est pas).
4.  **Extraction de Hash (Bloc A) :** Le trafic contenait aussi un mot de passe haché (authentification interceptée). Ils le cassent via dictionnaire.
5.  **Intrusion Finale (Bloc C) :** Ils utilisent ce mot de passe pour se connecter en SSH (pas de Metasploit ici) à une machine cible et récupérer le document final.
*   **Avantages :** Met en valeur la partie réseau souvent difficile à tester autrement.
*   **Inconvénients :** Fait l'impasse sur Metasploit, ce qui serait dommage vu l'énergie mise au TP 9.

### Proposition 3 : "La Poupée Russe" (Focus Exploitation & Asymétrique)
*Scénario plus technique, axé sur l'élévation de privilèges logicielle et la crypto asymétrique.*

1.  **Entrée (Bloc C) :** Exploitation classique via Metasploit (vsFTPd) pour obtenir un shell avec un utilisateur à droits limités.
2.  **Le Coffre-Fort (Bloc A) :** Dans son répertoire, l'utilisateur trouve un texte chiffré par RSA. L'étudiant doit générer une paire de clés, configurer une attaque d'ingénierie sociale basique (mettre sa clé publique dans le bon dossier pour que l'admin chiffre un message pour lui).
3.  **Le Graal (Bloc A) :** Une fois le message déchiffré, il obtient un hash MD5.
4.  **Cassage final (Bloc A) :** Il casse le hash pour obtenir le mot de passe `root` de la machine cible.
*   **Avantages :** Demande de l'imagination pour la crypto asymétrique.
*   **Inconvénients :** Peut-être trop abstrait pour une préparation d'examen.

---

**Recommandation de Basile :** La **Proposition 1** est la plus "carrée" pour préparer un examen pratique. Elle teste rigoureusement le flux de travail d'un pentester tel que vous l'avez enseigné : *Scanner -> Exploiter -> Voler des données -> Casser la crypto locale -> Déchiffrer les communications asymétriques.* 

Dites-moi laquelle vous préférez, et j'enverrai un de mes clones souffrir... heu, travailler, pour générer la structure complète du TP avec les fichiers associés !