

transformit = {
'Actor' : 'actor',
'Action' : 'action',
'Object' : 'object',
'Property' : 'property',
'IsActorOf' : 'is_actor_of',
'HasProperty' : 'has_property',
'ActsOn' : 'acts_on',
'IsActorOf' : 'is_actor_of',
'Reference' : 'reference',
'Aggregate' : 'aggregate',
'IsAggregateOf' : 'is_aggregate_of',
'source' : 'has_source',
'target' : 'has_target',
'Enumeration' : 'enumeration',
'Literal' : 'literal',
'HasLiteral': 'has_literal',
'HasReference': 'has_reference',
'many':'many',
'hasName': 'has_name',
'isEntity': 'is_entity',
#Deprecated
'Modifier' : 'property',
'IsModifierOf' : 'is_property_of'
}

transformitreverse = {
'IsActorOf' : 'has_actor',
'HasProperty' : 'is_property_of',
'ActsOn' : 'receives_action',
'IsActorOf' : 'has_actor',
#Deprecated
'IsModifierOf' : 'has_property',
'IsAggregateOf' : 'has_aggregate',
'source' : 'is_source_of',
'target' : 'is_target_of',
'HasLiteral' : 'is_literal_of',
'HasReference': 'is_reference_of'
}

