import math
from scad import *
from scad.shapes import *


def write(solid: WritableExpr):
    with open('scad-demo.scad', 'w') as f:
        f.write("$fn=50;\n")
        f.write(solid.write())
    import sys
    sys.exit(0)


cable_diameter = 2
descartes_ratio = 1 / 3 * (3 + 2 * math.sqrt(3))

sleeve_diameter = descartes_ratio * cable_diameter * 0.9
sleeve_height = 10
sleeve_thickness = 0.75
twist = 90
cut_height = 0.3

r = sleeve_thickness / 2

sleeve_outer_section = RotateExtrude(360, [
    Hull([
        tran(sleeve_diameter / 2 + r, +sleeve_height / 2, 0, [Circle(r)]),
        tran(sleeve_diameter / 2 + r, -sleeve_height / 2, 0, [Circle(r)]),
    ])
])

solid = Difference([
    sleeve_outer_section,
    LinearExtrude(sleeve_height + 3 * r,
                  [tran(sleeve_diameter / 2 + r, 0, 0, [Square(r * 3, cut_height, center=True)])],
                  twist=twist,
                  center=True),
])

write(solid)
