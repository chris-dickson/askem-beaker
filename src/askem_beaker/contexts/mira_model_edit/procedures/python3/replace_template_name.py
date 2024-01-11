def replace_template_name(model_name, old_name: str, new_name: str):
    """Replace the name of a template in a given model."""
    if old_name not in {template.name: template for template in model_name.templates}:
        raise ValueError(f"Template with name {old_name} not found in the given model")

    for template in model_name.templates:
        if template.name == old_name:
            template.name = new_name
    return model_name

model_name = replace_template_name({{ var_name|default("model_name") }}, {{ var_name|default("old_name") }}, {{ var_name|default("new_name") }})