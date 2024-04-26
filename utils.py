from flask import request, jsonify

def parse_request(request):
    """
    Takes client requests (as a JSON Payload or Query parameters) and returns them in a Python dictionary.
    This function also attempts to parse and convert mesh coordinates to float. If the conversion fails, it
    returns a 400 error with a JSON response indicating an invalid format.

    Parameters:
    - request: The Flask request object containing the client's HTTP request.

    Returns:
    - dict: A dictionary containing the parsed data, or
    - Flask.Response: A JSON response with status code 400 if an error occurs during type conversion.
    """
    if request.method == 'POST':
        keys = request.json
    elif request.method == 'GET':
        keys = request.args.to_dict()
    else:
        return False
    return keys

def get_keys(request):
    if request.method == 'POST':
        keys = request.json
    elif request.method == 'GET':
        keys = request.args.to_dict()
    else:
        return False
    return keys

def check_mesh_values(keys, request):
    if request.method == 'POST':
        for point in keys.get('mesh'):
            for coordinate in point:
                try:
                    float(coordinate)
                except ValueError:
                    return False
        return True
                
    elif request.method == 'GET':
        data = request.args.to_dict()
        mesh_points_as_string = request.args.get('mesh')
        try:
            # fix query param string from "a,b,c;d,e,f" to [[a,b,c],[d,e,f]]
            data.update(mesh=[list(map(float, point.split(','))) for point in mesh_points_as_string.split(';')])
        except ValueError:
            return False
    return True

def check_keys(provded_keys, expected_keys):
    if case:
        return False
    return True