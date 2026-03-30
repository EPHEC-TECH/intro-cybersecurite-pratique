---
layout: default
title: Attaque Réseau Local
order: 8
description: ARP, Man-in-the-Middle
nav_order: 8
published: true
---

# Séance 8a : ARP spoofing

# TP : Comprendre l'ARP Spoofing et l'attaque Man-in-the-Middle

**1. Théorie : Qu'est-ce que l'ARP Spoofing ?**

Le protocole ARP (Address Resolution Protocol) est essentiel pour la communication sur un réseau local. Il permet de faire correspondre une adresse IP (couche 3) à une adresse MAC physique (couche 2).

* **Fonctionnement normal :** Lorsqu'un PC veut communiquer avec sa passerelle par défaut (le routeur), il consulte son cache ARP. S'il ne connaît pas l'adresse MAC du routeur, il envoie une requête ARP. Une fois la réponse reçue, il enregistre le lien entre l'IP du routeur et son adresse MAC pour envoyer ses paquets.
* **Le concept de Spoofing :** L'attaque repose sur l'envoi de messages ARP falsifiés (souvent appelés "gratuitous ARP"). L'attaquant fait croire aux autres machines du réseau que son adresse MAC est celle de la passerelle par défaut.
* **Man-in-the-Middle (MITM) :** Une fois que le cache ARP de la victime est corrompu, tout le trafic destiné à Internet ou à un autre réseau est envoyé à l'attaquant au lieu du routeur. L'attaquant peut alors intercepter, lire ou modifier les données avant, idéalement, de les renvoyer au véritable routeur pour que la victime ne se doute de rien.

**2. Configuration du TP (Topologie)**

👉 [Télécharger le fichier Packet Tracer du TP (arp_spoofing.pkt)](../ressources/seance8/arp_spoofing.pkt)

Pour ce TP, utilisez un simulateur (Packet Tracer) avec la configuration suivante :

* **PC1 (Victime) :** IP 192.168.1.10, MAC : à trouver
* **Routeur R1 (Passerelle) :** IP 192.168.1.254, MAC : à trouver
* **Attaquant (Threat Actor) :** IP 192.168.1.20, MAC : à trouver
* **Serveur Web :** IP 192.168.2.100

**3. Étapes de réalisation**

**Étape 1 : Observation de l'état normal**

1. Depuis PC1, tentez de joindre le serveur web (ping ou navigateur sur le port 80).
2. Sur PC1, ouvrez l'invite de commande et tapez `arp -a`.
   * Observation : Vous devriez voir l'IP de la passerelle (1.254) associée à sa véritable adresse MAC .
3. Sur le Switch, vérifiez la table d'adresses MAC : `show mac address-table dynamic`. Notez sur quel port est apprise l'adresse MAC du routeur.

**Étape 2 : Lancement de l'attaque (Spoofing)**

1. L'attaquant change son adresse MAC pour usurper celle du routeur .
2. L'attaquant envoie des messages ARP de type "gratuitous" vers PC1 pour annoncer qu'il est la passerelle.
3. L'attaquant peut également envoyer un flux de pings continus vers PC1 pour maintenir la corruption du cache.

**Étape 3 : Vérification de la corruption**

1. Retournez sur PC1 et tapez à nouveau `arp -a`.
   * *Résultat attendu* : L'IP 192.168.1.254 est maintenant associée à l'adresse MAC de l'attaquant (ou le port du switch indique que cette MAC se trouve vers l'attaquant).
2. Sur le Switch, vérifiez à nouveau la table MAC. Vous constaterez que l'adresse MAC du routeur est maintenant apprise sur le port où est connecté l'attaquant .

**Étape 4 : Interception des données (MITM)**

1. Depuis PC1, essayez d'accéder au serveur web via le navigateur (192.168.2.100).
2. Sur la machine de l'attaquant, utilisez un analyseur de trafic (Sniffer).
   * Observation : Vous verrez passer les paquets HTTP (port 80) provenant de PC1.
   * Analyse : En examinant les en-têtes des paquets, vous pouvez lire les données transmises car le trafic n'est pas chiffré.

**4. Questions de réflexion :**

1. **Pourquoi le premier ping de PC1 échoue-t-il parfois ?**

2. **Quel est l'impact pour l'utilisateur (PC1) si l'attaquant ne renvoie pas les paquets au routeur ?**

3. **Comment un administrateur réseau peut-il détecter cette attaque sur un switch ?**

L'attaque réussit parce que le switch met à jour sa table d'adresses MAC dynamique de manière erronée lorsqu'il reçoit des trames de l'attaquant.

* En temps normal, le switch associe l'adresse MAC du routeur au port où il est réellement connecté (ex: G0/1).
* Lors de l'attaque, l'usurpateur (Threat Actor) envoie des messages qui forcent le switch à apprendre l'adresse MAC du routeur sur son propre port (ex: Fa0/2).
* On peut détecter cette anomalie sur le switch avec la commande `show mac address-table dynamic`, qui montrera que la MAC de la passerelle est désormais apprise sur le port de l'attaquant.

**Méthodes de protection :**

Pour empêcher ce détournement de trafic sur un switch Cisco, les administrateurs utilisent généralement les fonctionnalités suivantes :

1. **Dynamic ARP Inspection (DAI)** : C'est la protection la plus efficace. Le switch intercepte toutes les requêtes et réponses ARP sur les ports non approuvés. Il vérifie si la correspondance entre l'adresse IP et l'adresse MAC est valide avant de laisser passer le paquet.
2. **DHCP Snooping** : Pour fonctionner, DAI a besoin d'une base de données fiable. Le DHCP Snooping permet au switch de surveiller les attributions d'adresses IP par le serveur DHCP et de créer une table de correspondance (IP/MAC/Port) sécurisée.
3. **Port Security** : Cette fonction permet de limiter le nombre d'adresses MAC autorisées sur un port ou de bloquer l'accès si une adresse MAC inconnue (ou appartenant déjà à un autre port, comme celle du routeur) tente de se connecter sur un port utilisateur.
4. **ACLs ARP statiques** : Dans les réseaux où les adresses IP ne changent pas, on peut configurer manuellement des listes de contrôle d'accès pour forcer le switch à n'accepter que des couples IP/MAC spécifiques.

Souhaitez-vous que je recherche des sources supplémentaires pour obtenir les commandes de configuration spécifiques à ces protections (comme DAI ou DHCP Snooping) sur des équipements Cisco ?
