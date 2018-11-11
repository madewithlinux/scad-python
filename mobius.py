from scad import *
from scad.shapes import *

r = 3
h = 15
segment = Hull([
    Translate(Vec3d(0, 0, +h), [Sphere(r)]),
    Translate(Vec3d(0, 0, -h), [Sphere(r)]),
])

r2 = 80
angle_delta = 5

solid = PairwiseHull([
    RotateC(0, 0, d, [
        Translate(Vec3d(0, r2, 0), [
            RotateC(d / 2, 0, 0, [

                segment
            ])
        ])
    ])
    for d in frange(0, 360, angle_delta)
])

with open('scad-demo.scad', 'w') as f:
    f.write("$fn=20;\n")
    f.write(solid.write())
