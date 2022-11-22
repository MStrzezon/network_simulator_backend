from flask import Flask, jsonify
from flask_restx import Api
from flask_swagger_ui import get_swaggerui_blueprint

from flaskr.datahandling.simulation_rest import simulation
from flaskr.datahandling.devices_rest import devices

app = Flask(__name__)
api = Api(app)

app.register_blueprint(devices, url_prefix='/api/devices')
app.register_blueprint(simulation, url_prefix='/api/simulation')

SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.yaml'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Network simulator"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)


if __name__ == '__main__':
    app.run(debug=True)
