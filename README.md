# Geometry Engine
A Python service that uses Flask to act as a geometry engine, capable of performing 3D geometric opperations on a provided set of coordinate points.

## Geometric Operations
#### Bounding Box 
Given an array of points, calculates the smallet bounding box that contains all of the 3D points.  
Returns a JSON of 3D **bounding box** coordinate points,  
[[x<sub>1</sub>, y<sub>1</sub>, z<sub>1</sub>], [x<sub>2</sub>, y<sub>2</sub>, z<sub>2</sub>], [...]]   

#### Rotate Mesh
Given a 3D Mesh as an Input, rotates the mesh by X degrees along the specified axis.  
Returns a JSON of **rotated** 3D coordinate points,  
[[x<sub>1</sub>, y<sub>1</sub>, z<sub>1</sub>], [x<sub>2</sub>, y<sub>2</sub>, z<sub>2</sub>], [...]]   

#### Move Mesh 
Given a 3D mesh as an input, moves the mesh by a, b and c units along X, Y and Z axis respectively.  
Returns a JSON of **moved** 3D coordinate points,  
[[x<sub>1</sub>, y<sub>1</sub>, z<sub>1</sub>], [x<sub>2</sub>, y<sub>2</sub>, z<sub>2</sub>], [...]]   

#### Check Convex 
Given a polygon in a 3D space represented by 3D Points, check whether the polygon is convex.  
A convex polygon is defined as a closed figure where all interior angles are less than 180 degrees.  
Returns a **boolean** value in JSON format  
  
![image](https://github.com/VRazgaitis/geometry_engine/assets/116982063/30699b48-926f-4ee8-afd3-96708a35aac9)

## Instructions (Linux/macOS only)
* run ./setup_and_run.sh  
* Compute geometric operations, using HTTP GET or POST requests.
* See **example.py** or **example.sh** for example usage
