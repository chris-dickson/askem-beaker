model = stratify(
    template_model=model,
    key= "{{ key }}",
    strata={{ strata}},
    structure= {{ structure|default(None) }},
    directed={{ directed|default(False) }},
    cartesian_control={{ cartesian_control|default(False) }},
    modify_names={{ modify_names|default(True) }}
)