---
layout: default
title: Accueil
---

# 🛡️ Introduction à la CyberSecurité
Bienvenue sur le site du cours, vous y trouverez les énoncés des séances pratiques.

* **Lien officiel :** [Fiche EPHEC](https://eperso.ephec.be/ProfFicheCoursHe/Visualiser/14794)

## 📚 Programme des Séances
Voici le déroulé du quadrimestre. Cliquez sur une séance pour accéder au contenu.

| # | Sujet | Thèmes clés |
|:--|:------|:------------|
{% comment %}
    Utilisation de 'capture' pour générer toutes les lignes d'un coup.
    Ceci permet de présenter un seul bloc de texte au moteur Markdown.
{% endcomment %}
{% capture table_rows %}
{% assign sorted_seances = site.seances | sort: 'order' %}
{% for seance in sorted_seances %}
| {{ seance.order }} | [**{{ seance.title }}**]({{ seance.url | relative_url }}) | {{ seance.description }} |
{% endfor %}
{% endcapture %}
{{ table_rows }}


