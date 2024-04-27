import requests
import json

# Define the URL of the Flask endpoint
url = 'http://127.0.0.1:5000/move_mesh'

mesh_data = '2.0007,0,0;0,1,0;0,0,1'

# Define the query parameters
params = {
    "mesh": mesh_data,
    "x":1
}

# Send the GET request with the specified parameters
response = requests.get(url, params=params)

# Print the response text
# print(response.request.url)
print(response.text)
