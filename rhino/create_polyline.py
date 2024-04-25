"""
Run python in Rhino using EditPythonScript in the commandline
"""

import rhinoscriptsyntax as rs

points =   [[4.1949637777057571, -6.9916062961762613, 16.047420986034020], 
             [6.8206194998754439, -4.0247156045330703, 16.598321750671875], 
             [-0.48443183668373879, 1.7688355092261352, 20.213704228708519], 
             [-3.1100875588534249, -1.1980551824170558, 19.662803464070663], 
             [3.4299717028501773, 2.0579830217101063, -6.6613381477509392e-16], 
             [-3.8750796337090048, 7.8515341354693104, 3.6153824780366430], 
             [-6.5007353558786898, 4.8846434438261213, 3.0644817133987878], 
             [0.80431598068049104, -0.90890766993308547, -0.55090076463785609]]
name = 'non convex penta'

if points:
    polyline_id = rs.AddPolyline(points)
    if polyline_id:
        rs.SelectObject(polyline_id)
        rs.ObjectName(polyline_id, name)
        print("Polyline created and selected.")