# Première expérience réelle

[English](../en/first-experiment.md) | Français

Cette expérience est **manuelle et facultative**. Les appels API Gemini et Anthropic peuvent être facturés. Le démarrage hors ligne ne les lance pas. Utilisez seulement des tâches synthétiques ou redistribuables et vérifiez les politiques des fournisseurs.

1. Lisez la [méthodologie](methodology.md) et inspectez [`basic.jsonl`](../../benchmarks/datasets/basic.jsonl). Définissez une question étroite et les métriques de qualité, preuves, latence et échec avant l'essai. Six tâches synthétiques contrôlent le logiciel ; elles ne sont pas représentatives.
2. Notez `v1.0.0` et `git rev-parse HEAD`. Conservez le jeu et sa version. Choisissez les identifiants exacts de fournisseur/modèle, réglages API, politique, évaluateur, seed, répétitions et budget. Configurez les clés uniquement dans votre environnement.
3. Lancez `uv run crossmodel bench run benchmarks/datasets/basic.jsonl` pour contrôler le parcours sans appel API. Inspectez `manifest.json`, `results.jsonl` et `summary.json` dans le dossier affiché.
4. Après avoir accepté le nombre d'appels annoncé et les frais possibles, lancez par exemple `uv run crossmodel bench run benchmarks/datasets/basic.jsonl --live --provider gemini --orchestrator anthropic --repetitions 3 --shuffle --seed 42`. La V1 fait un appel par condition, sans seconde synthèse de l'orchestrateur.
5. Conservez le manifeste complet, les résultats bruts **non sensibles**, la synthèse et les limites. Les résultats omettent tâche/contexte/réponse par défaut ; `--save-responses` est facultatif et peut exposer des données. Les tokens ou coûts inconnus sont indisponibles, pas nuls. Signalez provenance, taille, faiblesses de l'évaluateur, évolution des modèles et appels échoués.

Le manifeste contient version du projet, SHA Git, hash/version du jeu, fournisseurs et modèles, politique, seed et répétitions. Notez séparément avec la date les réglages ou changements côté fournisseur. La seed contrôle l'ordre local des conditions, pas le déterminisme des modèles. Utilisez des tâches non vues et une revue indépendante avant toute revendication de performance. Partagez une configuration sûre dans les [Discussions](../../SUPPORT.md) pour inviter une reproduction.
