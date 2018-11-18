from scad import *
from scad.shapes import *

sharp_solid = Union([
    Cube(10, 50, 10),

    Translate(Vec3d(0, -30, 0), [Cube(30, 10, 10)]),
    Cube(30, 10, 10),
    Translate(Vec3d(0, 30, 0), [Cube(30, 10, 10)]),

    Translate(Vec3d(0, -30, 0), [Cube(60, 2, 2)]),
    Cube(60, 4, 4),
    Translate(Vec3d(0, 30, 0), [Cube(60, 7, 7)]),

])

r = 2

solid = Union([
    Difference([
        sharp_solid,
        zAxisCube(1000)
    ]),
    RoundCorners(r, sharp_solid),
])

# cube = Cube(2 * r, 2 * r, 2 * r)
# sphere = Sphere(r)
#
# a = sharp_solid
# b = Minkowski([a, cube])
# c = Difference([b, a]) # hollow shell
# d = Minkowski([c, sphere]) # smaller hollow shell
# e = Difference([a, d]) # original solid, but cut away by radius
# f = Minkowski([e, sphere])
#
# solid = Union([
#     Translate(Vec3d(0, 0, z * 20), [
#         Difference([
#             s,
#             zAxisCube(1000)
#         ]),
#     ])
#     for (z, s) in enumerate([
#         f, sharp_solid, b, c, d, e, f,
#                              # cube, sphere,
#     ])
# ])

with open('scad-demo.scad', 'w') as f:
    f.write("$fn=10;\n")
    f.write(solid.write())
