# Travaux liés

[English](../en/related-work.md) | Français

La délégation générique entre modèles est antérieure à ce projet. Les descriptions amont ci-dessous ont été vérifiées le 25 septembre 2026 ; leurs capacités peuvent évoluer. Ces liens servent de points de comparaison, sans approbation ni revendication de priorité.

| Projet | Périmètre vérifié | Rapport avec ce dépôt |
| --- | --- | --- |
| [Gemini MCP Tool](https://github.com/jamubc/gemini-mcp-tool) | Outil MCP reliant un assistant à Gemini CLI ou à son successeur pour l'analyse. | Un pont Gemini concret. Ce dépôt utilise des API de fournisseurs configurés via un contrat Python borné et enregistre les décisions de routage et d'évaluation. |
| [PAL MCP Server](https://github.com/BeehiveInnovations/pal-mcp-server) | Outils MCP pour plusieurs fournisseurs de modèles et points d'accès personnalisés. | La collaboration entre modèles existe déjà. Ce dépôt se concentre sur le filtrage explicite, la vérification locale des citations et les artefacts de benchmark reproductibles. |
| [LiteLLM Router](https://github.com/BerriAI/litellm-docs/blob/main/docs/routing.md) | Routage et répartition de charge entre déploiements, avec stratégies configurables. | Ce dépôt propose un routeur plus restreint et orienté recherche, filtrant les contraintes déclarées de confidentialité et capacité et pouvant utiliser un historique de benchmark. |
| [promptfoo](https://github.com/promptfoo/promptfoo/blob/main/site/docs/configuration/guide.md) | Prompts, fournisseurs, cas de test et assertions configurables pour évaluer des LLM. | C'est un système d'évaluation plus large. Ce dépôt relie ses évaluations limitées à sa délégation, sa trace de routage et son contrôle local des citations. |

L'objectif est une **boucle reproductible** reliant délégation bornée, mesure, filtrage des contraintes, exécution, vérification des preuves et évaluation. La V1 ne démontre aucune supériorité de qualité, coût, latence ou sécurité sur ces projets. Voir la [méthodologie](methodology.md) pour les expériences nécessaires.
