from flask import Flask, request, jsonify
import utils
import geometry_engine
import numpy as np

app = Flask(__name__)

@app.route('/move_mesh', methods=['GET','POST'])
def move_mesh_endpoint():
    data = utils.parse_request(request)
    result = geometry_engine.move_mesh(np.array(data['mesh']), 
                       data.get('x',0.0), 
                       data.get('y',0.0), 
                       data.get('z',0.0))
    return jsonify({'mesh': result})

@app.route('/rotate_mesh', methods=['GET','POST'])
def rotate_mesh_endpoint():
    data = utils.parse_request(request)
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

@app.route('/check_convex', methods=['GET','POST'])
def check_convex_endpoint():
    data = utils.parse_request(request)
    mesh = np.array(data['mesh'])
    return jsonify({'Convex polygon': geometry_engine.check_convex(mesh)})

if __name__ == '__main__':
    app.run(debug=True)
