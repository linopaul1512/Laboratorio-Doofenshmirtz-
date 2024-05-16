from flask import Flask, request, render_template, redirect, url_for, flash
from db import Categorias, Indicaciones, Examenes
from bson.objectid import ObjectId
import random


app = Flask(__name__, template_folder="./Templates")
app.config['SECRET_KEY'] = "clave secretas"

categoriaList = []
indicacionList = []
examenList = []


@app.route("/categoria/list", methods=["GET"])
def getListCategorias():
    categoriaList = Categorias.find()
    return render_template('listaCategoria.html.jinja', categoriaList=categoriaList)

@app.route('/categoria/agregar', methods=['GET', 'POST'])
def agregar_categoria():

    if request.method == "POST":
        IDCategoria = [random.randint(0, 1000) for _ in range(1)]
        Nombre = request.form['Nombre']
        Descripcion = request.form['Descripcion']


        object = {
            'IDCategoria': IDCategoria,
            'Nombre' : Nombre,
            'Descripcion' : Descripcion
        }
        Categorias.insert_one(object)
        return redirect(url_for('getListCategorias'))
    return render_template("agregarcategoria.html.jinja")


"""
@app.route('/<id>', methods=['GET'])
def buscar_categoria(id):
    oid = ObjectId(id)
    categoria = Categorias.find_one({'_id': oid})
    return render_template('detail.html.jinja', categoria = categoria)
"""


@app.route('/categoria/update/<id>', methods=['GET', 'POST'])
def modificar_categoria(id):
    oid = ObjectId(id)
    categoria = Categorias.find_one({'_id': oid})
    if request.method == "POST":
        new_element = request.form
        Categorias.replace_one({'_id': oid}, 
                                         {'IDCategoria': new_element['IDCategoria'],
                                            'Nombre': new_element['Nombre'],
                                            'Descripcion': new_element['Descripcion']})    
        return redirect(url_for('getListCategorias'))
    return render_template("modificarCategoria.html.jinja", categoria = categoria)




@app.route('/categoria/delete/<id>', methods=['POST'])
def eliminar_categoria(id):
    oid = ObjectId(id)
    categoria = Categorias.delete_one({'_id': oid})
    return redirect(url_for('getListCategorias'))



#CRUD de Indicaciones

@app.route("/indicaciones/list", methods=["GET"])
def getListIndicaciones():
    indicacionList = Indicaciones.find()
    return render_template('listaIndicacion.html.jinja', indicacionList=indicacionList)

@app.route('/indicaciones/agregar', methods=['GET', 'POST'])
def agregar_indicacion():
    if request.method == "POST":
        IDIndicacion = [random.randint(0, 1000) for _ in range(1)]
        Descripcion = request.form['Descripcion']


        object = {
            'IDIndicacion': IDIndicacion,
            'Descripcion' : Descripcion
        }
        Indicaciones.insert_one(object)
        return redirect(url_for('getListIndicaciones'))
    return render_template("agregarIndicacion.html.jinja")


"""
@app.route('/<id>', methods=['GET'])
def buscar_indicacion(id):
    oid = ObjectId(id)
    indicaciones = Indicaciones.find_one({'_id': oid})
    return render_template('detail.html.jinja', indicaciones = indicaciones)

"""

@app.route('/indicaciones/update/<id>', methods=['GET', 'POST'])
def modificar_indicacion(id):
    oid = ObjectId(id)
    indicacion = Indicaciones.find_one({'_id': oid})
    if request.method == "POST":
        new_element = request.form
        Indicaciones.replace_one({'_id': oid}, 
                                         {'Descripcion': new_element['Descripcion']})    
        return redirect(url_for('getListIndicaciones'))
    return render_template("modificarIndicacion.html.jinja", indicacion=indicacion)



@app.route('/indicaciones/delete/<id>', methods=['POST'])
def eliminar_indicacion(id):
    oid = ObjectId(id)
    indicaciones = Indicaciones.delete_one({'_id': oid})
    return redirect(url_for('getListIndicaciones'))




#CRUD de examenes

@app.route("/examenes/list", methods=["GET"])
def getListExamenes():
    examenList = Examenes.find()
    return render_template('listaExamen.html.jinja', examenList=examenList)

