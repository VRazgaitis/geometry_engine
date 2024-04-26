import rhinoscriptsyntax as rs
import numpy as np  

def get_point_coordinates_array():
    # Ask the user to select point objects
    point_ids = rs.GetObjects("Select points", rs.filter.point)
    
    if point_ids is None:
        print("No points selected.")
        return None

    # List to collect coordinates
    coordinates_list = []

    # Retrieve coordinates of each selected point
    for point_id in point_ids:
        point = rs.PointCoordinates(point_id)
        coordinates_list.append([point.X, point.Y, point.Z])
    coordinates_array = np.array(coordinates_list)

    # Return the array of coordinates
    print(coordinates_list)


