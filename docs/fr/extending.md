# Étendre la V1

[English](../en/extending.md) | Français

Les contrats figurent dans [`providers/base.py`](../../providers/base.py), [`routing.py`](../../routing.py) et [`benchmarks/runner.py`](../../benchmarks/runner.py). Isolez les SDK des fournisseurs et testez avec des données synthétiques et de faux clients.

## Ajouter un fournisseur

Implémentez `DelegationProvider` dans un nouveau module. Il suffit de passer son instance au `Router`, sans modifier ce dernier :

```python
from contracts import ProviderCapabilities
from routing import Router

class LocalExample:
    name = "local_example"
    model = "example-model"

    def capabilities(self) -> ProviderCapabilities:
        return ProviderCapabilities(structured_output=False, external_provider=False)

    def delegate(self, prompt: str, max_output_tokens: int, timeout_seconds: float) -> str:
        return "synthetic answer"

    def extract_findings(self, prompt: str, schema: dict,
                         max_output_tokens: int, timeout_seconds: float) -> str:
        raise NotImplementedError("structured extraction is unavailable")

router = Router({"local_example": LocalExample()})
```

Cet exemple illustre le contrat local ; ce n'est pas un adaptateur de production. La CLI et le serveur MCP ne découvrent **pas** automatiquement les nouvelles classes. Il faut les y brancher explicitement pour les exposer. Déclarez les capacités réelles : le routage peut écarter l'extraction avant tout appel.

## Ajouter une politique de routage

`Router.route(request, policy)` accepte un objet `RoutingPolicy` après filtrage des contraintes. `rank` reçoit seulement les noms admissibles et renvoie une liste ordonnée non vide, des codes de raison et des poids :

```python
class ReverseNamePolicy:
    name = "reverse_name"

    def rank(self, eligible, request, history):
        return sorted(eligible, reverse=True), ("reverse_name_order",), {}
```

Utilisez `router.route(request, ReverseNamePolicy())`. Les sélecteurs CLI/MCP ne reconnaissent actuellement que `manual`, `rules` et `benchmark_weighted` ; une politique personnelle s'utilise directement en Python ou demande une intégration explicite. Elle ne doit jamais réintroduire un fournisseur rejeté par les contraintes.

## Ajouter un évaluateur

`benchmarks.runner.run(..., evaluators={"exact_match": custom})` peut remplacer un évaluateur existant **dans un appel Python direct**. La fonction reçoit `(item, answer, findings)` et renvoie les champs de résultat :

```python
def custom(item, answer, findings):
    return {"evaluation_method": "custom", "evaluator": "exact_match",
            "answer_quality": answer == item.get("reference_answer"),
            "evidence_fidelity": None, "injection_success": None,
            "verification_success": None}
```

En V1, `load_dataset` n'accepte que les noms de `EVALUATORS`. Pour ajouter un **nouveau** nom JSONL, inscrivez-le dans cette liste et adaptez la CLI si nécessaire. Une simple correspondance Python ne suffit pas. Décrivez la méthode et validez-la sur des cas indépendants avant d'interpréter les résultats.

## Ajouter un jeu de données

Créez un JSONL UTF-8 avec un objet par ligne, un `id` unique et les champs texte `category`, `task`, `context` et `evaluator` reconnu. Exemple :

```json
{"id":"sum-1","category":"arithmetic","task":"Calculate 2 + 2.","context":"","evaluator":"numeric_match","reference_answer":"4","fake_answer":"4","dataset_version":"1"}
```

Lancez `uv run crossmodel bench run path/to/dataset.jsonl` pour la validation hors ligne. Le moteur utilise `fake_answer` en mode hors ligne ; ce résultat ne mesure pas les performances d'un LLM. Documentez la provenance, les droits de redistribution, la version, les références, les limites de l'évaluateur et les éventuelles injections. Voir le [format](../../benchmarks/README.fr.md) et la [méthodologie](methodology.md).
