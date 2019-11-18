from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import pandas as pd
import numpy as np
import plotly as py



# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
#app.config.from_object(__name__) //causa error CORS
app.config['CORS_HEADERS'] = 'Content-Type'

# enable CORS
cors = CORS(app, resources={r"/*": {"origins": "*"}})

# variables
PUNTOS_USUARIO = pd.DataFrame()
PUNTOS_FUNCION = pd.DataFrame()
FUNCION = ""

# sanity check route
@app.route('/grafica', methods=['GET', 'POST'])
@cross_origin()
def all_grafica():
    global PUNTOS_USUARIO
    global PUNTOS_FUNCION
    global FUNCION
    
    response_object={'status':'success'}
    if (request.method == 'POST'):
        post_data = request.get_json(force=True)
        #obtener arreglos de la peticion
        user_X_list = np.fromstring(post_data['listaX'],dtype=int, sep=',')
        user_Y_list = np.fromstring(post_data['listaY'],dtype=int, sep=',')
        # calcular polinomio
        z = np.polyfit(user_X_list, user_Y_list, len(user_X_list)-1)
        f = np.poly1d(z)
        # calcular nuevas x's & y's
        x_new = np.linspace(min(user_X_list), max(user_X_list), 50)
        y_new = f(x_new)
        # preparar datos para el response
        PUNTOS_USUARIO = pd.DataFrame({'X': user_X_list, 'Y': user_Y_list})
        PUNTOS_FUNCION = pd.DataFrame({'X': x_new, 'Y': y_new})
        FUNCION = str(f)
        #preparar response
        response_object['puntosUsuario'] = PUNTOS_USUARIO.to_dict(orient='records')
        response_object['puntosFuncion'] = PUNTOS_FUNCION.to_dict(orient='records')
        response_object['funcion'] = FUNCION
    else:
        response_object['puntosUsuario'] = PUNTOS_USUARIO.to_dict(orient='records')
        response_object['puntosFuncion'] = PUNTOS_FUNCION.to_dict(orient='records')
        response_object['funcion'] = FUNCION
                 
    return jsonify(response_object)


if __name__ == '__main__':
    app.run()