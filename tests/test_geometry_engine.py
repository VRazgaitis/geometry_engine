import numpy as np
import sys
import os
# Add the parent dir to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import geometry_engine

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

## ROTATE MESH TESTS
def test_rotate_mesh():
    mesh = np.array([[1, 0, 0],
                   [0, 1, 0],
                   [0, 0, 1]])
    
    expected_mesh = np.array([[1, 0, 0],
                       [0, 0.98480775, -0.17364818],
                       [0, 0.17364818, 0.98480775]])
    
    rotated_mesh = geometry_engine.rotate_mesh(mesh, angle=-10, axis='x')
    assert np.allclose(rotated_mesh, expected_mesh, atol=1e-8)

## CHECK CONVEX POLYGON TESTS
def test_check_convex_square():
    """Simple 2D sqaure"""
    square = np.array([ [0, 0, 0],      
                    [4, 0, 0],      
                    [4, 3, 0],      
                    [0, 3, 0]])
    assert geometry_engine.check_convex(square) == True

def test_check_convex_square_reverse():
    """Conmfirm that checks were independent of node traversal direction (clockwise, cc)"""
    square = np.array([ [0, 0, 0],      
                    [4, 0, 0],      
                    [4, 3, 0],      
                    [0, 3, 0]])
    clockwise_square = square[::-1]
    assert geometry_engine.check_convex(clockwise_square) == True

def test_check_convex_pentag():
    """Third node angle greater than 180"""
    non_convex_penta = np.array([ 
                                 [0, 0, 0],      
                                 [0, 10, 0],     
                                 [5, 5, 0],      
                                 [10, 10, 0],     
                                 [10, 0, 0]])  
    assert geometry_engine.check_convex(non_convex_penta) == False

def test_check_convex_3d_concave():
    """3D convex shape"""
    concave_3d = np.array([
                            [0, 0, 1],
                            [2, 0, 2],
                            [2, 1, 1],
                            [1, 1, 3],
                            [1, 2, 1],
                            [2, 2, 3],
                            [2, 3, 1],
                            [0, 3, 3],
                            [0, 0, 1]])                       
    assert geometry_engine.check_convex(concave_3d) == False

# BOUNDING BOX TESTS
def test_bounding_box():
    """
    bounding box drawn in Rhino and rotated
    """
    test_mesh = np.array([
             [4.1949637777057571, -6.9916062961762613, 16.047420986034020], 
             [6.8206194998754439, -4.0247156045330703, 16.598321750671875], 
             [-0.48443183668373879, 1.7688355092261352, 20.213704228708519], 
             [-3.1100875588534249, -1.1980551824170558, 19.662803464070663], 
             [3.4299717028501773, 2.0579830217101063, -6.6613381477509392e-16], 
             [-3.8750796337090048, 7.8515341354693104, 3.6153824780366430], 
             [0.80431598068049104, -0.90890766993308547, -0.55090076463785609],
             [-6.5007353558786898, 4.8846434438261213, 3.0644817133987878]])
    
    expected_bounding_box = np.array([
             [4.1949637777057571, -6.9916062961762613, 16.047420986034020], 
             [6.8206194998754439, -4.0247156045330703, 16.598321750671875], 
             [-0.48443183668373879, 1.7688355092261352, 20.213704228708519], 
             [-3.1100875588534249, -1.1980551824170558, 19.662803464070663], 
             [3.4299717028501773, 2.0579830217101063, -6.6613381477509392e-16], 
             [-3.8750796337090048, 7.8515341354693104, 3.6153824780366430], 
             [0.80431598068049104, -0.90890766993308547, -0.55090076463785609],
             [-6.5007353558786898, 4.8846434438261213, 3.0644817133987878]])
    bounding_box = np.array(geometry_engine.compute_bounding_box(test_mesh))
    for point in bounding_box:
        match = any(np.allclose(point, exp_point, atol=1e-8) for exp_point in expected_bounding_box)
        assert match, f"Point {point} not found in expected list with tolerance."