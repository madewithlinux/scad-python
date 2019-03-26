from scad import *
from scad.shapes import *
from math import sqrt

m1 = Import("stl/brain-lh.stl",
            center=True,
            convexity=30)
m2 = Import("stl/brain-rh.stl",
            center=True,
            convexity=30)

brain_hull = Hull([m1, m2])

# scale = 0.8
scale = 0.87
brain_insert0 = Difference([
    Scale(Vec3d(scale, scale, scale), [brain_hull]),
    tran(0, 50, -15, [Cube(150, 50, 45)]),
])

sc = 0.53
brain_insert = Scale(Vec3d(sc, sc, sc), [brain_insert0])
brain_insert = tran(24, -2, 75, [brain_insert])

trivia_trophy = Import("stl/trivia_trophy_fixed.stl",
                       center=True,
                       convexity=30)

solid = Union([
    # trivia_trophy,
    # Color(Vec3d(1, 0, 0), [Cube(70,100,60*2)]),
    # Color(Vec3d(1, 0, 0), [brain_insert]),
    Color(Vec3d(1, 0, 0), [brain_insert0]),
    m1,
    m2,
])

with open('scad-demo.scad', 'w') as f:
    f.write("$fn=20;\n")
    f.write(solid.write())
