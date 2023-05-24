from flask import Flask, render_template, request
from flask import redirect, url_for
from atlasCRUD.entityCRUD import create_entity, read_entity, update_entity, delete_entity
from atlasCRUD.typeCRUD import create_entity_type, delete_entity_type
from atlasCRUD.relationsCRUD import create_relationship, delete_relationship

app = Flask(__name__)

# Ruta principal
@app.route('/')
def index():
    return render_template('index.html')

# Rutas para CRUD de entidades
@app.route('/entity/create', methods=['GET', 'POST'])
def create_entity_form():
    if request.method == 'POST':
        entity_type = request.form['entity_type']
        attributes = {}

        # Recorrer los campos del formulario para obtener los atributos
        for key, value in request.form.items():
            if key != 'entity_type':
                attributes[key] = value

        # Crear la entidad
        create_entity(entity_type, attributes)

        return redirect(url_for('index'))

    return render_template('entity_create.html')

@app.route('/entity/read', methods=['GET', 'POST'])
def read_entity_form():
    if request.method == 'POST':
        entity_type = request.form['entity_type']
        entity_id = request.form['entity_id']

        # Leer la entidad
        entity = read_entity(entity_type, entity_id)

        return render_template('entity_read.html', entity=entity)

    return render_template('entity_read_form.html')

@app.route('/entity/update', methods=['GET', 'POST'])
def update_entity_form():
    if request.method == 'POST':
        entity_type = request.form['entity_type']
        entity_id = request.form['entity_id']
        attributes = {}

        # Recorrer los campos del formulario para obtener los atributos
        for key, value in request.form.items():
            if key not in ['entity_type', 'entity_id']:
                attributes[key] = value

        # Actualizar la entidad
        update_entity(entity_type, entity_id, attributes)

        return redirect(url_for('index'))

    return render_template('entity_update_form.html')

@app.route('/entity/delete', methods=['GET', 'POST'])
def delete_entity_form():
    if request.method == 'POST':
        entity_type = request.form['entity_type']
        entity_id = request.form['entity_id']

        # Eliminar la entidad
        delete_entity(entity_type, entity_id)

        return redirect(url_for('index'))

    return render_template('entity_delete_form.html')

# Rutas para CRUD de tipos de entidad
@app.route('/type/create', methods=['GET', 'POST'])
def create_entity_type_form():
    if request.method == 'POST':
        entity_type = request.form['entity_type']
        super_types = request.form.getlist('super_types')

        # Crear el tipo de entidad
        create_entity_type(entity_type, super_types)

        return redirect(url_for('index'))

    return render_template('type_create.html')

@app.route('/type/delete', methods=['GET', 'POST'])
def delete_entity_type_form():
    if request.method == 'POST':
        entity_type = request.form['entity_type']

        # Eliminar el tipo de entidad
        delete_entity_type(entity_type)

        return redirect(url_for('index'))

    return render_template('type_delete_form.html')

# Rutas para CRUD de relaciones
@app.route('/relationship/create', methods=['GET', 'POST'])
def create_relationship_form():
    if request.method == 'POST':
        relationship_type = request.form['relationship_type']
        attributes = {}

        # Recorrer los campos del formulario para obtener los atributos
        for key, value in request.form.items():
            if key != 'relationship_type':
                attributes[key] = value

        # Crear la relación
        create_relationship(relationship_type, attributes)

        return redirect(url_for('index'))

    return render_template('relationship_create.html')

@app.route('/relationship/delete', methods=['GET', 'POST'])
def delete_relationship_form():
    if request.method == 'POST':
        relationship_id = request.form['relationship_id']

        # Eliminar la relación
        delete_relationship(relationship_id)

        return redirect(url_for('index'))

    return render_template('relationship_delete_form.html')

if __name__ == '__main__':
    app.run()