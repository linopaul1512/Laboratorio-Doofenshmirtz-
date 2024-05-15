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
    examenesList = Examenes.find()
    return render_template('lista.html.jinja', examenesList=examenesList)

@app.route('examenes/agregar', methods=['GET', 'POST'])
def agregar_examen():
    if request.method == "POST"and Categorias:
        IDExamen= request.form['IDExamen']
        IDCategoria = request.form['IDCategoria']
        TipoMuestra = request.form['TipoMuestra']
        Precio = request.form['Precio']
        IDIndicacion = request.form['IDIndicacion']
        Categorias.find()

        object = {
            'IDExamen': IDExamen,
            'IDCategoria' : IDCategoria,
            'TipoMuestra' : TipoMuestra,
            'Precio' : Precio,
            'IDIndicacion' : IDIndicacion
        }
        Examenes.insert_one(object)
        return redirect(url_for('getListExamenes'))
    return render_template("agregarexamen.html.jinja")



@app.route('/examenes/<id>', methods=['GET'])
def buscar_examen(id):
    oid = ObjectId(id)
    examenes = examenes.find_one({'_id': oid})
    return render_template('detail.html.jinja', examenes = examenes)

@app.route('/examenes/update/<id>', methods=['GET', 'POST'])
def modificar_examen(id):
    oid = ObjectId(id)
    examenes = Examenes.find_one({'_id': oid})
    if request.method == "POST":
        new_element = request.form
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




if __name__ == "__main__":
    app.run(debug=True)
