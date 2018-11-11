from scad import *
from scad.shapes import *
from math import pi
import math

phi = (1 + math.sqrt(5)) / 2.0

r = 0.1
d = 10
diamond = Hull([
    Translate(Vec3d(+d, 0, 0), [Sphere(r)]),
    Translate(Vec3d(-d, 0, 0), [Sphere(r)]),
    Translate(Vec3d(0, +d, 0), [Sphere(r)]),
    Translate(Vec3d(0, -d, 0), [Sphere(r)]),
    Translate(Vec3d(0, 0, +d), [Sphere(r)]),
    Translate(Vec3d(0, 0, -d), [Sphere(r)]),
])

segments = [
    diamond,
    Cone(d, d, 0, center=False),
    Sphere(d),
]


def getCoaster(segment: WritableExpr):
    c = 5

    def getSegment(n: int):
        theta = 2 * pi / (phi * phi) * n
        theta = theta * 180 / pi  # degrees
        r = c * math.sqrt(n)
        return RotateC(0, 0, theta, [Translate(Vec3d(0, r, 0), [segment])])

    return Intersection([
        Union([
            getSegment(n)
            for n in range(500)
        ]),
        zAxisCube(1000)
    ])


solid = Union([
    Translate(Vec3d(250 * i, 0, 0), [getCoaster(seg)])
    for (i, seg) in enumerate(segments)
])

with open('scad-demo.scad', 'w') as f:
    f.write("$fn=100;\n")
    f.write(solid.write())
