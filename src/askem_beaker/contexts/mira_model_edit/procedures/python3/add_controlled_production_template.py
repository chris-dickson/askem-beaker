outcome_concept = Concept(name = "{{ outcome_name|default('outcome_name') }}")
controller_concept = Concept(name = "{{controller_name|default('controller_name')}}")
parameter_unit = Unit(expression = sympy.Symbol("{{ parameter_units|default('parameter_units')}}"))

parameters = {
    "{{ parameter_name|default('parameter_name')}}": Parameter(name = "{{ parameter_name|default('parameter_name')}}", value = {{ parameter_value|default("parameter_value")}}, units = parameter_unit, description = "{{ parameter_description|default('parameter_description')}}")
}

initials = { 
    "{{outcome_name|default('outcome_name')}}": Initial(concept = outcome_concept, expression = sympy.Float({{outcome_initial_value|default(1)}})),
    "{{controller_name|default('controller_name')}}": Initial(concept = controller_concept, expression = sympy.Float({{controller_initial_value|default(1)}}))
}

model = model.add_template(
    template = ControlledProduction(
        outcome = outcome_concept,
        controller = controller_concept,
        rate_law = sympy.parsing.sympy_parser.parse_expr("{{ template_expression|default('EXPRESSION_HERE') }}"),
        name = "{{ template_name|default('template_name') }}"
    ),
    parameter_mapping = parameters,
    initial_mapping = initials
)
