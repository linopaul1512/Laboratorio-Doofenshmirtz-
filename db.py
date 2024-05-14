import pymongo



#Inicia IP y Puerto
client = pymongo.MongoClient('localhost', 27017)

#también podemos indicar string de conexión
#client = pymongo.MongoClient('mongo://localhost//locaalhost :27017')

db = client["Proyecto_Final"]

#Acccedemos  al bd
Categorias = db["Categorias"]
Examenes = db["Examenes"]
Indicaciones = db["Indicaciones"]
