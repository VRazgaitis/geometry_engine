import rhinoscriptsyntax as rs
decimal_places = 2
def print_polyline_points():
    """
    Returns a list points of the selected polyline
    """
    # Get the selected objects in Rhino
    selected_objects = rs.SelectedObjects()
    
    if not selected_objects:
        print("No objects selected. Please select a polyline and run the script again.")
        return
    
    for obj_id in selected_objects:
        if rs.IsPolyline(obj_id):
            # Get the vertices of the polyline
            points = rs.PolylineVertices(obj_id)
            # Print each point's coordinates
            points_list = [[point.X, point.Y, point.Z] for point in points]
        else:
            print("One or more selected objects are not polylines.")
    print(points_list)
print_polyline_points()