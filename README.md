# 🛡️ Sécurité des Systèmes et Réseaux - Support de Cours

[![GitHub Pages](https://img.shields.io/badge/Status-En%20Ligne-success?style=flat-square)](https://[NOM-ORGANISATION].github.io)
[![EPHEC](https://img.shields.io/badge/EPHEC-2ème%20Année-blue?style=flat-square)](https://www.ephec.be)

Ce dépôt contient le code source et le contenu du site de cours de **Sécurité des Systèmes et Réseaux**. Le site est généré statiquement via [Jekyll](https://jekyllrb.com/) et hébergé sur GitHub Pages.

🔗 **Accéder au site du cours :** [https://[NOM-ORGANISATION].github.io](https://[NOM-ORGANISATION].github.io)

## 📚 Contenu du Module

Ce cours couvre les fondamentaux de la sécurité informatique, incluant :
* **Cryptographie :** Symétrique (AES), Asymétrique (RSA), Hachage.
* **Infrastructure :** PKI, Certificats, SSL/TLS, SSH.
* **Menaces Réseau :** Sniffing, Spoofing (ARP/DHCP), MiM.
* **Sécurité Web :** OWASP Top 10 (SQLi, XSS).
* **Outils pratiques :** Wireshark, Nmap, Metasploit, CyberChef.

Fiche officielle du cours : [EPHEC - Sécurité](https://eperso.ephec.be/ProfFicheCoursHe/Visualiser/14794)

---

## 🛠️ Guide pour les Enseignants (Maintenance)

Cette section explique comment modifier le cours ou travailler en local.

### 1. Prérequis
* Ruby & Bundler
* Git

### 2. Installation Locale
Pour visualiser le site sur votre machine avant de pousser les modifications :

```bash
# 1. Cloner le dépôt
git clone [https://github.com/](https://github.com/)[NOM-ORGANISATION]/[NOM-ORGANISATION].github.io.git
cd [NOM-ORGANISATION].github.io

# 2. Installer les dépendances
bundle install

# 3. Lancer le serveur local
bundle exec jekyll serve
