# Cas d'usage

[English](../en/use-cases.md) | Français

| Cas | Statut V1 | Capacité réelle |
| --- | --- | --- |
| Déléguer un long contexte | Disponible | Texte borné, sans gain revendiqué. |
| Obtenir un second avis indépendant | Disponible | Appel manuel à un autre fournisseur ; vérification par l'appelant. |
| Extraction avec preuves | Disponible | Résultats structurés, offsets locaux et hash. |
| Comparaison entre fournisseurs | Disponible | Mêmes primitives pour Gemini, Anthropic et Fake. |
| Recherche sur l'injection de prompt | Disponible | Jeu synthétique et évaluateur déterministe limité. |
| Détection des erreurs du modèle secondaire | Extension possible | Fixture d'erreur ; étude de correction non incluse. |
| Routage contraint par coût | Disponible | Plafond strict rejetant les coûts inconnus sauf autorisation explicite. |
| Routage contraint par latence | Disponible | Filtre historique sans garantie future. |
| Routage contraint par confidentialité | Disponible | Modes déclarés par l'appelant et listes de fournisseurs. |
| Planification future des modèles | Recherche future | Aucun ordonnanceur ni apprentissage adaptatif en V1. |

Ces contraintes peuvent servir à examiner coût, latence, capacités, fournisseurs approuvés et confidentialité en entreprise. V1 n'est pas une plateforme IAM complète. Un adaptateur local compatible OpenAI pour Ollama, vLLM ou LM Studio serait une extension naturelle ; il n'est pas inclus.
