from scad import *
from scad.shapes import *
from math import sqrt

prusa_build_plate = tran(0, 0, -10, [
    Color(Vec3d(0.5, 0.5, 0.5), [Cube(250, 210, 10)]),
])
makerbot_5thgen_build_plate = tran(0, 0, -10, [
    Color(Vec3d(1, 0, 0.0), [Cube(252, 199, 10)]),
])

# makerbot_5thgen_build_plate = tran(8,27,0,[
#     RotateC(0,0,0,[makerbot_5thgen_build_plate]),
# ])

spacing = 0.2
model = tran(-191.0013, 198.89575 + spacing, -50.0,
             Import("stl/Escher_Lizard_LowPoly_Small_ok.stl",
                    center=True,
                    convexity=10))

# cutout bottom part so the models stack vertically also
model = Difference([
    model,
    tran(0, 0, -2.1, [model]),
])

model = Scale(Vec3d(2.5, 2.5, 2.5), [model])

m1 = Union([
    model,
    RotateC(0, 0, 120, [model]),
    RotateC(0, 0, -120, [model]),
])

d = 13 * 2.5
m2 = Union([
    m1,
    tran(d, d * sqrt(3), 0, [m1]),
    RotateC(0, 0, 120, [tran(d, d * sqrt(3), 0, [m1]), ]),
    RotateC(0, 0, 60, [tran(d, d * sqrt(3), 0, [RotateC(0, 0, 60, [m1])]), ]),
])
solid = Union([
    m2,
    Color(Vec3d(0, 0, 0), [tran(d, -d * sqrt(3), 0, [RotateC(0, 0, 0, [model])]), ]),
    Color(Vec3d(0, 1, 0), [tran(-d, -d * sqrt(3), 0, [RotateC(0, 0, 0, [model])]), ]),
    Color(Vec3d(0, 1, 1), [tran(3 * d, -d * sqrt(3), 0, [RotateC(0, 0, 0, [model])]), ]),
    Color(Vec3d(1, 0, 0), [tran(-3 * d, d * sqrt(3), 0, [RotateC(0, 0, -120, [model])]), ]),
    Color(Vec3d(1, 0, 1), [tran(2 * d, 0, 0, [RotateC(0, 0, 0, [m1])]), ]),
    Color(Vec3d(1, 1, 0), [tran(3 * d, d * sqrt(3), 0, [RotateC(0, 0, 0, [model])]), ]),
    Color(Vec3d(1, 0, 1), [tran(3 * d, d * sqrt(3), 0, [RotateC(0, 0, 120, [model])]), ]),
    Color(Vec3d(1, 1, 1), [tran(0, 2 * d * sqrt(3), 0, [RotateC(0, 0, 120, [model])]), ]),
    Color(Vec3d(0, 0, 0), [tran(-2 * d, 2 * d * sqrt(3), 0, [RotateC(0, 0, 120, [model])]), ]),
    Color(Vec3d(0, 0, 1), [tran(2 * d, 2 * d * sqrt(3), 0, [RotateC(0, 0, 120, [model])]), ]),
    #
    Color(Vec3d(0, 0, 0), [tran(-2 * d, 2 * d * sqrt(3), 0, [RotateC(0, 0, -120, [model])]), ]),
    Color(Vec3d(1, 1, 1), [tran(0, 2 * d * sqrt(3), 0, [RotateC(0, 0, -120, [model])]), ]),
    Color(Vec3d(0, 0, 1), [tran(2 * d, 2 * d * sqrt(3), 0, [RotateC(0, 0, -120, [model])]), ]),
    # does not fit
    # Color(Vec3d(0, 1, 1), [tran(4 * d, 0, 0, [RotateC(0, 0, 120, [model])]), ]),
])

solid = tran(-17, -38, 0, [solid])

# solid = Union([solid, makerbot_5thgen_build_plate])
# solid = Union([solid, prusa_build_plate])

with open('scad-demo.scad', 'w') as f:
    f.write("$fn=20;\n")
    f.write(solid.write())
