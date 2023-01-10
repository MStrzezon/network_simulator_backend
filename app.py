from flask import Flask
from flask_cors import CORS
from flask_restx import Api
from flask_swagger_ui import get_swaggerui_blueprint

from flaskr.datahandling.simulation_params_rest import simulation_params_blueprint
from flaskr.datahandling.devices_rest import devices_blueprint
from flaskr.framesextraction.simulation_rest import simulation_blueprint

app = Flask(__name__)
api = Api(app)
CORS(app)

app.register_blueprint(devices_blueprint, url_prefix='/api/devices')
app.register_blueprint(simulation_params_blueprint, url_prefix='/api/simulation/params')
app.register_blueprint(simulation_blueprint, url_prefix='/api/simulation')

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
