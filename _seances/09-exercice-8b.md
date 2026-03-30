---
layout: default
title: Exercice 8B
order: 9
description: TP DHCP Rogue
nav_order: 9
published: true
---

# TP : Comprendre et Détecter un Rogue DHCP

Le protocole DHCP repose sur un processus en quatre étapes appelé DORA (Discover, Offer, Request, Acknowledgement).

*   **Vulnérabilité :** Lorsqu'un client envoie un message Discover en broadcast pour obtenir une IP, n'importe quel équipement sur le réseau peut répondre.
*   **L'attaque :** Un attaquant déploie un faux serveur DHCP sur le réseau. Si ce faux serveur répond plus vite que le serveur légitime, l'ordinateur de la victime acceptera la première offre reçue et ignorera les suivantes.

**Comment l'attaquant détourne le trafic (Man-in-the-Middle) ?**

Une fois que le client accepte l'offre du pirate, celui-ci lui transmet de fausses informations de configuration :

*   **Fausse Passerelle (Default Gateway) :** L'attaquant donne sa propre adresse IP comme passerelle par défaut. Tout le trafic de la victime destiné à Internet est alors envoyé à l'attaquant au lieu du vrai routeur.
*   **Faux DNS :** L'attaquant peut aussi se désigner comme serveur DNS. S'il veut voler des identifiants, il peut rediriger une requête vers un site légitime (ex: Google) vers sa propre page web frauduleuse.
*   **Interception :** L'attaquant lit les données (mots de passe, messages), puis les renvoie au véritable routeur pour que la victime ne remarque rien. C'est le concept de Man-in-the-Middle (MITM).

**1. Qu'est-ce qu'un Rogue DHCP ?**

Un attaquant lance un faux serveur DHCP sur le réseau.
S'il répond plus vite que le vrai, le client reçoit :

*   une fausse passerelle
*   un faux DNS
*   parfois un faux site Web (phishing)
*   et l'attaquant devient l'intermédiaire (MITM)

Dans ce TP, le pirate redirige la victime vers un faux site lotto.

**2. Analyse du réseau**

| Équipement | Adresse IP | Rôle |
| :--- | :--- | :--- |
| Serveur DHCP légitime | 172.16.1.10 | DHCP + DNS |
| Serveur Web légitime | 172.16.1.100 | www.lotto.com |
| Serveur DHCP Rogue | 172.16.1.20 | Pirate DHCP |
| Faux serveur Web | 172.16.1.200 | Faux www.lotto.com |
| PC Étudiant | DHCP | Victime |
| Sniffer | - | Capture DHCP |

**3. Étape 1 - Fonctionnement normal du réseau**

**Consigne A - Activer le vrai serveur DHCP**

Activez le serveur DHCP **172.16.1.10**. (connectez le via le câble de PT et supprimer le câble du rogue DHCP pour le bon fonctionnement du TP)

**Consigne B - Réinitialiser le PC étudiant**

Sur le PC > Desktop > IP Configuration

*   cliquez sur **DHCP**
*   puis bouton **Renew** (ou éteindre / rallumer le PC)

**Vérifications demandées :**

1.  Ouvrir **Command Prompt** ipconfig /all Noter :
    *   l'adresse IP reçue
    *   l'adresse du serveur DHCP
    *   l'adresse du DNS
    *   la passerelle
2.  Tester le vrai site :
    Dans un navigateur : http://www.lotto.com Le site devrait renvoyer 172.16.1.100.
3.  Dans le Simulation Mode, observer les trames DHCP Discover / Offer / Request / Ack , vérifie aussi sur le Sniffer dans l'onglet GUI.

**5. Étape 2 - Introduction du Rogue DHCP**

Activez le serveur DHCP pirate : 172.16.1.20.

*   Réinitialiser le PC :
    Retapez DHCP / Renew sur le PC.

*   Ce que vous observez :
    *   Le PC reçoit souvent une IP du faux serveur
    *   Le DNS devient celui du pirate

Dans le sniffer > vous verrez deux DHCP Offer.
Le premier arrivé gagne > souvent le Rogue DHCP.

**6. Étape 3 - Redirection vers un faux site Web**

Lorsque le client tape dans le navigateur :
http://www.lotto.com

> Le faux DNS renvoie 172.16.1.200
> Le PC visite le faux site lotto (phishing)

**Questions :**

1.  Quelle IP correspond maintenant à www.lotto.com ?
2.  Comment distinguer un vrai site d'un faux ?
3.  Pourquoi HTTPS limiterait fortement ce type d'attaque ?

**7. Étape 4 - Analyse réseau et détection**

*   comparer les trames DHCP du vrai et du faux serveur
*   identifier l'adresse MAC du Rogue DHCP
*   vérifier les différences dans la configuration IP
*   analyser le trafic HTTP vers le faux site

**Questions :**

1.  À quel moment l'attaque devient possible ?
2.  Quels paramètres DHCP sont modifiés ?
3.  Qu'est-ce qui aurait pu empêcher l'attaque ?

**8. Comment se protéger d'un DHCP Rogue ?**

**1. DHCP Snooping sur les switches**
Les switches professionnels peuvent :
*   définir les ports de confiance (où se trouve le vrai DHCP)
*   bloquer tout serveur DHCP illégitime

**2. Filtrage des DNS**
*   DNS sécurisé
*   DNSSEC
*   Vérifier les adresses IP résolues

**3. Utiliser HTTPS**
HTTPS empêche l'utilisateur d'être dupé par un faux site (il verra un cadenas rouge).

**4. Segmentation du réseau**
*   Mettre les serveurs dans un VLAN isolé
*   Éviter que n'importe quelle machine puisse agir comme serveur DHCP

**5. Surveillance réseau**
*   détecter des réponses DHCP qui ne viennent pas du serveur légitime
*   IDS / IPS (Snort, Suricata)