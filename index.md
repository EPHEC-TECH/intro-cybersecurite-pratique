---
layout: default
title: Accueil
---

# 🛡️ Introduction à la CyberSecurité
Bienvenue sur le site du cours, vous y trouverez les énoncés des séances pratiques.

* **Lien officiel :** [Fiche EPHEC](https://eperso.ephec.be/ProfFicheCoursHe/Visualiser/14794)

## 📚 Programme des Séances
Voici le déroulé du quadrimestre. Cliquez sur une séance pour accéder au contenu.

{% assign sorted_seances = site.seances | sort: 'order' %}
{% for seance in sorted_seances %}
  * **Séance {{ seance.order }} :** [{{ seance.title }}]({{ seance.url | relative_url }}) (Thèmes : {{ seance.description }})
{% endfor %}
