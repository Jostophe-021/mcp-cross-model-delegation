# Contribuer

[English](CONTRIBUTING.md) | Français

Ce projet est un petit cadre de recherche. Préférez les modifications petites, testables et accompagnées d'hypothèses explicites.

## Fork et dépôt amont

Si `origin` désigne votre fork GitHub, `upstream` désigne le dépôt d'origine. Depuis votre copie :

```bash
git remote add upstream https://github.com/Jostophe-021/mcp-cross-model-delegation.git
git fetch upstream
git rebase upstream/main
```

Ajoutez `upstream` une seule fois. Rebasez seulement votre propre branche non partagée ; résolvez les conflits avant de pousser. Forks indépendants et contributions amont sont tous deux bienvenus. Voir le [guide d'extension](docs/fr/extending.md) pour les contrats V1.

1. Installez Python 3.12 ou 3.13 et `uv`, puis lancez `uv sync --locked --extra all --extra test`.
2. Lancez `uv run pytest -q` et `uv run ruff check gateway.py server.py contracts.py routing.py execution.py evidence.py cli.py providers benchmarks tests` avant de proposer une modification. Les tests unitaires ne doivent jamais exiger une vraie clé API ni un appel réseau.
3. Ouvrez une issue décrivant le problème, le comportement attendu, l'incidence sur la sécurité ou la recherche et un exemple minimal **synthétique**. Proposez une modification par pull request ciblée.
4. Pour ajouter un fournisseur, implémentez `DelegationProvider` dans un nouveau module de `providers/`, isolez les appels SDK, validez la configuration, évitez de journaliser les données et ajoutez des tests avec un faux client. Discutez le périmètre dans une issue avant une grande PR.
5. Pour ajouter un benchmark, précisez la source de la tâche et ses droits de redistribution, la stratégie, la réponse de référence, l'évaluateur, les champs mesurés ou estimés et la méthode de reproduction. Utilisez seulement des données synthétiques ou redistribuables. Ne revendiquez pas de résultats non mesurés.
6. Ne commitez jamais `.env`, clés, tokens, journaux, données personnelles ou identifiants d'infrastructure privée. Effectuez un scan de secrets avant une pull request. Pour les vulnérabilités, suivez [SECURITY.fr.md](SECURITY.fr.md) plutôt que d'ouvrir une issue publique.

Les modifications substantielles de documentation doivent finir par être répercutées **en anglais et en français**. Une contribution peut commencer dans une seule langue, mais les releases officielles doivent préserver la parité, surtout pour la sécurité et le partage de données.

Utilisez les [Discussions](https://github.com/Jostophe-021/mcp-cross-model-delegation/discussions) pour les questions, idées et résultats de recherche reproductibles. Utilisez les [formulaires d'issue](https://github.com/Jostophe-021/mcp-cross-model-delegation/issues/new/choose) pour les bugs et propositions actionnables.
