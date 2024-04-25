from flask import Flask, request, jsonify
import geometry_engine
import numpy as np

app = Flask(__name__)

def parse_request(request):
    """
    Takes client requests (JSON Payload or Query parameters) and returns a Python dictionary 
    """
    if request.method == 'POST':
        data = request.json
    elif request.method == 'GET':
        data = request.args.to_dict()
        mesh_points_as_string = request.args.get('mesh')
        # fix query param string from "a,b,c;d,e,f" to [[a,b,c],[d,e,f]]
        data.update(mesh=[list(map(float, point.split(','))) for point in mesh_points_as_string.split(';')])
    return data

@app.route('/move_mesh', methods=['GET','POST'])
def move_mesh_endpoint():
    data = parse_request(request)
    result = geometry_engine.move_mesh(np.array(data['mesh']), 
                       data.get('x',0.0), 
                       data.get('y',0.0), 
                       data.get('z',0.0))
    return jsonify({'mesh': result})