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

<table class="table-seances">
  <thead>
    <tr>
      <th style="width: 5%">#</th>
      <th style="width: 35%">Sujet</th>
      <th style="width: 60%">Thèmes clés</th>
    </tr>
  </thead>
  <tbody>
    {% assign sorted_seances = site.seances | sort: 'order' %}
    {% for seance in sorted_seances %}
    <tr>
      <td style="text-align: center;">{{ seance.order }}</td>
      <td>
        <a href="{{ seance.url | relative_url }}">
          <strong>{{ seance.title }}</strong>
        </a>
      </td>
      <td>{{ seance.description }}</td>
    </tr>
    {% endfor %}
  </tbody>
</table>
