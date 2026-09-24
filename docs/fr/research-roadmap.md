# Feuille de route de recherche

[English](../en/research-roadmap.md) | Français

## Hypothèse et vocabulaire de statut

**Hypothèse :** La délégation de sous-tâches délimitées à un modèle secondaire peut réduire la charge de contexte de l'orchestrateur ou améliorer certains traitements spécialisés, mais elle peut aussi introduire de la latence, des coûts, des risques de confidentialité et une propagation supplémentaire des erreurs. Ce dépôt n'a mesuré aucun résultat. Marquez chaque affirmation comme **implémenté**, **prévu**, **hypothèse** ou **mesuré** ; ne publiez un résultat mesuré qu'avec les données, la méthode et l'incertitude nécessaires à sa reproduction.

**Cible V1 :** fournisseurs Gemini et Anthropic, FakeProvider déterministe, Router sous contraintes, trois politiques explicites, vérification locale des preuves, benchmark séquentiel à quatre conditions, évaluateurs déterministes et CLI. Ce sont des capacités logicielles, pas des résultats comparatifs. **Plus tard :** fournisseur local compatible OpenAI, plus grands jeux publics, holdout, comparaison des politiques et vérification indépendante. Aucune date promise. Voir la [méthodologie](methodology.md).

## Conditions expérimentales

| ID | Condition | Question | Statut |
| --- | --- | --- | --- |
| A | Orchestrateur seul, un appel | Comment résout-il la tâche ? | Runner V1 |
| B | Délégation fixe, un appel | La délégation aide-t-elle ? | Runner V1 ; synthèse future |
| C | Délégation structurée et vérification locale | La structure aide-t-elle les preuves ? | Runner V1 |
| D | Contextes générés petit, moyen, grand | Comment évoluent qualité et latence ? | Générateur V1 |
| E | Mauvaise réponse secondaire synthétique | Un autre modèle la corrige-t-il ? | Fixture V1 ; étude future |
| F | Instructions malveillantes dans CONTEXT | TASK est-elle préservée ? | Fixture V1 ; étude élargie future |
| G | Recherche de citations exactes/normalisées | Les citations sont-elles présentes ? | Vérificateur V1 |
| H | Gemini et Anthropic sous un protocole | Quels effets dépendent du fournisseur ? | Adaptateurs V1 ; aucune conclusion |

Choisissez des tâches synthétiques, publiques ou explicitement redistribuables. Préenregistrez si possible les groupes d'entrée et les règles de score. Faites varier un facteur expérimental à la fois, consignez les versions et réglages des modèles, répétez les essais stochastiques et rapportez des intervalles de confiance ou une incertitude plutôt qu'un seul score gagnant. Les groupes de taille de contexte doivent être définis relativement aux limites d'entrée documentées de chaque modèle, sans tailles arbitraires universelles.

## Métriques et évaluation

Mesurez la qualité des réponses, l'exactitude factuelle, la fidélité des preuves, le taux d'hallucination, le taux de vérification réussie, le taux de réussite des injections, la latence, les tokens d'entrée/sortie de l'orchestrateur et du modèle délégué, le total des tokens, le coût estimé, le taux d'échec, de nouvel essai et d'expiration. Indiquez si les valeurs sont mesurées, estimées ou indisponibles. Séparez temps et tokens bruts des jugements subjectifs de qualité. N'inventez jamais consommation ou coût quand une API ne les fournit pas.

Utilisez des références humaines, des réponses de référence et des règles déterministes lorsque c'est adapté. Un modèle évaluateur indépendant ou plusieurs juges peuvent les compléter, mais un juge LLM peut partager des biais, être influencé par le style ou manquer la même erreur. Le modèle évalué ne doit pas être le seul juge de sa réponse. Consignez l'identité de l'évaluateur, la grille, l'accord entre juges et les cas contestés. Les prompts sensibles ne doivent pas être enregistrés par défaut ; utilisez des entrées synthétiques ou un jeu de données soumis à une gouvernance distincte avec consentement et règles de conservation explicites.

Chaque essai conserve version du projet, SHA Git si disponible, version du dataset, fournisseur, modèle, stratégie, réglages, seed, répétitions, horodatage, métriques, résultat et catégorie d'erreur. Voir le [format du runner](../../benchmarks/README.fr.md). Ne commitez ni données réelles ni identifiants. Une politique optimisée et évaluée sur le même jeu peut surajuster ses particularités ; séparez historique d'entraînement et holdout. V1 n'inclut ni auto-apprentissage ni routeur LLM.
