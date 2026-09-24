# Méthodologie de recherche

[English](../en/methodology.md) | Français

## Questions et hypothèses

V1 fournit des instruments de mesure, pas des conclusions. Toute question exige un jeu de données, une baseline et une analyse indépendante :

1. Quand la délégation améliore-t-elle la qualité ?
2. Quand réduit-elle le contexte de l'orchestrateur ?
3. Quelle latence ajoute-t-elle ?
4. Quel coût ajoute-t-elle ?
5. Les preuves structurées améliorent-elles la vérification ?
6. Un orchestrateur peut-il détecter les erreurs du modèle secondaire ?
7. Quelle est la résistance de la séparation TASK/CONTEXT aux injections ?
8. Quel fournisseur réussit selon la catégorie de tâche ?
9. Le routage fondé sur des benchmarks dépasse-t-il une politique fixe ?
10. Comment confidentialité, coût et latence changent-ils la route retenue ?

Énoncez les hypothèses avant les expériences. Le dépôt ne répond encore à aucune de ces questions.

## Conditions et données

La CLI applique `orchestrator_only`, `fixed_delegation`, `structured_delegation` et `routed_delegation` au même JSONL. V1 exécute un seul appel par condition, sans seconde synthèse par l'orchestrateur. Les essais FakeProvider valident le logiciel, pas les modèles. Les appels réels exigent `--live` et des clés configurées. Les petites données versionnées sont synthétiques et redistribuables. Le générateur de long contexte enregistre seed, version, nombre de caractères et tokens inconnus.

Séparez catégories, répétitions, identifiants exacts des modèles et jeu de validation tenu à l'écart. Un routeur réglé sur le benchmark qui sert à l'évaluer risque d'apprendre ses particularités. Une étude future doit séparer l'historique d'entraînement et le holdout.

## Métriques, politiques et évaluation

Les résultats notent modèle, fournisseur, raisons de routage, latence, succès/erreur, hash de source, repli et évaluations. Tokens et coût restent `null` tant qu'ils ne sont pas mesurés ou estimés avec une source tarifaire datée. Une latence historique n'est pas garantie. `manual` sert de baseline, `rules` est déterministe, `benchmark_weighted` ne compare que les métriques connues de tous les candidats. Confidentialité et plafonds stricts filtrent avant le score.

Les évaluateurs déterministes traitent l'égalité textuelle, numérique, la présence locale de citations, la forme structurée et la préservation d'une tâche synthétique face à une injection. Une égalité exacte ne prouve pas une exactitude sémantique ; une citation présente ne prouve pas la vérité de l'affirmation. Le modèle testé n'est jamais son seul juge. Un juge LLM reste une piste future, distincte et optionnelle, avec identité et grille documentées.

## Reproductibilité et confidentialité

Chaque run enregistre version du projet, SHA Git si disponible, version du dataset, date, modèles, fournisseurs, conditions, seed, répétitions, politique et poids. Une étude publiable conserve résultats bruts **non sensibles**, résumé et limites connues. V1 omet prompts et réponses par défaut et conserve le SHA-256 du contexte exact. `--save-responses` convient uniquement aux données redistribuables. Aucune télémétrie personnalisée n'est activée.

## Menaces pour la validité

Alias de modèle mouvants, mises à jour fournisseur, sorties stochastiques, tokenizers différents, régions et APIs différentes, quotas, politiques de sûreté, biais d'évaluation, contamination des données, petits échantillons, effets temporels et surajustement du routeur limitent toute conclusion. Le jeu fourni est trop petit pour une comparaison de modèles. Les temps du fournisseur factice ne prouvent aucune économie.