@app.route('/examenes/agregar', methods=['GET', 'POST'])
def agregar_examen():
    if request.method == "POST":
        IDExamen = [random.randint(0, 1000) for _ in range(1)]
        IDCategoria = request.form['IDCategoria']
        Nombre = request.form['Nombre']
        TipoMuestra = request.form['TipoMuestra']
        Precio = request.form['Precio']
        IDIndicacion = request.form['IDIndicacion']

        object = {
            'IDExamen': IDExamen,
            'IDCategoria' : IDCategoria,
            'IDIndicacion' : IDIndicacion,
            'Nombre' : Nombre,
            'TipoMuestra' : TipoMuestra,
            'Precio' : Precio,
            'IDIndicacion' : IDIndicacion
        }

        Examenes.insert_one(object) 
        print(object)
        return redirect(url_for('getListExamenes'))
    categorias = Categorias.find()
    examenes = Examenes.find()
    indicaciones = Indicaciones.find()
    return render_template('agregarexamen.html.jinja', categorias=categorias, indicaciones=indicaciones, examenes = examenes)


@app.route('/examenes/<id>', methods=['GET'])
def buscar_examen(id):
    oid = ObjectId(id)
    examenes = examenes.find_one({'_id': oid})
    
    return render_template('detallesExamen.html.jinja', examenes=examenes)

@app.route('/<id>', methods=['GET'])
def get_element(id):
    oid = ObjectId(id)
    element = Examenes.find_one({'_id': oid})
    return render_template('detallesExamen.html.jinja', element = element)

@app.route('/examenes/update/<id>', methods=['GET', 'POST'])
def modificar_examen(id):
    oid = ObjectId(id)
    examenes = Examenes.find_one({'_id': oid})

    if request.method == "POST":
        new_element = request.form
        print(new_element)
        Examenes.replace_one({'_id': oid}, 
                                         {'IDExamen': new_element['IDExamen'],
                                          'IDCategoria': new_element['IDCategoria'],
                                          'TipoMuestra': new_element['TipoMuestra'],
                                          'Precio': new_element['Precio'],
                                          'IDIndicacion': new_element['IDIndicacion']

                                          })    
        return redirect(url_for('getListExamenes'))
    return render_template("modificarExamen.html.jinja", examenes=examenes)


@app.route('/examenes/delete/<id>', methods=['POST'])
def eliminar_examen(id):
    oid = ObjectId(id)
    examenes = Examenes.delete_one({'_id': oid})
    return redirect(url_for('getListExamenes'))



#Métedos para el reporte
@app.route('/report')
def mostrar_reporte():
    # Generamos los datos necesarios para el informe
    examenesxcategoria = {}
    for exam in Examenes.find():
        categoria = Categorias.find_one({'_id': exam['IDCategoria']})
        categoria_nombre = categoria['Nombre']
        if categoria_nombre in examenesxcategoria:
            examenesxcategoria[categoria_nombre] += 1
        else:
            examenesxcategoria[categoria_nombre] = 1

    # Contar cuántas veces se repite cada IDIndicacion en los exámenes
    indicaciones_contador = {}
    for exam in Examenes.find():
        id_indicacion = exam['IDIndicacion']
        if id_indicacion in indicaciones_contador:
            indicaciones_contador[id_indicacion] += 1
        else:
            indicaciones_contador[id_indicacion] = 1

    # Encontrar la indicación más común
    indicacionmascomun_id = max(indicaciones_contador, key=indicaciones_contador.get)
    indicacionmascomun = Indicaciones.find_one({'_id': indicacionmascomun_id})['Descripcion']

    intervalodeprecios = {
        '1-100': 0,
        '101-200': 0,
        '201-300': 0,
        '301-500': 0,
        '501+': 0
    }
    for exam in Examenes.find():
        precio = exam['Precio']
        if precio <= 100:
            intervalodeprecios['1-100'] += 1
        elif precio <= 200:
            intervalodeprecios['101-200'] += 1
        elif precio <= 300:
            intervalodeprecios['201-300'] += 1
        elif precio <= 500:
            intervalodeprecios['301-500'] += 1
        else:
            intervalodeprecios['501+'] += 1

    return render_template('reporte.html.jinja', examenesxcategoria=examenesxcategoria, indicacionmascomun=indicacionmascomun, intervalodeprecios=intervalodeprecios)

if __name__ == "__main__":
    app.run(debug=True)
