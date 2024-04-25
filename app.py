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

@app.route('/rotate_mesh', methods=['GET','POST'])
def rotate_mesh_endpoint():
    data = parse_request(request)
    # Error check angle
    try:
        angle = float(data.get('angle', 0))
    except ValueError:
        return jsonify({'error': 'Invalid angle provided. Angle must be a numeric value.'}), 400
    # Error check rotation axis character
    axis = data.get('axis', 'x')
    if axis not in ('x', 'X', 'y', 'Y', 'z', 'Z'):
        return jsonify({'error': 'Invalid rotation axis. Axis must be one of x, X, y, Y, z, Z.'}), 400
    # TODO: error check mesh 
    mesh = np.array(data['mesh'])
    result = geometry_engine.rotate_mesh(mesh, 
                       angle,
                       axis)
    return jsonify({'mesh': result})

if __name__ == '__main__':
    app.run(debug=True)
