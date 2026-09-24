# Benchmarks

[English](README.md) | Français

Ce dossier définit un format de mesure **prévu** ; il ne contient aucun résultat expérimental. Le [schéma JSON](benchmark_schema.json) enregistre l'identifiant du benchmark, la tâche, la taille du contexte, la version du projet, les modèles, le fournisseur, la stratégie, la configuration publique, la latence, les tokens, le coût estimé, le résultat, la réponse de référence, l'évaluation, les erreurs et l'horodatage. Utilisez `null` et `unavailable` si une valeur n'est pas fournie ; ne remplacez jamais une consommation manquante par un zéro inventé.

Seules les tâches synthétiques, publiques ou explicitement redistribuables peuvent être commitées. Ne stockez ni vrais prompts utilisateur, ni identifiants, ni infrastructure privée, ni données client. Si un futur exécuteur traite des données sensibles dans une gouvernance distincte, il devra conserver par défaut seulement des métriques agrégées non sensibles.

Les comparaisons prévues couvrent l'orchestrateur seul, la délégation libre, la délégation structurée, les groupes de taille de contexte, les mauvaises réponses secondaires introduites volontairement dans des tests **synthétiques**, l'injection dans le prompt, la fidélité des preuves et, plus tard, plusieurs fournisseurs. Consignez les évaluateurs et leurs grilles. Le modèle testé ne doit pas être son seul juge. Voir la [feuille de route de recherche](../docs/fr/research-roadmap.md).
