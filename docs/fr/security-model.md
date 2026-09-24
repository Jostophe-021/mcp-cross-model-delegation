# Modèle de sécurité et tableau des menaces

[English](../en/security-model.md) | Français

**Une frontière entre modèles n'est pas en soi une frontière de sécurité.** La séparation du prompt atténue les mélanges accidentels ; elle ne garantit aucune résistance aux injections adversariales. Le point d'accès MCP est local et sans authentification. Seul l'opérateur peut décider si un texte peut être transmis à Google.

| Risque | Atténuation actuelle | Limite restante |
| --- | --- | --- |
| Instructions cachées dans CONTEXT | TASK et CONTEXT sont deux champs JSON distincts ; le prompt subordonne explicitement CONTEXT | Le modèle peut encore suivre le texte malveillant ; tester et vérifier |
| Exfiltration du contexte sensible | Les descriptions des outils préviennent l'appelant ; aucune lecture automatique d'application ou de fichier | L'appelant peut toujours envoyer du texte confidentiel à Google |
| Fournisseur compromis ou indisponible | Délai d'expiration, erreurs fixes et assainies, aucun nouvel essai automatique | Le fournisseur peut être lent, faux ou malveillant |
| Réponse ou preuve inventée | Champs de preuve structurés et exigence de vérification par l'orchestrateur | La preuve vient du modèle et n'est pas vérifiée indépendamment |
| JSON ou structure invalide | Demande de schéma et contrôle local strict des formes et types | Une réponse plausible peut encore être factuellement fausse |
| Fuite dans les journaux | Aucun prompt, réponse ou télémétrie personnalisée journalisé par l'application | Le client, l'environnement, le réseau et le fournisseur peuvent journaliser séparément |
| Écoute MCP publique accidentelle | Liste explicite d'adresses loopback ; refus d'une écoute publique sans authentification | Un utilisateur ou processus local peut atteindre le point d'accès |
| Secrets commitées | `.gitignore`, `.env.example` fictif, scan CI | Les règles d'ignore n'empêchent pas `git add -f` ; inspecter l'historique |
| Dépendance compromise | Dépendances directes figées, lockfile, audit CI | Le risque de chaîne d'approvisionnement demeure ; mettre à jour et examiner |
| Réponse secondaire non vérifiée | README et outils demandent une vérification | Un orchestrateur peut échouer à vérifier |

Les objets d'erreur exposent des codes et messages fixes, jamais de texte d'exception, prompt, contexte, clé ou trace de pile. Les limites d'entrée et de sortie bornent la charge mais pas les dépenses. `store=False` empêche la conservation de l'objet Interaction pour cette requête selon l'API Gemini actuelle ; les autres traitements et politiques du fournisseur s'appliquent toujours. Consultez la [documentation de Google sur les journaux](https://ai.google.dev/gemini-api/docs/logs-datasets) et les conditions de votre compte.

Avant de connecter un produit distant, décidez de l'identité du client MCP, de l'authentification, du chiffrement du transport, des autorisations et des journaux. Le [Secure MCP Tunnel d'OpenAI](https://developers.openai.com/api/docs/guides/secure-mcp-tunnels), facultatif, garde le serveur MCP privé mais ne supprime pas la décision de partager des données avec Google. N'exposez pas `0.0.0.0:8000` en modifiant la garde sans conception de sécurité adaptée.
