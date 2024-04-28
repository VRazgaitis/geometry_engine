import pytest
import json
from flask_testing import TestCase
import sys
import os
import requests
# Add parent dir to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app

class TestFlaskApi(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app
        
    # MOVE MESH ENDPOINT
    def test_move_mesh_correct_inputs(self):
        """Test return status code with valid inputs, POST"""
        response = self.client.post('/move_mesh', data=json.dumps({
            'mesh': [[0, 0, 0], [1, 0, 0], [0, 1, 0]],
            'x': 1,
            'y': 2,
            'z':10
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_move_mesh_correct_inputs_get(self):
        """Test return status code with valid inputs using GET request"""
        url = 'http://127.0.0.1:5000/move_mesh'
        mesh_data = '2.0007,0,0;0,1,0;0,0,1'
        params = {
            "mesh": mesh_data,
            "x":1
        }
        response = requests.get(url, params=params)
        self.assertEqual(response.status_code, 200)  

    def test_move_mesh_bad_axis(self):
        """Test return status code with invalid input"""
        response = self.client.post('/move_mesh', data=json.dumps({
            'mesh': [[0, 0, 0], [1, 0, 0], [0, 1, 0]],
            'A': 1,
            'y': 2,
            'z':10
        }), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_move_mesh_bad_mesh(self):
        """Test return status code with invalid mesh"""
        response = self.client.post('/move_mesh', data=json.dumps({
            'mesh': 'maybe I can just decribe my mesh',
            'x': 1,
            'y': 2,
            'z':10
        }), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_move_mesh_no_mesh(self):
        """Test return status code and error message with no provided mesh"""
        response = self.client.post('/move_mesh', data=json.dumps({
            'x': 1,
            'y': 2,
            'z':10
        }), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['error'], 'Mesh values must be provided as coordinate points')

    def test_move_mesh_no_mesh_get(self):
        """Test return status code, error msg with no mesh using GET request"""
        url = 'http://127.0.0.1:5000/move_mesh'
        mesh_data = '2.0007,0,0;0,1,0;0,0,1'
        params = {
            "x":1
        }
        response = requests.get(url, params=params)
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.text)
        self.assertEqual(response_data['error'], 'Mesh values must be provided as coordinate points')  

    # ROTATE MESH ENDPOINT
    def test_rotate_mesh_correct_inputs(self):
        """Test return status code with valid inputs"""
        response = self.client.post('/rotate_mesh', data=json.dumps({
            'mesh': [[0, 0, 0], [1, 0, 0], [0, 1, 0]],
            'angle': 90,
            'axis': 'z'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_rotate_mesh_correct_inputs_get(self):
        """Test return status code with valid inputs using GET request"""
        url = 'http://127.0.0.1:5000/rotate_mesh'
        mesh_data = '2,0,0;0,1,0;0,0,1'
        params = {
            "mesh": mesh_data,
            "angle":20,
            "axis":'z'
        }
        response = requests.get(url, params=params)
        self.assertEqual(response.status_code, 200)  

    def test_rotate_mesh_bad_axis(self):
        """Test return status code with bad axis"""
        response = self.client.post('/rotate_mesh', data=json.dumps({
            'mesh': [[0, 0, 0], [1, 0, 0], [0, 1, 0]],
            'angle': 90,
            'axis': 'a'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_rotate_mesh_bad_axis_get(self):
        """Test return status code with valid inputs using GET request"""
        url = 'http://127.0.0.1:5000/rotate_mesh'
        mesh_data = '2,0,0;0,1,0;0,0,1'
        params = {
            "mesh": mesh_data,
            "angle":20,
            "axis":'a'
        }
        response = requests.get(url, params=params)
        self.assertEqual(response.status_code, 400)  

    def test_rotate_mesh_bad_angle(self):
        """Test return status code with bad angle"""
        response = self.client.post('/rotate_mesh', data=json.dumps({
            'mesh': [[0, 0, 0], [1, 0, 0], [0, 1, 0]],
            'angle': 'thirty degrees',
            'axis': 'Y'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_rotate_mesh_bad_mesh(self):
        """Test return status code with text string for mesh"""
        response = self.client.post('/rotate_mesh', data=json.dumps({
            'mesh': 'a string',
            'angle': 20,
            'axis': 'Y'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_rotate_mesh_no_mesh(self):
        """Test return status code with no mesh"""
        response = self.client.post('/rotate_mesh', data=json.dumps({
            'angle': 20,
            'axis': 'Y'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        # Assert that the error message is as expected
        response_data = json.loads(response.data)
        self.assertEqual(response_data['error'], 'Mesh values must be provided as coordinate points')

    # CONVEX POLYGON ENDPOINT
    def test_check_convex_correct_inputs(self):
        """Test return status code with valid inputs"""
        response = self.client.post('/check_convex', data=json.dumps({
            'mesh': [[0, 0, 0],      
                    [4, 0, 0],      
                    [4, 3, 0],      
                    [0, 3, 0]]
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_check_convex_bad_mesh(self):
        """Test return status code with valid inputs"""
        response = self.client.post('/check_convex', data=json.dumps({
            'mesh': [['a', 0, 0],      
                    [4, 0, 0],      
                    [4, 3, 0],      
                    [0, 3, 0]]
        }), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.text)
        self.assertEqual(response_data['error'], 'Mesh values must be provided as coordinate points')  

    def test_check_convex_correct_inputs_get(self):
        """Test return status code with valid inputs using GET request"""
        url = 'http://127.0.0.1:5000/check_convex'
        mesh_data = '0,0,0;04,0,0;4,3,0;0,3,0'
        params = {"mesh": mesh_data}
        response = requests.get(url, params=params)
        self.assertEqual(response.status_code, 200)  

    def test_check_convex_bad_mesh_get(self):
        """Test return status code with valid inputs using GET request"""
        url = 'http://127.0.0.1:5000/check_convex'
        mesh_data = '0,0,a;04,0,0;4,3,0;0,3,0'
        params = {"mesh": mesh_data}
        response = requests.get(url, params=params)
        self.assertEqual(response.status_code, 400)  
        response_data = json.loads(response.text)
        self.assertEqual(response_data['error'], 'Mesh values must be provided as coordinate points')

    # BOUNDING BOX ENDPOINT
    def test_bounding_box_correct_inputs(self):
        """Test return status code with valid inputs"""
        response = self.client.post('/bounding_box', 
        data=json.dumps({
            'mesh': 
            [[4.1949637777057571, -6.9916062961762613, 16.047420986034020], 
             [6.8206194998754439, -4.0247156045330703, 16.598321750671875], 
             [-0.48443183668373879, 1.7688355092261352, 20.213704228708519], 
             [-3.1100875588534249, -1.1980551824170558, 19.662803464070663], 
             [3.4299717028501773, 2.0579830217101063, -6.6613381477509392e-16], 
             [-3.8750796337090048, 7.8515341354693104, 3.6153824780366430], 
             [0.80431598068049104, -0.90890766993308547, -0.55090076463785609],
             [-6.5007353558786898, 4.8846434438261213, 3.0644817133987878]]
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
    
    def test_bounding_box_bad_mesh(self):
        """Test return status code with valid inputs"""
        response = self.client.post('/bounding_box', data=json.dumps({
            'mesh': [['a', 0, 0],      
                    [4, 0, 0],      
                    [4, 3, 0],      
                    [0, 3, 0]]
        }), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.text)
        self.assertEqual(response_data['error'], 'Mesh values must be provided as coordinate points')  

    def test_bounding_box_correct_inputs_get(self):
        """Test return status code with valid inputs using GET request"""
        url = 'http://127.0.0.1:5000/bounding_box'
        mesh_data = '0,0,0;04,0,0;4,3,0;0,3,0'
        params = {"mesh": mesh_data}
        response = requests.get(url, params=params)
        self.assertEqual(response.status_code, 200)  

    def test_bounding_box_bad_mesh_get(self):
        """Test return status code with valid inputs using GET request"""
        url = 'http://127.0.0.1:5000/bounding_box'
        mesh_data = '0,0,a;04,0,0;4,3,0;0,3,0'
        params = {"mesh": mesh_data}
        response = requests.get(url, params=params)
        self.assertEqual(response.status_code, 400)  
        response_data = json.loads(response.text)
        self.assertEqual(response_data['error'], 'Mesh values must be provided as coordinate points')
        
if __name__ == "__main__":
    pytest.main()