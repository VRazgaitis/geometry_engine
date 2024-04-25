# Geometry Engine
A Python service that uses Flask to act as a geometry engine, capable of performing 3D geometric opperations

## Operations
-**bounding_box:** Given an array of points, calculates the smallet bounding box that contains all of the 3D points. Returns a JSON of 3D coordinate points, [[a,b,c],[d,e,f],[...]]    
-**rotate_mesh:** Given a 3D Mesh as an Input, rotates the mesh by X degrees along the specified axis. Returns a JSON of rotated 3D coordinate points  
-**move_mesh:** Given a 3D mesh as an input, moves the mesh by a, b and c units along X, Y and Z axis respectively. Returns a JSON of moved 3D coordinate points  
-**check_convex:** Given a polygon in a 3D space represented by 3D Points, check whether the polygon is convex.

## Instructions (Linux/macOS only):
-run ./setup_and_run.sh  
-perform geometric operations. See **example.py** or **example.sh** for example usage