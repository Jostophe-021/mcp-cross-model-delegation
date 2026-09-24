# Exemple de déploiement générique

[English](../en/deployment-example.md) | Français

Le premier essai recommandé utilise Python et un client MCP local. Une architecture générique permanente peut comprendre une petite VM, un serveur MCP en conteneur et un gestionnaire de secrets. Il s'agit d'un **exemple d'architecture**, pas d'un déploiement automatisé ni d'une promesse d'hébergement gratuit. Vérifiez les prix actuels du cloud, du trafic sortant, du stockage et de l'API du modèle avant de créer des ressources.

```text
Client MCP distant compatible
    | (tunnel privé facultatif)
    v
Petite VM : client tunnel -> 127.0.0.1:8000/mcp
                              -> API Gemini par HTTPS sortant
Gestionnaire de secrets -> environnement du processus à l'exécution
```

Utilisez une identité de service dédiée n'ayant accès qu'au secret d'exemple nécessaire, un pare-feu privé par défaut, HTTPS sortant et aucun port MCP entrant. Fournissez la clé API à l'exécution depuis un gestionnaire de secrets tel que `YOUR_SECRET_NAME` ; ne la passez pas comme argument de build Docker et ne la commitez pas dans un fichier. Lancez le serveur avec son écoute locale par défaut. Un client tunnel partageant l'espace réseau de la VM peut atteindre cette adresse loopback. Protégez séparément son identifiant de contrôle et faites-le tourner selon les recommandations du fournisseur. Évitez d'inscrire secrets ou prompts complets dans les journaux.

Le [Secure MCP Tunnel d'OpenAI](https://developers.openai.com/api/docs/guides/secure-mcp-tunnels) est un transport facultatif pour les clients OpenAI compatibles. Le guide officiel explique la création d'un tunnel dans votre propre compte, l'exécution de `tunnel-client` là où il peut atteindre le serveur MCP local et la sélection de Tunnel dans une application en mode développeur. Suivez ce guide pour les commandes et autorisations actuelles ; ce dépôt ne contient volontairement aucun identifiant de tunnel, point d'accès ni identifiant de production. Le tunnel privé ne répond pas aux exigences de soumission d'un plugin public.

Avant d'accepter du trafic, testez `/mcp` avec le client prévu, confirmez l'écoute locale du serveur, examinez le redémarrage des conteneurs, consultez les politiques de données du fournisseur et configurez une alerte budgétaire en sachant qu'elle n'impose pas un plafond ferme. Une écoute distante exige une conception distincte d'authentification et de sécurité du transport. Pour le développement local, suivez le [README](../../README.fr.md) plutôt que de créer des ressources cloud.
