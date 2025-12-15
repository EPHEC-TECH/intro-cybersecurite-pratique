---
layout: default
title: Accueil
---

# 🛡️ Sécurité des Systèmes et Réseaux

Bienvenue sur le site du cours. Ce dépôt contient les supports de cours, les exercices pratiques et les ressources pour le module de sécurité.

## 📋 Informations Administratives
* **ECTS :** 4
* **Volume horaire :** 45h
* **Lien officiel :** [Fiche EPHEC](https://eperso.ephec.be/ProfFicheCoursHe/Visualiser/14794)

## 📚 Programme des Séances

Voici le déroulé du quadrimestre. Cliquez sur une séance pour accéder au contenu.

| # | Sujet | Thèmes clés |
|:--|:------|:------------|
{% assign sorted_seances = site.seances | sort: 'order' %}
{% for seance in sorted_seances %}
| {{ seance.order }} | [**{{ seance.title }}**]({{ seance.url | relative_url }}) | {{ seance.description }} |
{% endfor %}
