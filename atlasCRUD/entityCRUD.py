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

def create_entity_APIONLY(entity_type, entity_attributes):

    endpoint1 = f'{atlas_endpoint}/api/atlas/v2/entity'
    headers = {'Content-Type': 'application/json'}
    response2 = requests.get(f'{atlas_endpoint}/api/atlas/v2/types/typedefs', headers=headers, auth=(username, password))
    if response2.status_code == 200:
        response_json = response2.json()

        entity_defs = response_json.get('entityDefs', [])
        for entity_def in entity_defs:
            if entity_def.get('name') == entity_type:
                attribute_defs = entity_def.get('attributeDefs', [])
                attribute_names = [attr_def.get('name') for attr_def in attribute_defs]
                attribute_names.append('name')
                attribute_names.append('qualifiedName')
    print(attribute_names)

    # Verificar que el número de atributos coincida
    # if len(entity_attributes) != len(attribute_names):
    #     print("El número de atributos no coincide.")
    #     return None

    entity = {
        'entity': {
            'typeName': entity_type,
            'attributes': {}
        }
    }

    for i, attribute_value in enumerate(entity_attributes):
        attribute_name = attribute_names[i]
        entity['entity']['attributes'][attribute_name] = attribute_value

    response = requests.post(endpoint1, data=json.dumps(entity), headers=headers, auth=(username, password))

    if response.status_code == 200:
        response_json = response.json()
        created_entity_guid = response_json.get('guidAssignments', {}).get(entity_type)
        if created_entity_guid:
            print("Entidad creada con GUID:", created_entity_guid)
            return created_entity_guid
        else:
            print("No se pudo obtener el GUID de la entidad creada.")
            return None
    else:
        print("Error al crear la entidad.")
        print("Código de error:", response.status_code)
        return None
    
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

def delete_entity_by_name(entity_name):
    # Buscar todas las entidades con el nombre especificado
    search_endpoint = f'{atlas_endpoint}/api/atlas/v2/search/basic'
    headers = {'Content-Type': 'application/json'}

    query = {
        'query': entity_name
    }

    search_response = requests.post(search_endpoint, json=query, headers=headers, auth=(username, password))
    search_results = search_response.json()

    entities_found = search_results.get('entities', [])
    if len(entities_found) == 0:
        print("No se encontró ninguna entidad con el nombre:", entity_name)
        return None

    # Eliminar cada entidad encontrada por su GUID
    deleted_entities = []
    for entity in entities_found:
        entity_guid = entity['guid']
        delete_endpoint = f'{atlas_endpoint}/api/atlas/v2/entity/guid/{entity_guid}'
        delete_response = requests.delete(delete_endpoint, headers=headers, auth=(username, password))
        if delete_response.status_code == 200:
            deleted_entities.append(entity_guid)
            print("Entidad eliminada:", entity_name)

    if deleted_entities:
        return deleted_entities
    else:
        print("Error al eliminar la entidad.")
        print("Código de error:", delete_response.status_code)
        return None

def create_entities_from_json(json_data, entity_type):
    for entity_data in json_data:
        updated_entity_data = dict(entity_data)  # Crear una copia del diccionario original

        for attribute, value in entity_data.items():
            if attribute.endswith("_name"):
                updated_entity_data['name'] = value
                updated_entity_data['qualifiedName'] = value

        create_entity(entity_type, updated_entity_data)

# Ejemplo de uso:
if __name__ == "__main__":

    # entity_type = "sample_column"

    # entities = get_entities_by_type(entity_type)
    # print("Entidades encontradas:")
    # for entity in entities['entities']:
    #     print(entity)
    
    # Definir los detalles de la entidad a crear.
    entity_type = "Table"
    entity_attributes = {"name": "ftsma10", "qualifiedName": "ftsma10","table_catalog": "dl_essi", "table_schema": "public", "table_name": "ftsma10", "table_type": "BASE TABLE"}
    data = [{"table_catalog":"dl_essi","table_schema":"public","table_name":"ftsma10","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"cbeci10","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"cbecv10","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"cmprs10","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"qtsop10","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"hbmin10","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"htsin10","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"htaho10","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"ctppe10_2020","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"ctppe10_2022","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"cbpar10","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"ctppe10","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"mtadd10_2020","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"mtadd10_2022","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"mtadd10_2023","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"mtatr10_2020","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"qbcep10","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"qbdeq10","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"qbefi10","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"qbesa10","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"qbeso10","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"ctsci10","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"ftsmd10","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"ctppe10_2019","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"cbcoc10","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"cbepc10","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"cbeps10","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"cbgoc10","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"cbmoc10","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"cbmsp10","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"ctppe10_2021","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"ctppe10_2024","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"ctsci10_2021","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"hbeca10","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"hbtca10","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"qbgcc10","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"qbtho10","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"qbmso10","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"qbpro10","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"qbpso10","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"qbriq10","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"qmane10","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"qmcqs10","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"qmcqx10","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"ctpco10","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"cbraa10","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"cbsex10","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"cbtci10","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"cbtdi10","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"cbthp10","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"cbtid10","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"cbtpc10","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"cbtpp10","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"cmace10","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"cmact10","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"cmaho10","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"cmcas10","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"cmcon10","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"cmcpp10","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"cmdia10","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"cmpac10","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"cmper10","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"cbere10","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"cmras10","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"cmsho10","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"cmtse10","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"ctaam10","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"ctppe10_2023","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"ctsci10_2019","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"ctsci10_2020","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"ctsci10_2022","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"ctsci10_2023","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"hbeph10","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"hbooi10","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"hmcam10","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"hmese10","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"htdah10","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"hthod10","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"hthos10","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"mbacp10","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"mbdat10","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"mbegp10","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"mbepe10","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"mbmeg10","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"mbpae10","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"mbrai10","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"mbtac10","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"mbtae10","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"mbtoe10","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"mmeme10","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"mtadd10_2019","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"mtadd10_2021","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"mtade10_2019","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"mtade10_2020","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"mtade10_2021","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"mtade10_2022","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"mtade10_2023","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"mtaem10_2019","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"mtaem10_2020","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"mtaem10_2021","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"mtaem10_2022","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"mtaem10_2023","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"mtatr10_2019","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"mtatr10_2021","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"mtatr10_2022","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"mtatr10_2023","table_type":"BASE TABLE"},{"table_catalog":"dl_essi","table_schema":"public","table_name":"mtdae10","table_type":"BASE TABLE"}]
    create_entities_from_json(data, entity_type)
    #create_entities_from_json(data, entity_type)
    #entities = get_entities_by_name('testapi')
    #print(entities)

    #delete_entity_by_name('testapi')

    # Crear una nueva entidad.
    #create_response = create_entity_APIONLY(entity_type, entity_attributes)
    #entity_guid = create_response['guid']
    #print("Entidad creada:", create_response)

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

