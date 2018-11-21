from scad import *
from scad.shapes import *

x = 10
y = 20
z = 30
solid = Union([
    FilletCube(x, y, z, 2),
    # Cube(x, y, z),
    Translate(Vec3d(x / 2 + 1, 0, 0), [Sphere(1)]),
    Translate(Vec3d(0, y / 2 + 1, 0), [Sphere(1)]),
    Translate(Vec3d(0, 0, z / 2 + 1), [Sphere(1)]),
])

with open('scad-demo.scad', 'w') as f:
    f.write("$fn=50;\n")
    f.write(solid.write())
