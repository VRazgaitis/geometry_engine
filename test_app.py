import pytest
import json
from flask_testing import TestCase
from app import app

class TestFlaskApi(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

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

if __name__ == "__main__":
    pytest.main()