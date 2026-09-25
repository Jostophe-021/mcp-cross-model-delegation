# v1.0.0 — Stable Cross-Model Routing & Evaluation Framework

MCP Cross-Model Delegation est un petit cadre de recherche privilégiant l'exécution locale pour mesurer, comparer, router et vérifier des tâches délimitées entre modèles de langage.

## Contenu de cette version

- Adaptateurs Gemini et Anthropic facultatifs, et `FakeProvider` déterministe pour la validation hors ligne.
- Routage filtrant d'abord les contraintes, avec politiques `manual`, `rules` et `benchmark_weighted`, décisions `RoutingDecision` explicables, contraintes de confidentialité et traces de repli explicites.
- Vérification locale des citations dans le contexte fourni.
- Runner de benchmark reproductible avec évaluateurs déterministes, commandes CLI et outils MCP génériques. Les noms des outils Gemini V0.1 restent disponibles comme alias de compatibilité.
- Documentation anglaise et française, paramètres de sécurité favorisant l'exécution locale, workflow de publication OCI avec métadonnées et SBOM SPDX, et métadonnées prêtes pour le MCP Registry.

La démonstration hors ligne est `uv run crossmodel bench run benchmarks/datasets/basic.jsonl` après `uv sync --locked --extra all --extra test`. Elle ne demande aucune clé API. Les appels à de vrais fournisseurs exigent des identifiants séparés et une activation explicite.

**Cette version fournit le cadre et une validation synthétique reproductible. Elle ne prétend pas que la délégation entre modèles améliore la qualité, le coût, la latence ou l'utilisation de tokens sans expériences mesurées.**
