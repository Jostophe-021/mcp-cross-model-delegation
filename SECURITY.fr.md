# Politique de sécurité

[English](SECURITY.md) | Français

## Signalement

Utilisez le **signalement privé de vulnérabilité** de GitHub pour ce dépôt s'il est activé. Si aucun canal privé n'est disponible, ouvrez une issue publique contenant uniquement une demande minimale et non sensible de mise en place d'un canal privé. Ne publiez pas les détails d'exploitation, les clés API, les vrais prompts, les données utilisateur ou les informations d'infrastructure privée dans une issue ou pull request publique. Aucune adresse e-mail de sécurité n'est prétendue ici.

## Périmètre et risques actuels

Il s'agit d'un aperçu expérimental, pas d'un service durci. Les principaux risques sont l'injection indirecte dans CONTEXT, le partage accidentel de texte sensible avec un fournisseur tiers, l'hallucination ou la manipulation des réponses, un résultat structuré invalide, une dépendance compromise, une écoute publique mal configurée et la journalisation accidentelle de secrets ou de données. L'écoute locale par défaut, les limites de taille, l'absence de télémétrie personnalisée, `store=False`, les réponses d'erreur fixes et les tests avec faux clients réduisent certains risques sans les éliminer. Une frontière entre modèles n'est pas en soi une frontière de sécurité.

N'exposez pas publiquement le point d'accès MCP sans authentification et protection du transport adaptées. N'utilisez pas les réponses du modèle secondaire comme seul fondement d'une décision importante. Les politiques du fournisseur et les journaux du client et de l'hôte comptent aussi. Voir le [tableau des menaces](docs/fr/security-model.md).
