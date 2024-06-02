from flask import Flask, jsonify, request
from flask_cors import CORS
from sqlalchemy import create_engine, Column, Integer, String, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from geoalchemy2 import Geometry
import json

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5500"}})

# Definir el modelo SQLAlchemy
Base = declarative_base()

class Municipio(Base):
    __tablename__ = 'gadm41_esp_4'

    gid = Column(Integer, primary_key=True)
    name_4 = Column(String)
    geom = Column(Geometry(geometry_type='MULTIPOLYGON', srid=4326))  # Asegurarse de que el tipo de geometría es MULTIPOLYGON

# Crear una función para la conexión a la base de datos y la consulta
def obtener_municipio(lat, lng):
    engine = create_engine('postgresql://postgres:211018@localhost:5432/Catastro')
    Session = sessionmaker(bind=engine)
    session = Session()

    # Usar func para construir la geometría del punto
    punto = func.ST_SetSRID(func.ST_Point(lng, lat), 4326)

    # Transformar la geometría del municipio a una proyección métrica (por ejemplo, UTM zona 30N, EPSG:32630)
    utm_geom = func.ST_Transform(Municipio.geom, 32630)

    """
    #Consulta sin la inclusion del area
    municipio = session.query(  
        Municipio.name_4, 
        func.ST_AsGeoJSON(Municipio.geom).label('geom_geojson'),
        func.ST_Area(Municipio.geom).label('area')
        ).filter(func.ST_Contains(Municipio.geom, punto)).first()
        """
    
    #Consulta con la inclusion del area
    municipio = session.query( 
        Municipio.name_4, 
        func.ST_AsGeoJSON(Municipio.geom).label('geom_geojson'),
        func.ST_Area(utm_geom).label('area')
        ).filter(func.ST_Contains(Municipio.geom, punto)).first()

    if municipio:
        # Convertir la geometría a GeoJSON
        geom_geojson = json.loads(municipio.geom_geojson)
        municipio_geojson = {
            "type": "Feature",
            "geometry": geom_geojson,
            "properties": {"name_4": municipio.name_4,
                           "area":municipio.area/1000000} #El area esta en metros cuadrados
        }
        return municipio_geojson
    else:
        return None

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

    # Consultar la base de datos para obtener el municipio correspondiente
    municipio_geojson = obtener_municipio(latlng['lat'], latlng['lng'])

    if municipio_geojson:
        return jsonify(municipio_geojson), 200
    else:
        return jsonify({"message": "No se encontró ningún municipio"}), 404

if __name__ == '__main__':
    app.run(debug=True)
