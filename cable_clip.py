import math
from scad import *
from scad.shapes import *


def write(solid: WritableExpr):
    with open('scad-demo.scad', 'w') as f:
        f.write("$fn=50;\n")
        f.write(solid.write())
    import sys
    sys.exit(0)


descartes_ratio = 1 / 3 * (3 + 2 * math.sqrt(3))
cable_diameter = 2

print("ideal sleeve diameter", descartes_ratio * cable_diameter)

sleeve_height = 10
sleeve_thickness = 0.75
twist = 90
cut_height = 0.5


def cable_sleeve(sleeve_diameter,
                 sleeve_height,
                 sleeve_thickness,
                 twist,
                 cut_height):
    r = sleeve_thickness / 2

    sleeve_outer_section = RotateExtrude(360, [Hull([
        tran(sleeve_diameter / 2 + r, +sleeve_height / 2, 0, [Circle(r)]),
        tran(sleeve_diameter / 2 + r, -sleeve_height / 2, 0, [Circle(r)]),
    ])])

    return Difference([
        sleeve_outer_section,
        LinearExtrude(sleeve_height + 3 * r,
                      [tran(sleeve_diameter / 2 + r, 0, 0, [Square(r * 3, cut_height, center=True)])],
                      twist=twist,
                      center=True),
    ])


spacing = 10

solid = Union([
    tran(spacing * x,
         spacing * y,
         sleeve_height / 2 + sleeve_thickness / 2,  # make sure they're all level on the xy-plane
         [cable_sleeve(sleeve_diameter=sleeve_diameter,
                       sleeve_height=sleeve_height,
                       sleeve_thickness=sleeve_thickness,
                       twist=twist,
                       cut_height=cut_height)])
    for x, sleeve_thickness in enumerate([0.75, 1, 1.25, 1.5, 1.75, 2])
    for y, sleeve_diameter in enumerate(linspace(3.85, 5, 6))
])

write(solid)
