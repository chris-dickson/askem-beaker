from mira.metamodel.ops import stratify

if "{{ schema_name }}" == "regnet":
    {{ var_name|default("model") }} = stratify(
        template_model={{ var_name|default("model") }},
        **{{ stratify_kwargs }}, structure=[]
    )
else:
    {{ var_name|default("model") }} = stratify(
        template_model={{ var_name|default("model") }},
        **{{ stratify_kwargs }}
    )
