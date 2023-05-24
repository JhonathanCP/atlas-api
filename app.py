from atlasCRUD.typeCRUD import *
from atlasCRUD.entityCRUD import *
from flask import Flask, render_template, request
from flask import redirect, url_for

app = Flask(__name__, template_folder='./templates')

# Ruta principal
# @app.route('/')
# def index():
#     return render_template('index.html')

@app.route('/render_types')
def render_types():
    types = get_entity_types()
    return render_template('render_types.html', types=types)

@app.route('/fill_entity', methods=['GET', 'POST'])
def fill_entity():
    opcion_seleccionada = request.form['type']
    attributes = get_entity_attributes(opcion_seleccionada)
    return render_template('fill_entity.html', attributes=attributes)

@app.route('/save_entity', methods=['POST'])
def save_entity():
    filled_attributes = request.form.getlist('attr[]')
    print(filled_attributes)
    type = 'Tabla'
    create_entity_APIONLY(type, filled_attributes)
    return 'Creado'

# @app.route('/entity/read', methods=['GET', 'POST'])
# def read_entity_form():
#     if request.method == 'POST':
#         entity_type = request.form['entity_type']
#         entity_id = request.form['entity_id']

#         # Leer la entidad
#         entity = get_entity(entity_type, entity_id)

#         return render_template('entity_read.html', entity=entity)

#     return render_template('entity_read_form.html')

# @app.route('/entity/update', methods=['GET', 'POST'])
# def update_entity_form():
#     if request.method == 'POST':
#         entity_type = request.form['entity_type']
#         entity_id = request.form['entity_id']
#         attributes = {}

#         # Recorrer los campos del formulario para obtener los atributos
#         for key, value in request.form.items():
#             if key not in ['entity_type', 'entity_id']:
#                 attributes[key] = value

#         # Actualizar la entidad
#         update_entity(entity_type, entity_id, attributes)

#         return redirect(url_for('index'))

#     return render_template('entity_update_form.html')

# @app.route('/entity/delete', methods=['GET', 'POST'])
# def delete_entity_form():
#     if request.method == 'POST':
#         entity_type = request.form['entity_type']
#         entity_id = request.form['entity_id']

#         # Eliminar la entidad
#         delete_entity(entity_type, entity_id)

#         return redirect(url_for('index'))

#     return render_template('entity_delete_form.html')

# # Rutas para CRUD de tipos de entidad
# @app.route('/type/create', methods=['GET', 'POST'])
# def create_entity_type_form():
#     if request.method == 'POST':
#         entity_type = request.form['entity_type']
#         super_types = request.form.getlist('super_types')

#         # Crear el tipo de entidad
#         create_entity_type(entity_type, super_types)

#         return redirect(url_for('index'))

#     return render_template('type_create.html')

# @app.route('/type/delete', methods=['GET', 'POST'])
# def delete_entity_type_form():
#     if request.method == 'POST':
#         entity_type = request.form['entity_type']

#         # Eliminar el tipo de entidad
#         delete_entity_type(entity_type)

#         return redirect(url_for('index'))

#     return render_template('type_delete_form.html')

# # Rutas para CRUD de relaciones
# @app.route('/relationship/create', methods=['GET', 'POST'])
# def create_relationship_form():
#     if request.method == 'POST':
#         relationship_type = request.form['relationship_type']
#         attributes = {}

#         # Recorrer los campos del formulario para obtener los atributos
#         for key, value in request.form.items():
#             if key != 'relationship_type':
#                 attributes[key] = value

#         # Crear la relación
#         create_relationship(relationship_type, attributes)

#         return redirect(url_for('index'))

#     return render_template('relationship_create.html')

# @app.route('/relationship/delete', methods=['GET', 'POST'])
# def delete_relationship_form():
#     if request.method == 'POST':
#         relationship_id = request.form['relationship_id']

#         # Eliminar la relación
#         delete_relationship(relationship_id)

#         return redirect(url_for('index'))

#     return render_template('relationship_delete_form.html')

if __name__ == '__main__':
    app.run(debug=True)