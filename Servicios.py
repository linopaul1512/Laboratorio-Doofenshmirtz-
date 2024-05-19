from flask import Flask, request, render_template, redirect, url_for, flash, session
from db import Categorias, Indicaciones, Examenes, Usuarios
from bson.objectid import ObjectId
import random
from collections import Counter

app = Flask(__name__, template_folder="./Templates")
app.config  ['SECRET_KEY'] = "clave secreta"

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
                return redirect(url_for('iniciar_sesion'))
        else:
            flash('Contraseña incorrrecta.', 'Error')
    return render_template('agregarusuario.html.jinja')

# Meétodo para iniciar sesión
@app.route('/login', methods=['GET', 'POST'])
def iniciar_sesion():
    if request.method == 'POST':
        Usuario = request.form['Usuario']
        Contrasena = request.form['Contrasena']
        usuario = Usuarios.find_one({"Usuario": Usuario})
        # Si se encuentra un usuario y la contraseña ingresada coincide con la almacenada en la base de datos
        if usuario and usuario['Contrasena'] == Contrasena:
            # Almacena el nombre de usuario en la sesión para indicar que el usuario ha iniciado sesión
            session['Usuario'] = Usuario
            # Muestra un mensaje de éxito al usuario
            flash('Se inició sesión correctamente', 'Éxito')
            # Redirige al usuario a la función 'renderizar'
            return redirect(url_for('renderizar'))
        else:
            # Si los datos ingresados son incorrectos, muestra un mensaje de error
            flash('Los datos ingresados son erróneos', 'Error')
    # Si el usuario accede a la página de inicio de sesión, renderiza la plantilla de inicio de sesión
    return render_template('iniciarsesion.html.jinja')

# Método para renderizar 
@app.route('/render_layout')
def renderizar():
    validar_sesion()
    return render_template('base.html.jinja')

#Método para cerrar sesión
@app.route('/logout', methods=['GET'])
def cerrar_sesion():
    session.pop('Usuario', None)
    return redirect(url_for('hogar_no_registado'))


# Método para reedirigir a los usuarios que iniciaron sesión
@app.route('/home', methods=['GET', 'POST'])
def hogar_registrados():
    validar_sesion()
    return redirect(url_for('renderizar')) 



#CRUD para categoría
@app.route("/categoria/list", methods=["GET"])
def getListCategorias():
    validar_sesion()
    categoriaList = Categorias.find()
    return render_template('listaCategoria.html.jinja', categoriaList=categoriaList)

@app.route('/categoria/agregar', methods=['GET', 'POST'])
def agregar_categoria():
    validar_sesion()
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
    validar_sesion()
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
    validar_sesion()
    oid = ObjectId(id)
    categoria = Categorias.delete_one({'_id': oid})
    return redirect(url_for('getListCategorias'))



#CRUD de Indicaciones

@app.route("/indicaciones/list", methods=["GET"])
def getListIndicaciones():
    validar_sesion()
    indicacionList = Indicaciones.find()
    return render_template('listaIndicacion.html.jinja', indicacionList=indicacionList)

@app.route('/indicaciones/agregar', methods=['GET', 'POST'])
def agregar_indicacion():
    validar_sesion()
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
    validar_sesion()
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
    validar_sesion()
    oid = ObjectId(id)
    indicaciones = Indicaciones.delete_one({'_id': oid})
    return redirect(url_for('getListIndicaciones'))


#CRUD de examenes

@app.route("/examenes/list", methods=["GET"])
def getListExamenes():
    validar_sesion()
    examenList = Examenes.find()
    return render_template('listaExamen.html.jinja', examenList=examenList)

@app.route('/examenes/agregar', methods=['GET', 'POST'])
def agregar_examen():
    validar_sesion()
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
    validar_sesion()
    oid = ObjectId(id)
    examen = Examenes.find_one({'_id': oid})
    categoria = Categorias.find_one()
    indicacion = Indicaciones.find_one()
    

    return render_template('detallesExamen.html.jinja', examen=examen, indicacion=indicacion, categoria=categoria)

@app.route('/examenes/update/<id>', methods=['GET', 'POST'])
def modificar_examen(id):
    validar_sesion()
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
    categorias = Categorias.find()
    examenes = Examenes.find()
    indicaciones = Indicaciones.find()
    return render_template("modificarExamen.html.jinja", categorias=categorias, indicaciones=indicaciones, examenes = examenes)

@app.route('/examenes/delete/<id>', methods=['POST'])
def eliminar_examen(id):
    validar_sesion()
    oid = ObjectId(id)
    examenes = Examenes.delete_one({'_id': oid})
    return redirect(url_for('getListExamenes'))

#reporte
@app.route('/report')
def mostrar_reporte():
    validar_sesion()

    # Calcular la indicación más común
    indicacionList = [examen['IDIndicacion'] for examen in Examenes.find()]
    indicacion_counter = Counter(indicacionList)
    indicacionmascomun = indicacion_counter.most_common(1)[0][0]

    """
    Intente  de que mostrara la descripción pero me daba error NoneType:

    indicacionList = [examen['IDIndicacion'] for examen in Examenes.find()]
    indicacion_counter = Counter(indicacionList)
    indicacionmascomunid = indicacion_counter.most_common(1)[0][0]
    indicacionmascomun = Indicaciones.find_one({'_id': indicacionmascomunid})['Descripcion']

    """
    
    #La librería Counter aquí ayudío bastante y me redujo mi código en Servicios    
    # Contar cuántos exámenes hay por cada categoría
    cantcategorias = Counter([str(examen['IDCategoria']) for examen in Examenes.find()])
    categoriasbusq = {str(categoria['IDCategoria']): categoria['Nombre'] for categoria in Categorias.find()}
    print("Cantidad de categorías:", cantcategorias)
    print("Categorias Dict:", categoriasbusq)

    intervalodeprecios = [
        Examenes.count_documents({"Precio": {"$lte": 100}}),
        Examenes.count_documents({"Precio": {"$gt": 100, "$lte": 200}}),
        Examenes.count_documents({"Precio": {"$gt": 200, "$lte": 300}}),
        Examenes.count_documents({"Precio": {"$gt": 300, "$lte": 500}}),
        Examenes.count_documents({"Precio": {"$gt": 500}})
    ]
    # count_documents es una función de pymongo que contabiliza la cantidad de documentos en una colleción
    # en mi caso me ayudó bastante porque la entructura condicional que hice con contadores tradicionales no  estaban funcionando
    print(intervalodeprecios)

    return render_template('reporte.html.jinja',categoriasbusq=categoriasbusq, cantcategorias= cantcategorias,indicacionmascomun=indicacionmascomun, intervalodeprecios= intervalodeprecios)


#Catálogo
@app.route("/catalogo/list", methods=["GET"])
def getListCatalogo():
    validar_sesion()
    examenList = Examenes.find()
    categoriaList = Categorias.find()
    
    return render_template('catalogo.html.jinja', examenList=examenList, categoriaList=categoriaList)





@app.route('/catalogo/update/<id>', methods=['GET', 'POST'])
def modificar_examen_catalogo(id):
    validar_sesion()
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
    categorias = Categorias.find()
    indicaciones = Indicaciones.find()
    return render_template("modificarExamen.html.jinja", examenes=examenes, indicaciones=indicaciones, categorias=categorias)

#Nota: la barra de búsqueda para filtrar nunca me funcionó, lo intenté bastante



if __name__ == "__main__":
    app.run(debug=True)




