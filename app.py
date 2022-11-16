from flask import Flask, jsonify
from flask_restx import Api

from flaskr.datahandling.simulation_rest import simulation
from flaskr.datahandling.devices_rest import devices

app = Flask(__name__)
api = Api(app)

app.register_blueprint(devices, url_prefix='/api/devices')
app.register_blueprint(simulation, url_prefix='/api/simulation')


if __name__ == '__main__':
    app.run(debug=True)
