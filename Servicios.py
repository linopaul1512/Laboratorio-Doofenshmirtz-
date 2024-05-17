from flask import Flask, request, render_template, redirect, url_for, flash, session
from db import Categorias, Indicaciones, Examenes, Usuarios
from bson.objectid import ObjectId
import random
from collections import Counter
#hola
app = Flask(__name__, template_folder="./Templates")
app.config['SECRET_KEY'] = "clave secreta"

categoriaList = []
indicacionList = []
examenList = []
usuarioList = []

#Método para verificar si el usuaio entrante inició sesión
def validar_sesion():
    print('username' not in session)
    if 'username' not in session:
        flash('Debes iniciar sesión para acceder a esta página', 'Error')
        return redirect(url_for('iniciar_sesion'))

# Ruta de inicio para usuarios no logeados
@app.route('/', methods=['GET'])
def hogar_no_registado():
    if 'Usuario' in session:
        return redirect(url_for('hogar_registrados'))
    return render_template('hogarnoregistrados.html.jinja')


#Método para registrar usuario
@app.route('/register', methods=['GET', 'POST'])
def agregar_usuario():
    if request.method == 'POST':
        Usuario = request.form['Usuario']
        Contrasena = request.form['Contrasena']
        ContrasenaConfirmada = request.form['ContrasenaConfirmada']
        if Contrasena == ContrasenaConfirmada:
            usuaarioexistente = Usuarios.find_one({"Usuario": Usuario})
            if usuaarioexistente:
                flash('El nombre de usuario ya existe. Por favor, elige otro.', 'Error')
            else:
                nuevousuario = {"Usuario": Usuario, "Contrasena": Contrasena}
                Usuarios.insert_one(nuevousuario)
                flash('Usuario registrado correctamente.', 'Ëxito')
                return redirect(url_for('login'))
        else:
            flash('Contraseña incorrrecta.', 'Error')
    return render_template('agregarusuario.html.jinja')

# Meétodo para iniciar sesión
@app.route('/login', methods=['GET', 'POST'])
def iniciar_sesion():
    if request.method == 'POST':
        Usuario = request.form['Usuario']
        Contrasena = request.form['Contrasena']
        usuario = Usuarios.find_one({"username": Usuario})
        if usuario and usuario['Contrasena'] == Contrasena:
            session['Usuario'] = Usuario
            flash('Se inició sesión correctamente', 'Ëxito')
            return redirect(url_for('base.html.jinja'))  # Redirige al layout después de iniciar sesión
        else:
            flash('Los datos ingresados son erróneos', 'Error')
    return render_template('iniciarsesion.html.jinja')

# Método para renderizar 
@app.route('/render_layout')
def renderizar():
    validar_sesion()
    return render_template('base.html.jinja')

#Método para cerrar sesión
@app.route('/logout', methods=['GET'])
def logout():
    session.pop('Usuario', None)
    return redirect(url_for('hogar_no_registado'))


# Ruta de inicio para usuarios logeados
@app.route('/home', methods=['GET', 'POST'])
def hogar_registrados():
    validar_sesion()
    return redirect(url_for('renderizar')) 



#CRUD para categoría
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


@app.route('/indicaciones/update/<id>', methods=['GET', 'POST'])
def modificar_indicacion(id):
    oid = ObjectId(id)
    indicacion = Indicaciones.find_one({'_id': oid})
    if request.method == "POST":
        new_element = request.form
        Indicaciones.replace_one({'_id': oid}, 
                                         {'IDIndicacion': new_element['IDIndicacion'],
                                          'Descripcion': new_element['Descripcion']})    
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
        Precio = int(request.form['Precio'])
        IDIndicacion = request.form['IDIndicacion']

        object = {
            'IDExamen': IDExamen,
            'IDCategoria' : IDCategoria,
            'IDIndicacion' : IDIndicacion,
            'Nombre' : Nombre,
            'TipoMuestra' : TipoMuestra,
            'Precio' : Precio,
        }

        Examenes.insert_one(object) 
        print(object)
        return redirect(url_for('getListExamenes'))
    categorias = Categorias.find()
    examenes = Examenes.find()
    indicaciones = Indicaciones.find()
    return render_template('agregarexamen.html.jinja', categorias=categorias, indicaciones=indicaciones, examenes = examenes)

@app.route('/<id>', methods=['GET'])
def buscar_examen(id):
    oid = ObjectId(id)
    examen = Examenes.find_one({'_id': oid})
    
    # Buscar nombre de la categoría
    categoria = Categorias.find_one({"IDCategoria": examen["IDCategoria"]})
    if categoria:
        NombreCategoria = categoria.get("Nombre", "No encontrado")
    else:
        NombreCategoria = "No encontrado"

    # Buscar descripción de las indicaciones
    indicacion = Indicaciones.find_one({"IDIndicacion": examen["IDIndicacion"]})
    if indicacion:
        DescripcionIndicacion = indicacion.get("Descripcion", "No encontrado")
    else:
        DescripcionIndicacion = "No encontrado"

    return render_template('detallesExamen.html.jinja', examen=examen, DescripcionIndicacion=DescripcionIndicacion, NombreCategoria=NombreCategoria)

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

#reporte
@app.route('/report')
def mostrar_reporte():
    # Contabilizar categoría 
    cancategorias = []
    for examen in Examenes.find():
        categoria = Categorias.find_one({'IDCategoria': examen['IDCategoria']})
        if categoria:
            categoriaid = str(categoria['_id'])
            if categoriaid in cancategorias:
                cancategorias[categoriaid] += 1
            else:
                cancategorias[categoriaid] = 1

    # Contabilizar las indicaciones
    canindicaciones = []
    for examen in Examenes.find():
        indicacion = Indicaciones.find_one({'IDIndicacion': examen['IDIndicacion']})
        if indicacion: 
            indicacionid = str(indicacion['_id'])
            if indicacionid in canindicaciones:
                canindicaciones[indicacionid] += 1
            else:
                canindicaciones[indicacionid] = 1


    # Indicar la indicación más común
    if canindicaciones:
        indicacionmascomun_id = max(canindicaciones, key=canindicaciones.get)
        indicacionmascomun_doc = Indicaciones.find_one({'_id': ObjectId(indicacionmascomun_id)})
        if indicacionmascomun_doc:
            indicacionmascomun = indicacionmascomun_doc.get('Descripcion', 'No encontrado')
        else:
            indicacionmascomun = 'No encontrado'
    else:
        indicacionmascomun = 'No encontrado'

    # Intervalo de precios
    intervalodeprecios = {
        '1-100': 0,
        '101-200': 0,
        '201-300': 0,
        '301-500': 0,
        '501+': 0
    }

    for examen in Examenes.find():
        precio = examen['Precio']
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


        print(intervalodeprecios)

        return render_template('reporte.html.jinja', cancategorias=cancategorias, indicacionmascomun=indicacionmascomun, intervalodeprecios=intervalodeprecios)

#Catálogo
@app.route("/catalogo/list", methods=["GET"])
def getListCatalogo():
    examenList = Examenes.find()
    return render_template('catalogo.html.jinja', examenList=examenList)


@app.route('/catalogo/update/<id>', methods=['GET', 'POST'])
def modificar_examen_catalogo(id):
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
        return redirect(url_for('getListCatalogo'))
    return render_template("modificarExamen.html.jinja", examenes=examenes)



if __name__ == "__main__":
    app.run(debug=True)




