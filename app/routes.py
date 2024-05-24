from flask import request, jsonify
import numpy as np
from app import app
import app.utils as utils
import app.geometry_engine as geometry_engine
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.before_request
def log_request_info():
    logger.info(f"Incoming Request: {request.method} {request.url}")
    logger.info(f"Headers: {request.headers}")
    logger.info(f"Body: {request.get_data()}")

@app.after_request
def log_response_info(response):
    logger.info(f"Outgoing Response: {response.status}")
    logger.info(f"Headers: {response.headers}")
    logger.info(f"Body: {response.get_data(as_text=True)}")
    return response

@app.route('/move_mesh', methods=['GET','POST'])
@utils.validate_parameters(('mesh', 'x', 'y', 'z', 'X', 'Y', 'Z'))
def move_mesh_endpoint(parameters):
    """
    Transforms a mesh based on specified translation parameters.
    The mesh is translated along the x, y, and z axes using provided values.

    Args:
    - parameters (dict): A dictionary containing:
        - 'mesh' (list of lists): Mesh data points.
        - 'x', 'y', 'z' (float, optional): Translation values along respective axes.

    Returns:
    - JSON: A JSON object with the transformed mesh data.
    """
    mesh = np.array(parameters['mesh'])
    result = geometry_engine.move_mesh(mesh, 
                       parameters.get('x',0.0), 
                       parameters.get('y',0.0), 
                       parameters.get('z',0.0))
    return jsonify({'mesh': result})

@app.route('/rotate_mesh', methods=['GET','POST'])
@utils.validate_parameters(('mesh', 'angle', 'axis'), rotation_endpoint=True)
def rotate_mesh_endpoint(parameters):
    """
    Rotates a mesh around a specified axis by a given angle.

    Args:
    parameters (dict): A dictionary containing:
        - 'mesh' (list of lists): Mesh data points.
        - 'angle' (float): Rotation angle in degrees.
        - 'axis' (str): Axis of rotation ('x', 'y', or 'z').

    Returns:
    - JSON: A JSON object with the rotated mesh data.
    """
    mesh = np.array(parameters['mesh'])
    angle = float(parameters.get('angle', 0))
    axis = parameters.get('axis', 'x')
    result = geometry_engine.rotate_mesh(mesh, 
                       angle,
                       axis)
    return jsonify({'mesh': result})

@app.route('/check_convex', methods=['GET','POST'])
@utils.validate_parameters(('mesh'))
def check_convex_endpoint(parameters):
    """
    Determines if the provided mesh points form a convex polygon.

    Args:
    parameters (dict): A dictionary containing:
        - 'mesh' (list of lists): Points of the mesh as coordinate pairs.

    Returns:
    - JSON: A JSON object indicating whether the polygon is convex.
    """
    mesh = np.array(parameters['mesh'])
    return jsonify({'Convex polygon': geometry_engine.check_convex(mesh)})

@app.route('/bounding_box', methods=['GET','POST'])
@utils.validate_parameters(('mesh', 'x', 'y', 'z', 'X', 'Y', 'Z'))
def bounding_box_endpoint(parameters):
    """
    Computes the bounding box of the given mesh.

    Args:
    parameters (dict): A dictionary containing:
        - 'mesh' (list of lists): Mesh data points.

    Returns:
    - JSON: A JSON object containing the 8 points of the oriented bounding box.
    """
    mesh = np.array(parameters['mesh'])
    return jsonify({'Bounding box': geometry_engine.compute_bounding_box(mesh)})
