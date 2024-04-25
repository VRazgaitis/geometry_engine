from flask import request

def parse_request(request):
    """
    Takes client requests (as a JSON Payload or Query parameters) and returns them in a Python dictionary 
    """
    if request.method == 'POST':
        data = request.json
    elif request.method == 'GET':
        data = request.args.to_dict()
        mesh_points_as_string = request.args.get('mesh')
        # fix query param string from "a,b,c;d,e,f" to [[a,b,c],[d,e,f]]
        data.update(mesh=[list(map(float, point.split(','))) for point in mesh_points_as_string.split(';')])
    return data