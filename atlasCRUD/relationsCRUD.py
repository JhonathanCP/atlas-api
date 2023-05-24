import requests

# Configurar la conexión a Apache Atlas.
atlas_endpoint = 'http://10.0.27.41:21000'
username = 'admin'
password = 'admin'


# Crear una relación.
def create_relationship(entity_guid1, entity_guid2, relationship_type):
    endpoint = f'{atlas_endpoint}/api/atlas/v2/relationship'
    headers = {'Content-Type': 'application/json'}

    payload = {
        'typeName': relationship_type,
        'end1': {'guid': entity_guid1},
        'end2': {'guid': entity_guid2}
    }

    response = requests.post(endpoint, json=payload, headers=headers, auth=(username, password))
    return response.json()

# Obtener una relación por su GUID.
def get_relationship(relationship_guid):
    endpoint = f'{atlas_endpoint}/api/atlas/v2/relationship/guid/{relationship_guid}'

    response = requests.get(endpoint, auth=(username, password))
    return response.json()

# Actualizar una relación.
def update_relationship(relationship_guid, attributes):
    endpoint = f'{atlas_endpoint}/api/atlas/v2/relationship/guid/{relationship_guid}'
    headers = {'Content-Type': 'application/json'}

    payload = {
        'attributes': attributes
    }

    response = requests.put(endpoint, json=payload, headers=headers, auth=(username, password))
    return response.json()

# Eliminar una relación.
def delete_relationship(relationship_guid):
    endpoint = f'{atlas_endpoint}/api/atlas/v2/relationship/guid/{relationship_guid}'

    response = requests.delete(endpoint, auth=(username, password))
    return response.json()

# Ejemplo de uso:
if __name__ == "__main__":
    # Definir los detalles de las entidades y la relación.
    entity_guid1 = "12345678-1234-1234-1234-1234567890AB"
    entity_guid2 = "87654321-4321-4321-4321-0987654321BA"
    relationship_type = "Contains"

    # Crear la relación.
    create_response = create_relationship(entity_guid1, entity_guid2, relationship_type)
    relationship_guid = create_response['guid']
    print("Relación creada:", create_response)

    # Obtener la relación recién creada.
    relationship_info = get_relationship(relationship_guid)
    print("Información de la relación:", relationship_info)

    # Actualizar los atributos de la relación.
    updated_attributes = {
        'description': 'Updated relationship'
    }
    update_response = update_relationship(relationship_guid, updated_attributes)
    print("Relación actualizada:", update_response)

    # Eliminar la relación.
    delete_response = delete_relationship(relationship_guid)
    print("Relación eliminada:", delete_response)