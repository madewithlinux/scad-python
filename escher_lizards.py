from scad import *
from scad.shapes import *
from math import sqrt

spacing = 0.2
model = tran(-191.0013, 198.89575 + spacing, -50.0,
             Import("stl/Escher_Lizard_LowPoly_Small_ok.stl",
                    center=True,
                    convexity=10))
m1 = Union([
    model,
    RotateC(0, 0, 120, [model]),
    RotateC(0, 0, -120, [model]),
])

d = 13
m2 = Union([
    m1,
    tran(d, d * sqrt(3), 0, [m1]),
    RotateC(0, 0, 120, [tran(d, d * sqrt(3), 0, [m1]), ]),
    RotateC(0, 0, 60, [tran(d, d * sqrt(3), 0, [RotateC(0, 0, 60, [m1])]), ]),
])
solid = Union([
    m2,
    tran(2 * d, 0, 0, [m2])
])

with open('scad-demo.scad', 'w') as f:
    f.write("$fn=20;\n")
    f.write(solid.write())
