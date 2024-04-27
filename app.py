from flask import Flask, request, jsonify
import utils
import geometry_engine
import numpy as np

app = Flask(__name__)

@app.route('/move_mesh', methods=['GET','POST'])
def move_mesh_endpoint():
    # VALIDATE API PARAMETERS
    parameters = utils.get_parameters(request)
    if not parameters:
        return jsonify({'error': 'No parameters provided'}), 400
    expected_parameters = ('mesh', 'x', 'y', 'z', 'X', 'Y', 'Z')
    if not utils.check_provided_parameters(parameters, expected_parameters):
        return jsonify({'error': 'Invalid provided parameters'}), 400    
    if not utils.check_valid_mesh(parameters, request):
        return jsonify({'error': 'Mesh values must be coordinate points'}), 400
    # RUN COMPUTATION
    mesh = np.array(parameters['mesh'])
    result = geometry_engine.move_mesh(mesh, 
                       parameters.get('x',0.0), 
                       parameters.get('y',0.0), 
                       parameters.get('z',0.0))
    return jsonify({'mesh': result})

@app.route('/rotate_mesh', methods=['GET','POST'])
def rotate_mesh_endpoint():
    # VALIDATE API PARAMETERS
    parameters = utils.get_parameters(request)
    if not parameters:
        return jsonify({'error': 'No parameters provided'}), 400
    expected_parameters = ('mesh', 'angle', 'axis')
    if not utils.check_provided_parameters(parameters, expected_parameters):
        return jsonify({'error': 'Invalid provided parameters'}), 400 
    # Error check rotation axis character
    axis = parameters.get('axis', 'x')
    if axis not in ('x', 'X', 'y', 'Y', 'z', 'Z'):
        return jsonify({'error': 'Invalid rotation axis. Axis must be one of x, X, y, Y, z, Z.'}), 400
    if not utils.check_valid_mesh(parameters, request):
        return jsonify({'error': 'Mesh values must be coordinate points'}), 400
    try:
        angle = float(parameters.get('angle', 0))
    except ValueError:
        return jsonify({'error': 'Invalid angle provided. Angle must be a numeric value.'}), 400
    # RUN COMPUTATION
    mesh = np.array(parameters['mesh'])
    result = geometry_engine.rotate_mesh(mesh, 
                       angle,
                       axis)
    return jsonify({'mesh': result})

@app.route('/check_convex', methods=['GET','POST'])
def check_convex_endpoint():
    # VALIDATE API PARAMETERS
    parameters = utils.get_parameters(request)
    if not utils.check_valid_mesh(parameters, request):
        return jsonify({'error': 'Mesh values must be coordinate points'}), 400
    # RUN COMPUTATION
    mesh = np.array(parameters['mesh'])
    return jsonify({'Convex polygon': geometry_engine.check_convex(mesh)})

@app.route('/bounding_box', methods=['GET','POST'])
def bounding_box_endpoint():
    # VALIDATE API PARAMETERS
    parameters = utils.get_parameters(request)
    if not utils.check_valid_mesh(parameters, request):
        return jsonify({'error': 'Mesh values must be coordinate points'}), 400
    # RUN COMPUTATION
    mesh = np.array(parameters['mesh'])
    return jsonify({'Bounding box': geometry_engine.compute_bounding_box(mesh)})

if __name__ == '__main__':
    app.run(debug=True)