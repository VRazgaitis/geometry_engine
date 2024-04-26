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

def compute_bounding_box(mesh, show_plot=False):
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
    
    # FOR PLOTTING:
    # undo the rotations, movement on coordinate points
    realigned_coords = np.matmul(eigenvectors, rotated_coordinates)
    realigned_coords += means[:, np.newaxis]
    
    # un-align the bounding box from the rotated points
    bounding_box_coords = np.matmul(eigenvectors, 
        rectangle_coordinates(xmin, ymin, zmin, xmax, ymax, zmax))
    # move box from being centered about the cartesian origin
    bounding_box_coords += means[:, np.newaxis] 
    if show_plot:
        plot_bounding_box(realigned_coords, bounding_box_coords)
    return bounding_box_coords.T.tolist()

def plot_bounding_box(realigned_coords, bounding_box_coords):
    """
    Plots a minimum volume bounding box superimposed on top of mesh points
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(realigned_coords[0,:], realigned_coords[1,:], realigned_coords[2,:], label="rotation and translation undone")
    ax.legend()

    # z1 plane boundary
    ax.plot(bounding_box_coords[0, 0:2], bounding_box_coords[1, 0:2], bounding_box_coords[2, 0:2], color='b')
    ax.plot(bounding_box_coords[0, 1:3], bounding_box_coords[1, 1:3], bounding_box_coords[2, 1:3], color='b')
    ax.plot(bounding_box_coords[0, 2:4], bounding_box_coords[1, 2:4], bounding_box_coords[2, 2:4], color='b')
    ax.plot(bounding_box_coords[0, [3,0]], bounding_box_coords[1, [3,0]], bounding_box_coords[2, [3,0]], color='b')

    # z2 plane boundary
    ax.plot(bounding_box_coords[0, 4:6], bounding_box_coords[1, 4:6], bounding_box_coords[2, 4:6], color='b')
    ax.plot(bounding_box_coords[0, 5:7], bounding_box_coords[1, 5:7], bounding_box_coords[2, 5:7], color='b')
    ax.plot(bounding_box_coords[0, 6:], bounding_box_coords[1, 6:], bounding_box_coords[2, 6:], color='b')
    ax.plot(bounding_box_coords[0, [7, 4]], bounding_box_coords[1, [7, 4]], bounding_box_coords[2, [7, 4]], color='b')

    # z1 and z2 connecting boundaries
    ax.plot(bounding_box_coords[0, [0, 4]], bounding_box_coords[1, [0, 4]], bounding_box_coords[2, [0, 4]], color='b')
    ax.plot(bounding_box_coords[0, [1, 5]], bounding_box_coords[1, [1, 5]], bounding_box_coords[2, [1, 5]], color='b')
    ax.plot(bounding_box_coords[0, [2, 6]], bounding_box_coords[1, [2, 6]], bounding_box_coords[2, [2, 6]], color='b')
    ax.plot(bounding_box_coords[0, [3, 7]], bounding_box_coords[1, [3, 7]], bounding_box_coords[2, [3, 7]], color='b')
    plt.show()

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

bb_points = np.array([
             [4.1949637777057571, -6.9916062961762613, 16.047420986034020], 
             [6.8206194998754439, -4.0247156045330703, 16.598321750671875], 
             [-0.48443183668373879, 1.7688355092261352, 20.213704228708519], 
             [-3.1100875588534249, -1.1980551824170558, 19.662803464070663], 
             [3.4299717028501773, 2.0579830217101063, -6.6613381477509392e-16], 
             [-3.8750796337090048, 7.8515341354693104, 3.6153824780366430], 
             [0.80431598068049104, -0.90890766993308547, -0.55090076463785609],
             [-6.5007353558786898, 4.8846434438261213, 3.0644817133987878]])

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
  
# pprint.pprint(compute_bounding_box(bb_points, show_plot=True))
