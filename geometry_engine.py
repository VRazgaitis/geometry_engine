import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pprint

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

def compute_bounding_box(mesh):
    points = mesh.T  # transpose for means
    means = np.mean(points, axis=1)
    covariance_matrix = np.cov(points)  # diagonals represent clustering about each mean
    eigenvalues, eigenvectors = np.linalg.eig(covariance_matrix)
    # center the dataset about the cartesian origin
    centered_points = points - means[:,np.newaxis]  #nnp.newaxis for subtraction compatability
    # rotate points to align with the eigenvector basis
    rotated_coordinates = np.matmul(eigenvectors.T, centered_points)
    # compute a bounding box
    xmin, xmax, ymin, ymax, zmin, zmax = (
        np.min(rotated_coordinates[0, :]), 
        np.max(rotated_coordinates[0, :]),
        np.min(rotated_coordinates[1, :]),
        np.max(rotated_coordinates[1, :]),
        np.min(rotated_coordinates[2, :]),
        np.max(rotated_coordinates[2, :]))
    rectangle_coordinates = lambda x1, y1, z1, x2, y2, z2: np.array([
        [x1, x1, x2, x2, x1, x1, x2, x2],
        [y1, y2, y2, y1, y1, y2, y2, y1],
        [z1, z1, z1, z1, z2, z2, z2, z2]])
    
    # TO DELETE: POINTS UN-ROTATED
    #----------------------------------------
    # undo the rotations on coordinate points
    realigned_coords = np.matmul(eigenvectors, rotated_coordinates)
    # undo the movement of coordinate points to be centered on the origin
    realigned_coords += means[:, np.newaxis]
    
    # un-align the bounding box from the rotated points
    bounding_box_coords = np.matmul(eigenvectors, 
        rectangle_coordinates(xmin, ymin, zmin, xmax, ymax, zmax))
    # move box from being centered about the cartesian origin
    bounding_box_coords += means[:, np.newaxis] 
    return bounding_box_coords.T.tolist()

assert_against = np.array([
    [2.9332705452110419, 14.005997384948117, 6.1899642452550392], 
    [1.2796522506551051, 22.683917742744043, 12.887540879848547], 
    [-3.9500367363111302, 20.248855069408705, 14.751404668622987], 
    [-2.2964184417551925, 11.570934711612779, 8.053828034029479], 
    [9.2360317618136420, 0.22996972574907204, 25.595435689360876], 
    [7.5824134672577008, 8.9078900835449986, 32.293012323954386],
    [12.812102454223936, 11.342952756880337, 30.429148535179941],
    [14.465720748779876, 2.6650323990844091, 23.731571900586438]
    ])

# missing value:
# [14.465720748779876, 2.6650323990844091, 23.731571900586438]
mesh = np.array([
    [2.9332705452110419, 14.005997384948117, 6.1899642452550392], 
    [1.2796522506551051, 22.683917742744043, 12.887540879848547], 
    [-3.9500367363111302, 20.248855069408705, 14.751404668622987], 
    [-2.2964184417551925, 11.570934711612779, 8.053828034029479], 
    [9.2360317618136420, 0.22996972574907204, 25.595435689360876], 
    [7.5824134672577008, 8.9078900835449986, 32.293012323954386],
    [12.812102454223936, 11.342952756880337, 30.429148535179941],
    [-2.2121896654934430, 19.410762544741115, 14.427265355518752], 
    [0.93512546588596646, 20.876224375596824, 13.305560657617981], 
    [-3.9500367363111302, 20.248855069408705, 14.751404668622987], 
    [-2.2121896654934430, 19.410762544741115, 14.427265355518752],
    [8.2569381821712469, 9.1154644721638078, 30.351490472953653], 
    [11.404253313550655, 10.580926303019524, 29.229785775052882], 
    [1.2796522506551051, 22.683917742744043, 12.887540879848547], 
    [7.5824134672577008, 8.9078900835449986, 32.293012323954386], 
    [8.2569381821712469, 9.1154644721638078, 30.351490472953653],
    [14.465720748779876, 2.6650323990844091, 23.731571900586438]
    ])

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
  
pprint.pprint(compute_bounding_box(mesh))

