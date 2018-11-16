from scad import *
from scad.shapes import *

sharp_solid = Union([
    Cube(50, 10, 10),
    Translate(Vec3d(0, 30, 0), [Cube(50, 10, 10)]),
    Translate(Vec3d(0, -30, 0), [Cube(50, 10, 10)]),
    Cube(10, 50, 10),
])

# solid = sharp_solid
solid = RoundCorners(5, sharp_solid)

with open('scad-demo.scad', 'w') as f:
    f.write("$fn=10;\n")
    f.write(solid.write())
