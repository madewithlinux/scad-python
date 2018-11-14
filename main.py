from scad import *
from scad.shapes import *

solid = Minkowski([
    Sphere(4),
    Cube(10, 20, 30),
])

solid = FilletCube(4.000000000000001, 20, 30, 4)

with open('scad-demo.scad', 'w') as f:
    f.write("$fn=50;\n")
    f.write(solid.write())
