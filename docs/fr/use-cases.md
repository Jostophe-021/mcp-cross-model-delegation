# Cas d'usage

[English](../en/use-cases.md) | Français

## Disponibles en V1

- **Délégation délimitée et second avis :** transmettre TASK et CONTEXT fournis par l'appelant à Gemini ou Anthropic et examiner la réponse. L'appelant décide de son emploi.
- **Extraction avec preuves :** demander des résultats structurés et vérifier localement les citations dans le contexte fourni. Cela vérifie leur emplacement, pas leur vérité.
- **Délégation de longs contextes :** transmettre un texte long et borné à un fournisseur configuré ; aucun gain de tokens ou de coût n'est mesuré.
- **Comparaison Gemini/Anthropic :** exécuter le même jeu redistribuable sous des conditions explicites, avec manifeste et résultats.
- **Contraintes de routage :** filtrer confidentialité déclarée, fournisseurs autorisés, capacités et historiques connus de coût et de latence avant sélection.
- **Recherche sur l'injection de prompt :** utiliser la petite fixture synthétique et son évaluateur déterministe pour de futures études, sans preuve de résistance.
- **Infrastructure de benchmark et outils MCP :** fonctionner hors ligne avec FakeProvider ou activer des appels réels ; exposer la délégation bornée aux clients MCP compatibles sur loopback.

## Extensions possibles

- Fournisseurs secondaires OpenAI et locaux ou compatibles OpenAI.
- Jeux de données plus larges et indépendants, autres méthodes d'évaluation.
- Planification avancée et expériences adaptatives.

La V1 n'est ni un système IAM d'entreprise complet, ni un agent autonome, ni une frontière de sécurité. Voir la [méthodologie](methodology.md) et le [guide d'extension](extending.md).
