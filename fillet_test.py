from scad import *
from scad.shapes import *

r = 10
x = 100
y = 50
z = 150

# base = Cube(d, 2 * r, 2 * r)
#
# remove = Hull([
#     Translate(Vec3d(d, r, r), [Sphere(r)]),
#     Translate(Vec3d(-d, r, r), [Sphere(r)]),
# ])
#
# solid = Difference([
#     base,
#     remove,
# ])


solid = Union([
    Cube(x, y, z),
    # Translate(Vec3d(0, y / 2, z / 2), [RotateC(180, 0, 0, [EdgeFillet(r, x)])]),
    # Translate(Vec3d(0, -y / 2, z / 2), [RotateC(-90, 0, 0, [EdgeFillet(r, x)])]),
    # Translate(Vec3d(0, y / 2, -z / 2), [RotateC(90, 0, 0, [EdgeFillet(r, x)])]),
    # Translate(Vec3d(0, -y / 2, -z / 2), [RotateC(0, 0, 0, [EdgeFillet(r, x)])]),
    #
    # Translate(Vec3d(x / 2, -y / 2, 0), [RotateC(0, 90, 90, [EdgeFillet(r, z)])]),
    # Translate(Vec3d(x / 2, y / 2, 0), [RotateC(0, -90, 90, [EdgeFillet(r, z)])]),
    # Translate(Vec3d(-x / 2, -y / 2, 0), [RotateC(0, 90, 0, [EdgeFillet(r, z)])]),
    # Translate(Vec3d(-x / 2, y / 2, 0), [RotateC(0, -90, 180, [EdgeFillet(r, z)])]),

    Translate(Vec3d(x / 2, 0, z / 2), [RotateC(-90, 0, 90, [EdgeFillet(r, y)])]),
    Translate(Vec3d(x / 2, 0, z / 2), [RotateC(-90, 0, 90, [EdgeFillet(r, y)])]),
])

with open('scad-demo.scad', 'w') as f:
    f.write("$fn=50;\n")
    f.write(solid.write())
