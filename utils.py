from flask import request, jsonify

def get_parameters(request):
    """
    Takes client requests (as a JSON Payload or Query parameters) and returns them in a Python dictionary.
    Returns False if an different type of HTTP request has been made

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

def check_provided_parameters(provided_parameters, expected_parameters):
    """
    Returns True if all of the provided parameters in an API call are expected
    for the given computation 

    Parameters:
    - provided_parameters (dict): client's provided parameters
    - expected_parameters (list): allowable parameters for given function 

    Returns:
    - bool: True if all provided parameters are expected 
    """
    for key in provided_parameters:
        if key not in expected_parameters:
            return False
    return True