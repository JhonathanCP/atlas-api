from atlasCRUD.typeCRUD import *


attributes = get_entity_attributes('Table')
print(attributes)

entity_type = "Table"
super_types = ["DataSet"]
attribute_defs = [
    {
        'name': 'table_catalog',
        'typeName': 'string',
        'isOptional': False
    },
    {
        'name': 'table_schema',
        'typeName': 'string',
        'isOptional': False
    },
    {
        'name': 'table_name',
        'typeName': 'string',
        'isOptional': False
    },
    {
        'name': 'table_type',
        'typeName': 'string',
        'isOptional': False
    },
]

response = create_entity_type(entity_type, super_types, attribute_defs)
print("Tipo de entidad creada:", response)