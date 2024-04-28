import numpy as np
import matplotlib.pyplot as plt

def move_mesh(mesh, x=0.0, y=0.0, z=0.0):
    """
    Moves points of a 3d mesh by (a,b,c) units along (x,y,z) axes.

    Args:
    - mesh (numpy.ndarray): A 3D numpy array representing the mesh to be moved.
                            Each row should represent a point in 3D space as [x, y, z].
    - x (float): amount to move x values.
    - y (float): amount to move y values.
    - z (float): amount to move z values.

    Returns:
    - list: A nested list, where each list entry is an [x, y, z] coordinate
            point that has been moved by the specified amount.
    """
    moved_mesh = mesh.copy()
    moved_mesh = mesh.astype(np.float64)
    moved_mesh += np.array([float(x), float(y), float(z)])
    return moved_mesh.tolist()

def rotate_mesh(mesh, angle, axis):
    """
    Rotates a 3D mesh by a given angle around a specified axis.

    The rotation is performed in a right-handed coordinate system, where positive angles
    correspond to counter-clockwise rotation when looking along the axis towards the origin.

    To rotate a point about a specific axis, you take the dot product of the point's 
    vector representation with the corresponding rotation matrix.

    Args:
    - mesh (numpy.ndarray): A 3D numpy array representing the mesh to be rotated.
                            Each row should represent a point in 3D space as [x, y, z].
    - angle (float): The rotation angle in degrees. Positive values represent
                     counter-clockwise rotation and negative values represent
                     clockwise rotation.
    - axis (str): The axis around which to rotate the mesh.

    Returns:
    - list: A nested list, where each list entry is an [x, y, z] coordinate
            point that has been rotated by the specified angle around the 
            specified axis.
    """
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
    
    if axis in ('x','X'):
        rotation_matrix = r_x
    elif axis in ('y','Y'):
        rotation_matrix = r_y
    elif axis in ('z','Z'):
        rotation_matrix = r_z

    return rotation_matrix.dot(mesh.T).T.tolist()

def check_convex(mesh):
    """
    Determines if a polygon, defined by a sequence of 3D points is convex (all internal angles < 180 deg).

    The function checks convexity by evaluating the cross products of consecutive edge vectors of the polygon.
    A polygon is considered convex if all the cross products point in the same general direction (i.e., the
    dot product of consecutive cross products is non-negative).

    Args:
    - mesh (numpy.ndarray): A 3D array where each row represents a 3D point [x, y, z].

    Returns:
    - bool: True if the polygon is convex, False otherwise.

    Notes:
    - The function assumes that the polygon is closed, meaning the vertices are listed in either clockwise
      or counterclockwise order, and the last vertex connects back to the first.
    - The function returns False for polygons with less than three vertices since at least three vertices
      are needed to form a polygon.
    - The function is robust against collinear points (where cross product norms may be zero).
    """
    n = len(mesh)
    if n < 3:
        return False
    # Calculate consecutive edge vectors and cross products 
    normals = []
    for i in range(n):
        vector_a = mesh[(i + 1) % n] - mesh[i]
        vector_b = mesh[(i + 2) % n] - mesh[(i + 1) % n]
        normal_vector = np.cross(vector_a, vector_b)
        if np.linalg.norm(normal_vector) == 0:
            continue #skip parallel edges
        normals.append(normal_vector)
    
    if not normals:
        return False
    
    # all positive dot products signify that the normal vectors are all in the same direction
    reference_normal = normals[0]
    for normal in normals[1:]:
        if np.dot(reference_normal, normal) <= 0:
            return False  # at least one edge pair has a normal pointing opposite to the reference normal
    return True

def compute_bounding_box(mesh, show_plot=False):
    """
    Calculates the smallest axis-aligned bounding box that encloses all the provided 3D points.

    This function computes the bounding box by first determining the covariance matrix of the points to identify
    the principal directions of the point set. It then rotates the points to align with these principal directions,
    computes the minimum and maximum coordinates along each principal axis, and constructs the bounding box.
    Optionally, it can also plot the original points and their bounding box.

    Args:
    - mesh (numpy.ndarray): A 3D array where each row represents a 3D point [x, y, z].
    - show_plot (bool): If True, the function will plot the points and their bounding box. Default is False.

    Returns:
    - list: Coordinates of the 8 vertices of the oriented bounding box, in the original coordinate system. 
            Each vertex is represented as a list [x, y, z].
    """
    points = mesh.T  # transpose for mean computation
    means = np.mean(points, axis=1)
    covariance_matrix = np.cov(points)  # diagonals represent clustering about each mean
    eigenvalues, eigenvectors = np.linalg.eig(covariance_matrix)
    # center the dataset about the cartesian origin
    centered_points = points - means[:,np.newaxis]  # nnp.newaxis for subtraction compatability
    # rotate points to align with the eigenvector basis (Eig.T=inv(Eig))
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
    # un-align the bounding box from the rotated points
    bounding_box_coords = np.matmul(eigenvectors, 
        rectangle_coordinates(xmin, ymin, zmin, xmax, ymax, zmax))
    # un-center box centering around the cartesian origin
    bounding_box_coords += means[:, np.newaxis] 
    if show_plot:
        plot_bounding_box(points, bounding_box_coords)
    return bounding_box_coords.T.tolist()

def plot_bounding_box(points, bounding_box_coords):
    """
    Plots to the console a minimum volume bounding box,
    superimposed on top of the provided mesh points.
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(points[0,:], points[1,:], points[2,:], label="Points")
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