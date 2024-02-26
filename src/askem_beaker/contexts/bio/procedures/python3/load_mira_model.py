import copy, requests
from mira.sources.amr import model_from_json
amr_json = requests.get("{{ model_url }}", auth={{auth_details}}, timeout=10).json()
{{ var_name|default("model") }} = model_from_json(amr_json)
_{{ var_name|default("model") }}_orig = copy.deepcopy({{ var_name|default("model") }})