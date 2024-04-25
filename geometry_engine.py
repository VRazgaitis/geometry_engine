import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def move_mesh(mesh, x=0.0, y=0.0, z=0.0):
    """
    Moves points of a 3d mesh by (a,b,c) units along (x,y,z) axes
    """
    moved_mesh = mesh.copy()
    moved_mesh = mesh.astype(np.float64)
    # moved_mesh += np.array([float(x), float(y), float(z)], dtype=np.float64)
    moved_mesh += np.array([float(x), float(y), float(z)])
    return moved_mesh.tolist()