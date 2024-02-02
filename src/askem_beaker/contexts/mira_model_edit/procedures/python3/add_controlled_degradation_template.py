subject_concept = Concept(name = "{{ subject_name|default('subject_name') }}")
controller_concept = Concept(name = "{{controller_name|default('controller_name')}}")
parameter_unit = Unit(expression = sympy.Symbol("{{ parameter_units|default('parameter_units')}}"))

parameters = {
    "{{ parameter_name|default('parameter_name')}}": Parameter(name = "{{ parameter_name|default('parameter_name')}}", value = {{ parameter_value|default("parameter_value")}}, units = parameter_unit, description = "{{ parameter_description|default('parameter_description')}}")
}

initials = { 
    "{{subject_name|default('subject_name')}}": Initial(concept = subject_concept, expression = sympy.Float({{subject_initial_value|default(1)}})),
    "{{controller_name|default('controller_name')}}": Initial(concept = controller_concept, expression = sympy.Float({{controller_concept|default(1)}}))
}

model = model.add_template(
    template = ControlledDegradation(
        subject = subject_concept,
        controller = controller_concept,
        rate_law = sympy.parsing.sympy_parser.parse_expr("{{ template_expression|default('EXPRESSION_HERE') }}"),
        name = "{{ template_name|default('template_name') }}"
    ),
    parameter_mapping = parameters,
    initial_mapping = initials
)
