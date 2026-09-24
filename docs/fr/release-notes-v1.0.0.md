# Notes proposées pour la version v1.0.0

**Tag :** `v1.0.0`
**Titre :** v1.0.0 — Stable Cross-Model Routing & Evaluation Framework

Cette version introduit des fournisseurs Gemini et Anthropic optionnels derrière un petit contrat commun. Elle ajoute un routage explicable qui filtre d'abord les contraintes, avec les politiques `manual`, `rules` et `benchmark_weighted` ; une vérification locale des citations ; un runner de benchmark reproductible ; une CLI ; et des outils MCP génériques. Les noms des outils Gemini V0.1 restent disponibles comme alias de compatibilité. Le serveur privilégie une exécution locale et refuse une écoute publique sans authentification.

Cette version fournit le cadre et une validation synthétique reproductible. Elle ne prétend pas que la délégation entre modèles améliore la qualité, le coût ou la latence sans expériences mesurées. Les expériences API réelles demandent une activation explicite et des accès API distincts.

Ne publier ces notes qu'après approbation de la PR, fusion, contrôles de release et création du tag et de l'image OCI. Les [notes anglaises](../en/release-notes-v1.0.0.md) font partie du même brouillon.
