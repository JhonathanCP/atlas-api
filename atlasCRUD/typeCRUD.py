import requests
import json

# Configurar la conexión a Apache Atlas.
atlas_endpoint = 'http://10.0.27.41:21000'
username = 'admin'
password = 'admin'

# Crear un tipo de entidad.
def create_entity_type(entity_type, super_types, attribute_defs):
    endpoint = f'{atlas_endpoint}/api/atlas/v2/types/typedefs'
    headers = {'Content-Type': 'application/json'}

    typedef = {
        'enumTypes': [],
        'structTypes': [],
        'classificationDefs': [],
        'entityDefs': [
            {
                'name': entity_type,
                'superTypes': super_types,
                'attributeDefs': attribute_defs
            }
        ],
        'relationshipDefs': []
    }

    response = requests.post(endpoint, json=typedef, headers=headers, auth=(username, password))
    return response.json()

# Obtener un tipo de entidad por nombre.
def get_entity_type(entity_type):
    endpoint = f'{atlas_endpoint}/api/atlas/v2/types/typedef/name/{entity_type}'
    headers = {'Content-Type': 'application/json'}

    response = requests.get(endpoint, headers=headers, auth=(username, password))
    return response.json()

def get_entity_types():
    endpoint = f'{atlas_endpoint}/api/atlas/v2/types/typedefs'
    response = requests.get(endpoint, auth=(username, password))

    if response.status_code == 200:
        data = response.json()
        entity_types = [entity_def['name'] for entity_def in data['entityDefs']]
        return entity_types
    else:
        return None

# Actualizar un tipo de entidad.
def update_entity_type(entity_type, super_types, attributes_defs):
    endpoint = f'{atlas_endpoint}/api/atlas/v2/types/typedef/name/{entity_type}'
    headers = {'Content-Type': 'application/json'}

    typedef = {
        'enumTypes': [],
        'structTypes': [],
        'classificationDefs': [],
        'entityDefs': [
            {
                'name': entity_type,
                'superTypes': super_types,
                'attributeDefs': attributes_defs
            }
        ],
        'relationshipDefs': []
    }

    response = requests.put(endpoint, json=typedef, headers=headers, auth=(username, password))
    return response.json()

#Obtener atributos de una entidad
def get_entity_attributes(entity_type):
    endpoint = f'{atlas_endpoint}/api/atlas/v2/types/typedefs'
    headers = {'Content-Type': 'application/json'}

    response = requests.get(endpoint, headers=headers, auth=(username, password))

    if response.status_code == 200:
        response_json = response.json()

        entity_defs = response_json.get('entityDefs', [])
        for entity_def in entity_defs:
            if entity_def.get('name') == entity_type:
                attribute_defs = entity_def.get('attributeDefs', [])
                attribute_names = [attr_def.get('name') for attr_def in attribute_defs]
                attribute_names.append('name')
                attribute_names.append('qualifiedName')
                return attribute_names

        print("No se encontró el tipo de entidad:", entity_type)
    else:
        print("Error al obtener el tipo de entidad")
        print("Código de error:", response.status_code)

        try:
            response_json = response.json()
            print("Mensaje de error:", response_json)
        except json.JSONDecodeError as e:
            print(f"Error decoding response JSON: {e}")

    return []

# Eliminar un tipo de entidad.
def delete_entity_type(entity_type):
    endpoint = f'{atlas_endpoint}/api/atlas/v2/types/typedef/name/{entity_type}'
    headers = {'Content-Type': 'application/json'}

    response = requests.delete(endpoint, headers=headers, auth=(username, password))
    if response.status_code == 204:
        print("Tipo de entidad eliminado exitosamente")
        return True
    else:
        print("Error al eliminar el tipo de entidad")
        print("Código de error:", response.status_code)

        try:
            response_json = response.json()
            print("Mensaje de error:", response_json)
        except json.JSONDecodeError as e:
            print(f"Error decoding response JSON: {e}")


# Ejemplo de uso:
if __name__ == "__main__":
    # Definir los detalles del tipo de entidad a crear.
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
    #entity_type = "DBTest"
    #super_types = ["DataSet"]
    #attribute_defs = []

    #entity_types = get_entity_types()
    #print(entity_types)

    #Crear un nuevo tipo de entidad.
    #response = create_entity_type(entity_type, super_types, attribute_defs)
    #print("Tipo de entidad creada:", response)

    # # Obtener el tipo de entidad recién creado.
    # entity_type_info = get_entity_type(entity_type)
    # print("Tipo de entidad:", entity_type_info)

    # # Actualizar el tipo de entidad.
    # update_response = update_entity_type(entity_type, super_types)
    # print("Tipo de entidad actualizado:", update_response)

    # # Eliminar el tipo de entidad.
    #delete_type_response = delete_entity_type(entity_type)
    #print("Tipo de entidad eliminado:", delete_type_response)
    
    attributes = get_entity_attributes('Table')
    print(attributes)
