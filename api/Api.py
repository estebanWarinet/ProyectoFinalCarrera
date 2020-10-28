import flask
from flask_cors import CORS
from flask import request, jsonify, send_file, send_from_directory
from multiprocessing.dummy import Pool
import base64

import CDRFG as CDRFG


app = flask.Flask(__name__)
cors = CORS(app,resources={r"/*": {"origins": "*"}})
app.config["DEBUG"] = True
app.config['CORS_HEADERS'] = 'Content-Type'
app.config["CORS_SUPPORTS_CREDENTIALS"]=True

pool = Pool(10)

@app.route('/descargarZip', methods = ['GET'])
def return_files_tut():
	try:
		return send_file('./api.zip',as_attachment=True, attachment_filename='tablas.zip')
	except Exception as e:
		return str(e)


@app.route('/upload', methods=['POST'])
def upload():
    if (request.form["archivoGrilla"] != "NO-Archivo"):
        print("Paso If")
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            uploaded_file.save(uploaded_file.filename)

    CDRFG.main(request.form)
    try:
        with open('./DecaimientoCoherencia.png', "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
    
    except Exception as e:
		    return str(e)

@app.route('/SinArchivo', methods=['POST'])
def SinArchivo():

    CDRFG.main(request.form)
    try:
        with open('./DecaimientoCoherencia.png', "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
    
    except Exception as e:
		    return str(e)

@app.route('/descargar-desdeDirectorio', methods = ['GET'])
def return_files_fromDirectory():
	try:
            with open('./DecaimientoCoherencia.png', "rb") as img_file:
                return base64.b64encode(img_file.read()).decode('utf-8')
         
	except Exception as e:
		return str(e)


## No se usa por ahora
@app.route('/ejecutarCDRFG', methods = ['POST'])
def processJson():
    data = request.get_json()
    datos=data["datos"]
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