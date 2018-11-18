from scad import *
from scad.shapes import *

sharp_solid = Union([
    Cube(50, 10, 10),
    Translate(Vec3d(0, 30, 0), [Cube(50, 10, 10)]),
    Translate(Vec3d(0, -30, 0), [Cube(50, 10, 10)]),
    Cube(10, 50, 10),
])

r = 2

solid = Union([
    Difference([
        sharp_solid,
        zAxisCube(1000)
    ]),
    RoundCorners(r, sharp_solid),
])

with open('scad-demo.scad', 'w') as f:
    f.write("$fn=10;\n")
    f.write(solid.write())
