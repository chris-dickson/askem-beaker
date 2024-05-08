"""
structure :
    An iterable of pairs corresponding to a directed network structure
    where each of the pairs has two strata. If none given, will assume a complete
    network structure. If no structure is necessary, pass an empty list.

directed :
    Should the reverse direction conversions be added based on the given structure?

cartesian_control :
    If true, splits all control relationships based on the stratification.

    This should be true for an SIR epidemiology model, the susceptibility to
    infected transition is controlled by infected. If the model is stratified by
    vaccinated and unvaccinated, then the transition from vaccinated
    susceptible population to vaccinated infected populations should be
    controlled by both infected vaccinated and infected unvaccinated
    populations.

    This should be false for stratification of an SIR epidemiology model based
    on cities, since the infected population in one city won't (directly,
    through the perspective of the model) affect the infection of susceptible
    population in another city.

modify_names :
    If true, will modify the names of the concepts to include the strata
    (e.g., ``"S"`` becomes ``"S_boston"``). If false, will keep the original
    names.
"""

model = stratify(
    template_model=model,
    key= "{{ key }}",
    strata={{ strata}},
    structure= {{ structure|default(None) }},
    directed={{ directed|default(False) }},
    cartesian_control={{ cartesian_control|default(False) }},
    modify_names={{ modify_names|default(True) }}
)