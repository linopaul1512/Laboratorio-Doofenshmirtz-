from flask import Flask, request, render_template, redirect, url_for, flash
from db import Categorias, Indicaciones, Examenes
from bson.objectid import ObjectId

app = Flask(__name__, template_folder="./Templates")
app.config['SECRET_KEY'] = "clave secreta"

categoriaList = []

@app.route("/list", methods=["GET"])
def getListCategorias():
    categoriaList = Categorias.find()

    return render_template('lista.html.jinja', categoriaList=categoriaList)

@app.route('/', methods=['GET', 'POST'])
def agregar_categoria():
    if request.method == "POST":
        IDCategoria = request.form['IDCategoria']
        Nombre = request.form['Nombre']
        Descripcion = request.form['Descripcion']


        object = {
            'IDCategoria': IDCategoria,
            'Nombre': Nombre,
            'Descripcion' : Descripcion
        }
        Categorias.insert_one(object)
        return redirect(url_for('getList'))
    return render_template("add.html.jinja")



@app.route('/<id>', methods=['GET'])
def buscar_categoria(id):
    oid = ObjectId(id)
    categoria = Categorias.find_one({'_id': oid})
    return render_template('detail.html.jinja', categoria = categoria)

@app.route('/update/<id>', methods=['GET', 'POST'])
def modificar_categoria(id):
    oid = ObjectId(id)
    categoria = Categorias.find_one({'_id': oid})
    if request.method == "POST":
        new_element = request.form
        Categorias.replace_one({'_id': oid}, 
                                         {'IDCategoria': new_element['IDCategoria'],
                                          'Nombre': new_element['Nombre'],
                                          'Descripcion': new_element['Descripcion']})    
        return redirect(url_for('getList'))
    return render_template("update.html.jinja", categoria=categoria)

@app.route('/delete/<id>', methods=['GET'])
def eliminar_categoria(id):
    oid = ObjectId(id)
    categoria = Categorias.delete_one({'_id': oid})
    return redirect(url_for('getList'))



#CRUD de Indicaciones

@app.route("/list", methods=["GET"])
def getListIndicaciones():
    indicacionesList = Indicaciones.find()

@app.route('/', methods=['GET', 'POST'])
def agregar_indicaciones():
    if request.method == "POST":
        IDIndicacion = request.form['IDIndicacion']
        Descripcion = request.form['Descripcion']


        object = {
            'IDIndicacion': IDIndicacion,
            'Descripcion' : Descripcion
        }
        Categorias.insert_one(object)
        return redirect(url_for('getList'))
    return render_template("add.html.jinja")



@app.route('/<id>', methods=['GET'])
def buscar_indicacion(id):
    oid = ObjectId(id)
    indicaciones = Indicaciones.find_one({'_id': oid})
    return render_template('detail.html.jinja', indicaciones = indicaciones)

@app.route('/update/<id>', methods=['GET', 'POST'])
def modificar_indicacion(id):
    oid = ObjectId(id)
    indicaciones = Categorias.find_one({'_id': oid})
    if request.method == "POST":
        new_element = request.form
        Categorias.replace_one({'_id': oid}, 
                                         {'IDIndicacion': new_element['IDIndicacion'],
                                          'Descripcion': new_element['Descripcion']})    
        return redirect(url_for('getList'))
    return render_template("update.html.jinja", indicaciones=indicaciones)

@app.route('/delete/<id>', methods=['GET'])

def eliminar_categoria(id):
    oid = ObjectId(id)
    indicaciones = Categorias.delete_one({'_id': oid})
    return redirect(url_for('getList'))



#CRUD de examenes



@app.route("/list", methods=["GET"])
def getListExamenes():
    examenesList = Examenes.find()
    return render_template('lista.html.jinja', examenesList=examenesList)

@app.route('/', methods=['GET', 'POST'])
def agregar_examen():
    if request.method == "POST"and Categorias:
        IDExamen= request.form['IDExamen']
        IDCategoria = request.form['IDCategoria']
        TipoMuestra = request.form['TipoMuestra']
        Precio = request.form['Precio']
        IDIndicacion = request.form['IDIndicacion']


        object = {
            'IDExamen': IDExamen,
            'IDCategoria' : IDCategoria,
            'TipoMuestra' : TipoMuestra,
            'Precio' : Precio,
            'IDIndicacion' : IDIndicacion
        }
        Examenes.insert_one(object)
        return redirect(url_for('getList'))
    return render_template("add.html.jinja")



@app.route('/<id>', methods=['GET'])
def buscar_examen(id):
    oid = ObjectId(id)
    examenes = examenes.find_one({'_id': oid})
    return render_template('detail.html.jinja', examenes = examenes)

@app.route('/update/<id>', methods=['GET', 'POST'])
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
        return redirect(url_for('getList'))
    return render_template("update.html.jinja", examenes=examenes)

@app.route('/delete/<id>', methods=['GET'])

def eliminar_examen(id):
    oid = ObjectId(id)
    examenes = Examenes.delete_one({'_id': oid})
    return redirect(url_for('getList'))






if __name__ == "__main__":
    app.run(debug=True)
