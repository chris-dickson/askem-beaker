def add_parameter(
    model,
    parameter_id: str,
    name: str = None,
    description: str = None,
    value: float = None,
    distribution: Distribution = None,
    units_mathml: str = None
):
    """Add a new parameter to the template model

    Parameters
    ----------
    model : JSON
        The model as an AMR JSON
    parameter_id :
        The ID of the new parameter to add
    name :
        The display name of the new parameter (optional)
    description :
        The description of the new parameter (optional)
    value :
        The value of the new parameter (optional)
    distribution :
        The distribution of the new parameter (optional)
    units_mathml :
        The units of the new parameter as a MathML XML string (optional)

    Returns
    -------
    : JSON
        The updated model as an AMR JSON
    """
    assert isinstance(model, TemplateModel)
    tm = model
    tm.add_parameter(
        parameter_id, name, description, value, distribution, units_mathml
    )
    return tm

model = add_parameter(
    model={{ model|default("model") }}, 
    parameter_id="{{ parameter_id|default(None) }}", 
    name="{{ name|default(None) }}", 
    description="{{ description|default(None) }}",
    value={{ value|default(None) }},
    distribution={{ distribution|default(None) }},
    units_mathml={{ units_mathml|default(None) }}
)