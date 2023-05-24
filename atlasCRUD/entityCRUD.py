import requests
import json

# Configurar la conexión a Apache Atlas.
atlas_endpoint = 'http://10.0.27.41:21000'
username = 'admin'
password = 'admin'

# Crear una entidad.
def create_entity(entity_type, entity_attributes):
    endpoint = f'{atlas_endpoint}/api/atlas/v2/entity'
    headers = {'Content-Type': 'application/json'}

    entity = {
        'entity': {
            'typeName': entity_type,
            'attributes': entity_attributes
        }
    }

    response = requests.post(endpoint, data=json.dumps(entity), headers=headers, auth=(username, password))
    return response.json()

def create_entities(json_entities):
    endpoint = f'{atlas_endpoint}/api/atlas/v2/entity/bulk'
    headers = {'Content-Type': 'application/json'}

    response = requests.post(endpoint, data=json.dumps(json_entities), headers=headers, auth=(username, password))

    if response.status_code == 201:
        response_json = response.json()
        created_entities = response_json.get('guidAssignments', [])

        if created_entities:
            print("Entidades creadas:")
            for entity in created_entities:
                print(f" - Nombre: {entity['typeName']}, GUID: {entity['guid']}")
        else:
            print("No se crearon entidades.")
    else:
        print("Error al crear las entidades")
        print("Código de error:", response.status_code)

        try:
            response_json = response.json()
            print("Mensaje de error:", response_json)
        except json.JSONDecodeError as e:
            print(f"Error decoding response JSON: {e}")

# Obtener una entidad por su GUID.
def get_entity(entity_guid):
    endpoint = f'{atlas_endpoint}/api/atlas/v2/entity/guid/{entity_guid}'
    headers = {'Content-Type': 'application/json'}

    response = requests.get(endpoint, headers=headers, auth=(username, password))
    return response.json()

# Obtener entidades por tipo de entidad
def get_entities_by_type(entity_type):
    endpoint = f'{atlas_endpoint}/api/atlas/v2/search/basic'
    headers = {'Content-Type': 'application/json'}

    query = {
        'typeName': entity_type
    }

    response = requests.post(endpoint, json=query, headers=headers, auth=(username, password))
    return response.json()

# Obtener entidades por nombre
def get_entities_by_name(entity_name):
    endpoint = f'{atlas_endpoint}/api/atlas/v2/search/basic'
    headers = {'Content-Type': 'application/json'}

    query = {
        'query': entity_name
    }

    response = requests.post(endpoint, json=query, headers=headers, auth=(username, password))
    return response.json()

# Actualizar una entidad.
def update_entity(entity_guid, entity_attributes):
    endpoint = f'{atlas_endpoint}/api/atlas/v2/entity/guid/{entity_guid}'
    headers = {'Content-Type': 'application/json'}

    entity = {
        'entity': {
            'attributes': entity_attributes
        }
    }

    response = requests.put(endpoint, data=json.dumps(entity), headers=headers, auth=(username, password))
    return response.json()
    

# Eliminar una entidad.
def delete_entity(entity_guid):
    endpoint = f'{atlas_endpoint}/api/atlas/v2/entity/guid/{entity_guid}'
    headers = {'Content-Type': 'application/json'}

    response = requests.delete(endpoint, headers=headers, auth=(username, password))
    return response.json()

# Ejemplo de uso:
if __name__ == "__main__":

    # entity_type = "sample_column"

    # entities = get_entities_by_type(entity_type)
    # print("Entidades encontradas:")
    # for entity in entities['entities']:
    #     print(entity)
    
    # Definir los detalles de la entidad a crear.
    entity_type = "Column"
    entity_attributes = {
        'table_catalog': 'John Doe',
        'age': 30,
        'email': 'johndoe@example.com',
        'qualifiedName': 'John Doe'
    }

    # Crear una nueva entidad.
    create_response = create_entity(entity_type, entity_attributes)
    entity_guid = create_response['guid']
    print("Entidad creada:", create_response)

    # # Obtener la entidad recién creada.
    # entity_info = get_entity(entity_guid)
    # print("Información de la entidad:", entity_info)

    # # Actualizar los atributos de la entidad.
    # updated_attributes = {
    #     'name': 'John Smith',
    #     'age': 35,
    #     'email': 'johnsmith@example.com'
    # }
    # update_response = update_entity(entity_guid, updated_attributes)
    # print("Entidad actualizada:", update_response)

    # # Eliminar la entidad.
    # delete_response = delete_entity(entity_guid)
    # print("Entidad eliminada:", delete_response)
    # print('-----------------------------')
    # entity = get_entity('84321134-1964-4055-8095-be24aee961cb')
    # print(entity)
    # delete_response = delete_entity('84321134-1964-4055-8095-be24aee961cb')
    # print("Entidad eliminada:", delete_response)
    # delete_response = delete_entity('e8000d02-b82c-420e-8a0b-145154cf554e')
    # delete_response = delete_entity('e594dcd4-36b6-434e-8c8f-30ff3d8a8f00')
    # delete_response = delete_entity('b4c1e30e-7226-4501-bc57-99543b0da711')
    
    
    #entities = get_entities_by_name("company_id")
    #print(entities)

