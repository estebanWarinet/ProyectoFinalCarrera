import flask
from flask import request, jsonify

import CDRFG as CDRFG

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/ejecutarCDRFG', methods = ['POST'])
def processJson():
    data = request.get_json()
    DatosEntrada = data['DatosEntrada']
    datos=DatosEntrada[0]["datos"]
    datosAvanzados = datos["datosAvanzados"]
    datosGrilla = datos["datosGrilla"]
    datosNecesarios = datos["datosNecesarios"]
    CDRFG.main(datosGrilla,datosNecesarios,datosAvanzados)
    return jsonify({
        'datosNecesarios': datosNecesarios, 
        'datosGrilla':datosGrilla, 
        'datosAvanzados':datosAvanzados
    })

app.run()