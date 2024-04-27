from flask import request, jsonify
from functools import wraps

def validate_parameters(expected_parameters, rotation_endpoint=False):
    """
    Decorator to validate API parameters for Flask endpoint routes. Ensures 
    that the provided parameters match the ones that the route function requires,
    throwing errors where appropriate. 
    
    Additional angle and axis checks for the rotate_mesh function

    Args:
    - expected_parameters (tuple): A tuple listing valid keys for the given function
    - rotation_endpoint (bool): Flag to indicate if the rotation endpoint is being 
      called, necessitating additional validation.

    Returns:
    - function: A decorator that can be applied to Flask route functions.
    """
    def decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            parameters = get_parameters(request)
            if not parameters:
                return jsonify({'error': 'No parameters provided'}), 400
            if not check_provided_parameters(parameters, expected_parameters):
                return jsonify({'error': 'Invalid provided parameters'}), 400
            if not check_valid_mesh(parameters, request):
                return jsonify({'error': 'Mesh values must be provided as coordinate points'}), 400
            if rotation_endpoint and not axis_valid(parameters):
                return jsonify({'error': 'Specify a valid axis for rotation'}), 400
            if rotation_endpoint and not angle_valid(parameters):
                return jsonify({'error': 'Invalid angle provided. Provide a numeric value in degrees'}), 400
            # Pass the 'parameters' dictionary as a keyword argument to the decorated function
            return func(*args, **kwargs, parameters=parameters)
        return wrapped_function
    return decorator

def get_parameters(request):
    """
    Takes client requests (as a JSON Payload or Query parameters) and returns them in a Python dictionary.
    Returns False if a different type of HTTP request has been made

    Parameters:
    - request: The Flask request object containing the client's HTTP request.

    Returns:
    - dict: A dictionary containing the client's provided parameters
    """
    if request.method == 'POST':
        parameters = request.json
    elif request.method == 'GET':
        parameters = request.args.to_dict()
    else:
        return False
    return parameters

def check_valid_mesh(parameters, request):
    """
    Returns true if the provided mesh is formatted as a nested list of floats 
    representing coordinate points.

    Parameters:
    - parameters (dict): client's provided parameters

    Returns:
    - bool: True if mesh contains coordinate points
    """
    # Validate mesh has been provided 
    if 'mesh' not in parameters:
        return False
    # Confirm all coordinate points are numeric
    if request.method == 'POST':
        for point in parameters.get('mesh'):
            for coordinate in point:
                try:
                    float(coordinate)
                except ValueError:
                    return False
        return True
    # mesh points come in as string for GET requests         
    elif request.method == 'GET':
        mesh_points_as_string = parameters['mesh']
        try:
            # fix query param string from "a,b,c;d,e,f" to [[a,b,c],[d,e,f]]
            parameters.update(mesh=[list(map(float, point.split(','))) for point in mesh_points_as_string.split(';')])
        except ValueError:
            return False
    return True

def check_provided_parameters(parameters, expected_parameters):
    """
    Returns True if all of the provided parameters in a given API call match
    the expected parameters for a given computation 

    Parameters:
    - provided_parameters (dict): client's provided parameters
    - expected_parameters (list): allowable parameters for given function 

    Returns:
    - bool: True if all provided parameters are expected 
    """
    for key in parameters:
        if key not in expected_parameters:
            return False
    return True

def axis_valid(parameters):
    """
    Checks that a valid axis has been specified
    """
    axis = parameters.get('axis', 'none provided')
    return axis in ('x', 'X', 'y', 'Y', 'z', 'Z')

def angle_valid(parameters):
    """
    Returns true if parameters contains a valid angle in degrees
    """
    try:
        angle = float(parameters.get('angle', 'none provided'))
    except ValueError:
        return False
    return True