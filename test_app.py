import pytest
import json
from flask_testing import TestCase
from app import app

class TestFlaskApi(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app
        
    # MOVE MESH ENDPOINT
    def test_move_mesh_correct_inputs(self):
        """Test return status code with valid inputs"""
        response = self.client.post('/move_mesh', data=json.dumps({
            'mesh': [[0, 0, 0], [1, 0, 0], [0, 1, 0]],
            'x': 1,
            'y': 2,
            'z':10
        }), content_type='application/json')
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
        """Test return status code with no provided mesh"""
        response = self.client.post('/move_mesh', data=json.dumps({
            'x': 1,
            'y': 2,
            'z':10
        }), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    # ROTATE MESH ENDPOINT
    def test_rotate_mesh_correct_inputs(self):
        """Test return status code with valid inputs"""
        response = self.client.post('/rotate_mesh', data=json.dumps({
            'mesh': [[0, 0, 0], [1, 0, 0], [0, 1, 0]],
            'angle': 90,
            'axis': 'z'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_rotate_mesh_bad_axis(self):
        """Test return status code with bad axis"""
        response = self.client.post('/rotate_mesh', data=json.dumps({
            'mesh': [[0, 0, 0], [1, 0, 0], [0, 1, 0]],
            'angle': 90,
            'axis': 'a'
        }), content_type='application/json')
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

if __name__ == "__main__":
    pytest.main()