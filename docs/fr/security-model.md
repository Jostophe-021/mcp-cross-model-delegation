# Modèle de sécurité et tableau des menaces

[English](../en/security-model.md) | Français

**Une frontière entre modèles n'est pas en soi une frontière de sécurité.** La séparation du prompt atténue les mélanges accidentels sans garantir une résistance aux injections. MCP reste local et sans authentification publique. L'appelant déclare `privacy_mode` ; le Router ne devine pas la confidentialité. Seul l'opérateur décide ce qui peut être envoyé à Google ou Anthropic.

| Risque | Atténuation actuelle | Limite restante |
| --- | --- | --- |
| Instructions cachées dans CONTEXT | TASK et CONTEXT sont deux champs JSON distincts ; le prompt subordonne explicitement CONTEXT | Le modèle peut encore suivre le texte malveillant ; tester et vérifier |
| Exfiltration du contexte sensible | Avertissements, aucune lecture automatique, listes de fournisseurs et mode local | L'appelant peut toujours envoyer du texte confidentiel à un fournisseur externe approuvé |
| Fournisseur compromis ou indisponible | Délai d'expiration, erreurs fixes, aucun retry applicatif, repli explicite sur erreur réessayable | Le fournisseur peut être lent, faux ou malveillant |
| Réponse ou preuve inventée | Recherche locale de citation exacte/normalisée et hash de source | Une citation présente ne prouve pas l'affirmation |
| JSON ou structure invalide | Demande de schéma et contrôle local strict des formes et types | Une réponse plausible peut encore être factuellement fausse |
| Fuite dans les journaux | Aucun prompt, réponse ou télémétrie personnalisée journalisé par l'application | Le client, l'environnement, le réseau et le fournisseur peuvent journaliser séparément |
| Écoute MCP publique accidentelle | Liste explicite d'adresses loopback ; refus d'une écoute publique sans authentification | Un utilisateur ou processus local peut atteindre le point d'accès |
| Secrets commitées | `.gitignore`, `.env.example` fictif, scan CI | Les règles d'ignore n'empêchent pas `git add -f` ; inspecter l'historique |
| Dépendance compromise | Dépendances directes figées, lockfile, audit CI | Le risque de chaîne d'approvisionnement demeure ; mettre à jour et examiner |
| Réponse secondaire non vérifiée | README et outils demandent une vérification | Un orchestrateur peut échouer à vérifier |

Les erreurs exposent des codes et messages fixes, jamais d'exception, prompt, contexte, clé ou trace de pile. Les logs applicatifs ne portent que sur ID, opération, fournisseur, modèle, politique, durée et statut. Les limites ne sont pas un plafond financier. Un `max_cost` strict rejette un coût inconnu sauf `allow_unknown_cost` explicite. `store=False` désactive la conservation de l'objet Interaction Gemini, sans supprimer les autres traitements du fournisseur. Consultez la [documentation de Google](https://ai.google.dev/gemini-api/docs/logs-datasets) et les conditions des deux fournisseurs.

Avant de connecter un produit distant, définissez identité du client, authentification, chiffrement, autorisations et journaux. Le [Secure MCP Tunnel d'OpenAI](https://developers.openai.com/api/docs/guides/secure-mcp-tunnels) est facultatif ; il garde l'écoute privée sans supprimer la décision de partager les données avec le fournisseur. N'exposez pas `0.0.0.0:8000` sans conception de sécurité adaptée. Aucune télémétrie personnalisée n'est activée.

## Dépendances de construction

Les actions CI sont figées sur des SHA de commit complets et la version lisible figure dans chaque workflow. L'image Docker de base reste `python:3.12-slim` afin que les reconstructions reçoivent les correctifs de sécurité amont. Cette étiquette mobile empêche une reproduction octet pour octet. Un digest pourra être figé lorsqu'un processus de mise à jour automatique et revu sera en place ; sans lui, les correctifs de l'image de base resteraient bloqués. Le lockfile et l'audit des dépendances couvrent les paquets Python, pas l'image de base.
