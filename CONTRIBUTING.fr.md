# Contribuer

[English](CONTRIBUTING.md) | Français

Ce projet est un aperçu de recherche expérimental. Préférez les modifications petites, testables et accompagnées d'hypothèses explicites.

1. Installez Python 3.12+ et `uv`, puis lancez `uv sync --extra test`.
2. Lancez `uv run pytest -q` et `uv run ruff check gateway.py server.py providers tests` avant de proposer une modification. Les tests unitaires ne doivent jamais exiger une vraie clé API ni un appel réseau.
3. Ouvrez une issue décrivant le problème, le comportement attendu, l'incidence sur la sécurité ou la recherche et un exemple minimal **synthétique**. Proposez une modification par pull request ciblée.
4. Pour ajouter un fournisseur, implémentez `DelegationProvider` dans un nouveau module de `providers/`, isolez les appels SDK, validez la configuration, évitez de journaliser les données et ajoutez des tests avec un faux client. N'ajoutez pas d'autres fournisseurs à cet aperçu uniquement pour compléter une liste.
5. Pour ajouter un benchmark, précisez la source de la tâche et ses droits de redistribution, la stratégie, la réponse de référence, l'évaluateur, les champs mesurés ou estimés et la méthode de reproduction. Utilisez seulement des données synthétiques ou redistribuables. Ne revendiquez pas de résultats non mesurés.
6. Ne commitez jamais `.env`, clés, tokens, journaux, données personnelles ou identifiants d'infrastructure privée. Effectuez un scan de secrets avant une pull request. Pour les vulnérabilités, suivez [SECURITY.fr.md](SECURITY.fr.md) plutôt que d'ouvrir une issue publique.

Les modifications substantielles de documentation doivent finir par être répercutées **en anglais et en français**. Une contribution peut commencer dans une seule langue, mais les releases officielles doivent préserver la parité, surtout pour la sécurité et le partage de données.
