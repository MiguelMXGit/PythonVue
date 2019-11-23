from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from random import randrange
import pandas as pd
import numpy as np
import math 
import psycopg2

# instantiate the app
app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'

# enable CORS
cors = CORS(app, resources={r"/*": {"origins": "*"}})

# variables
PUNTOS_USUARIO = pd.DataFrame()
PUNTOS_FUNCION = pd.DataFrame()
FUNCION = ""
ERROR_RELATIVO = 0.0
# sanity check route
# login route
@app.route('/authentication', methods=['POST'])
@cross_origin()
def authenticateUser():
    # get request
    post_data = request.get_json(force=True)
    username = post_data['username']
    password = post_data['password']
    response_object = {'status':'success'}
    if (searchUser(username,password)):
        response_object['login'] = 'success'
    else:
        response_object['login'] = 'fail'
    
    return jsonify(response_object)
    
def searchUser(username,password):
    # instantiate  Database
    db = "dbname='VuejsLogin' user='postgres' host='localhost' password='oracle'"
    try:
        conn = psycopg2.connect(db)
        cursor = conn.cursor()
    except:
        print ("Unable to connect to the database")
        return False
    # login logic
    cursor.execute("""SELECT id FROM users WHERE username='{}' AND password='{}' """.format(username,password) )
    rows = cursor.fetchall()
    if (len(rows)>0):
        return True 
    return False
    
# chart route
@app.route('/grafica', methods=['GET', 'POST'])
@cross_origin()
def all_grafica():
    global PUNTOS_USUARIO
    global PUNTOS_FUNCION
    global FUNCION
    global ERROR_RELATIVO
    response_object={'status':'success'}
    if (request.method == 'POST'):
        post_data = request.get_json(force=True)
        # obtener arreglos de la peticion
        user_X_list = np.fromstring(post_data['listaX'],dtype=int, sep=',')
        user_Y_list = np.fromstring(post_data['listaY'],dtype=int, sep=',')
        # obtener index de los puntos que formaran la funcion
        random_index = generate_Random_Index(user_X_list)
        # obtener index de los puntos restantes para probar el error
        rest_index = get_rest_index(random_index,len(user_X_list))
        # obtener los puntos que formaran la funcion
        puntos_funcion_X = user_X_list[random_index]
        puntos_funcion_Y = user_Y_list[random_index]
        # puntos restantes para probar el error de la funcion
        puntos_reales_X = user_X_list[rest_index]
        puntos_reales_Y = user_Y_list[rest_index]
        # obtener polinomios de grado 1 al 6
        polinomios = generate_Polinomios(puntos_funcion_X,puntos_funcion_Y)
        # obtener mejor polinomio y su error relativo
        # infoMejorPolinomio es un arreglo que contiene ['mejorPolinomio','error relativo']
        infoMejorPolinomio = mejor_Polinomio(polinomios,puntos_reales_X,puntos_reales_Y)
        f=infoMejorPolinomio[0]
        ERROR_RELATIVO = infoMejorPolinomio[1]
        # calcular nuevas x's & y's
        x_new = np.linspace(min(user_X_list)-3, max(user_X_list)+3, 50)
        y_new = f(x_new)
        # preparar datos para el response
        PUNTOS_USUARIO = pd.DataFrame({'X': user_X_list, 'Y': user_Y_list})
        PUNTOS_FUNCION = pd.DataFrame({'X': x_new, 'Y': y_new})
        FUNCION = str(f)
        #preparar response
        response_object['puntosUsuario'] = PUNTOS_USUARIO.to_dict(orient='records')
        response_object['puntosFuncion'] = PUNTOS_FUNCION.to_dict(orient='records')
        response_object['funcion'] = FUNCION
        response_object['errorRelativo'] = ERROR_RELATIVO
    else:
        response_object['puntosUsuario'] = PUNTOS_USUARIO.to_dict(orient='records')
        response_object['puntosFuncion'] = PUNTOS_FUNCION.to_dict(orient='records')
        response_object['funcion'] = FUNCION
        response_object['errorRelativo'] = ERROR_RELATIVO
                 
    return jsonify(response_object)

def generate_Polinomios(X_list, Y_list):
    polinomios = []
    for i in range(1,7):
        z = np.polyfit(X_list, Y_list, i)
        polinomios.append(np.poly1d(z))
    return polinomios

def generate_Random_Index(lista):
    random_index = []
    mitad = len(lista)/2
    mitad =  int(mitad)

    while(len(random_index)<=mitad):
        aux = randrange(0,len(lista))
        if not(aux in lista):
            random_index.append(aux)

    return random_index

def mejor_Polinomio(polinomios,puntos_reales_x, puntos_reales_y):
    infoMejorPolinomio = []
    menorError = -1.0
   
    for f in polinomios:
        erroresAbsolutos = 0.0
        erroresRelativos = 0.0
        for i in range(0,len(puntos_reales_x)):
            # obtener el error absoluto
            erroresAbsolutos += math.fabs(puntos_reales_y[i] - f(puntos_reales_x[i])) 
            try:
                erroresRelativos += ((math.fabs(puntos_reales_y[i] - f(puntos_reales_x[i])))/math.fabs(puntos_reales_y[i]))*100
            except ZeroDivisionError:
                pass

        if (erroresAbsolutos < menorError) or (menorError < 0.0):
            menorError=erroresAbsolutos
            erroresRelativos = erroresRelativos/len(puntos_reales_x)
            infoMejorPolinomio = [f,erroresRelativos]
    return infoMejorPolinomio

def get_rest_index(random_index, longitud_lista):
    rest_index=[]
    for i in range(0,longitud_lista):
        if not i in random_index:
            rest_index.append(i)
    return rest_index

if __name__ == '__main__':
    app.run(debug=True)