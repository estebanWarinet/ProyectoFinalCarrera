import flask
from flask_cors import CORS
from flask import request, jsonify, send_file, send_from_directory
from multiprocessing.dummy import Pool

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
    
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        uploaded_file.save(uploaded_file.filename)

    CDRFG.main(request.form)
    return jsonify({'result': 'recibido'})

@app.route('/descargar-desdeDirectorio', methods = ['GET'])
def return_files_fromDirectory():
	try:
		return  send_file('./DecaimientoCoherencia.png')
         
	except Exception as e:
		return str(e)

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