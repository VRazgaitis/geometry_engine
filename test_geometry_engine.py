import numpy as np
import geometry_engine

## MOVE MESH TESTS
def test_move_mesh_type_check():
    """
    Confirm that type conversion is working 
    """
    mesh = np.array([[0, 0, 0],
                       [0, 0, 0],
                       [0, 0, 0]])
    
    expected_mesh = np.array([[1, 0, 3],
                       [1, 0, 3],
                       [1, 0, 3]])
    
    moved_mesh = geometry_engine.move_mesh(mesh, x='1', z=3)
    assert np.array_equal(moved_mesh, expected_mesh)

def test_move_mesh_decimals_check():
    """
    Decimal places check
    """
    mesh = np.array([[0, 0, 0],
                       [0, 0, 0],
                       [0, 0, 0]])
    
    expected_mesh = np.array([[1.0007, 0, 3],
                       [1.0007, 0, 3],
                       [1.0007, 0, 3]])
    
    moved_mesh = geometry_engine.move_mesh(mesh, x='1.0007', z=3)
    assert np.array_equal(moved_mesh, expected_mesh)

def test_move_mesh_decimals_check2():
    """
    Confirm that numpy is correctly assigning dtype=np.float64 when no mesh move values have been provided
    """
    mesh = np.array([[0.0002, 0, 0],
                       [0, 0, 0],
                       [0, 0, -0.0002]])
    
    expected_mesh = np.array([[0.0002, 0, 0],
                       [0, 0, 0],
                       [0, 0, -0.0002]])
    
    moved_mesh = geometry_engine.move_mesh(mesh)
    assert np.array_equal(moved_mesh, expected_mesh)

def test_move_mesh_no_transform():
    mesh = np.array([[0, 0, 0],
                       [0, 0, 0],
                       [0, 0, 0]])
    
    expected_mesh = np.array([[0, 0, 0],
                       [0, 0, 0],
                       [0, 0, 0]])
    
    moved_mesh = geometry_engine.move_mesh(mesh)
    assert np.array_equal(moved_mesh, expected_mesh)