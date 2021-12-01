from flask import Flask, render_template, request, jsonify
import json, logging, os, atexit
from model import TrafficBlock

app = Flask(__name__, static_url_path='')
model = TrafficBlock()

def carToJSON(agentInfo):
    infoDICT = []

    for i in range(0,4):
        pos = {
            "x": agentInfo[i][0],
            "y": agentInfo[i][1],
            "z": agentInfo[i][2],
            "r": agentInfo[i][3]
        }
        infoDICT.append(pos)
    return json.dumps(infoDICT)

def trafficLightToJSON(agentInfo):
    infoDICT = []

    for i in range(0, 4):
        trafficLight = {
            "status": agentInfo[i][0]
        }
        infoDICT.append(trafficLight)
    return json.dumps(infoDICT)




# On IBM Cloud Cloud Foundry, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000
port = int(os.getenv('PORT', 8585))

@app.route('/')
def root():
    return jsonify([{"message":"Hello World from IBM Cloud!"}])

@app.route('/reto/cars', methods=['GET', 'POST'])
def retoC():
    info = model.step()
    return carToJSON(info["Cars"])

@app.route('/reto/trafficLights', methods=['GET', 'POST'])
def retoTL():
    info = model.step()
    return trafficLightToJSON(info["TrafficLights"])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)