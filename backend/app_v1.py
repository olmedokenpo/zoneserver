from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5500"}})  # Permitir solicitudes desde cualquier origen

# Área de ejemplo-1
bufferGeoJSON = {
    "type": "Feature",
    "geometry": {
        "type": "Polygon",
        "coordinates": [[
            [-2.667412995999939, 37.209045411000034],
            [-1.997562051999978, 37.209045411000034],
            [-1.997562051999978, 37.55778122000004],
            [-2.667412995999939, 37.55778122000004],
            [-2.667412995999939, 37.209045411000035]
        ]]
    },
    "properties": {}
}

#Fin Area de ejemplo-1

# Ruta para obtener el área de ejemplo
@app.route('/areas', methods=['GET'])
def get_areas():
    return jsonify(bufferGeoJSON)

# Ruta para manejar clics en el mapa
@app.route('/clic', methods=['POST'])
def handle_click():
    data = request.json  # Obtener los datos enviados en el cuerpo de la solicitud
    latlng = data.get('latlng')  # Obtener las coordenadas del clic
    print("Clic en el mapa en las coordenadas:", latlng)

    # Aquí puedes realizar cualquier procesamiento adicional necesario con las coordenadas

    # Por ejemplo, podrías guardar las coordenadas en una base de datos
    # O podrías realizar algún cálculo basado en las coordenadas

    # Luego, puedes enviar una respuesta al frontend si es necesario
    # Por ejemplo, puedes enviar un mensaje de confirmación
    ##OJO
    
    ##Fin OJO
    response_data = {'message': 'Coordenadas recibidas correctamente'}
    return jsonify(response_data), 200

if __name__ == '__main__':
    app.run(debug=True)
