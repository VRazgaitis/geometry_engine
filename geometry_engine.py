import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def move_mesh(mesh, x=0.0, y=0.0, z=0.0):
    """
    Moves points of a 3d mesh by (a,b,c) units along (x,y,z) axes
    """
    moved_mesh = mesh.copy()
    moved_mesh = mesh.astype(np.float64)
    moved_mesh += np.array([float(x), float(y), float(z)])
    return moved_mesh.tolist()

def rotate_mesh(mesh, angle, axis):
    """
    Rotate a 3D mesh by a given angle around a specified axis.

    The rotation is performed in a right-handed coordinate system, where positive angles
    correspond to counter-clockwise rotation when looking along the axis towards the origin.

    Parameters:
        mesh (numpy.ndarray): A 3D numpy array representing the mesh to be rotated.
                              Each row should represent a point in 3D space as [x, y, z].
        angle (float): The rotation angle in degrees. Positive values represent
                       counter-clockwise rotation and negative values represent
                       clockwise rotation.
        axis (str): The axis around which to rotate the mesh.

    Returns:
        list: A new mesh array, where each point is a list [x, y, z] of has been rotated by the specified
                       angle around the specified axis.

    Raises:
        ValueError: If the specified axis is not 'X', 'Y', or 'Z'.
    """
    # Check if the angle is a number (either int or float)
    if not isinstance(angle, (int, float)):
        raise TypeError("angle must be a number (int or float)")

    # Check if the axis is one of the accepted values
    if axis not in ('x', 'X', 'y', 'Y', 'z', 'Z'):
        raise ValueError("axis must be one of 'x', 'X', 'y', 'Y', 'z', 'Z'")
    
    angle = np.radians(float(angle))
    # Define rotation matrices
    r_x = np.array([[1, 0, 0],
                   [0, np.cos(angle), -np.sin(angle)],
                   [0, np.sin(angle), np.cos(angle)]])
    
    r_y = np.array([[np.cos(angle), 0, np.sin(angle)],
                   [0, 1, 0],
                   [-np.sin(angle), 0, np.cos(angle)]])
    
    r_z = np.array([[np.cos(angle), -np.sin(angle), 0],
                   [np.sin(angle), np.cos(angle), 0],
                   [0, 0, 1]])
    
    # Select appropriate rotation matrix
    if axis in ('x','X'):
        rotation_matrix = r_x
    elif axis in ('y','Y'):
        rotation_matrix = r_y
    elif axis in ('z','Z'):
        rotation_matrix = r_z

    # Perform rotation
    rotated_mesh = mesh.copy()
    return rotation_matrix.dot(rotated_mesh.T).T.tolist()

def check_convex(mesh):
    """
    Given a polygon in a 3D space represented by 3D Points, returns True if the polygon is convex.
    A polygon is convex if all internal angles are at most 180 degrees.
    """
    n = len(mesh)
    if n < 3:
        return False
    # Calculate consecutive edge vectors and cross products 
    normals = []
    for i in range(n):
        # get a vector from edge i to i+1
        edge_1 = mesh[(i + 1) % n] - mesh[i]
        # get a vector from edge i+1 to i+2
        edge_2 = mesh[(i + 2) % n] - mesh[(i + 1) % n]
        # get the cross product of edge_1 x edge_2
        normal = np.cross(edge_1, edge_2)
        if np.linalg.norm(normal) == 0:
            continue #skip parallel edges
        normals.append(normal)
    
    # check the direction of the normals
    if not normals:
        return False
    
    # all positive dot products signify that the normal vectors are all in the same direction
    reference_normal = normals[0]
    for normal in normals[1:]:
        if np.dot(reference_normal, normal) <= 0:
            # at least one edge whose normal points opposite to the reference normal
            return False
    return True
