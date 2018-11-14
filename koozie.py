from scad import *
from scad.shapes import *

can_diameter = 68.0
can_rad = can_diameter / 2
can_height = 100.0

wall_thickness = 1.25
ice_thickness = 5
airgap_thickness = ice_thickness * 0.75

inner_wall = Tube(can_rad, can_rad + wall_thickness, can_height)
outer_wall = Tube.r1WallHeight(inner_wall.r2 + ice_thickness, airgap_thickness, can_height)

walls = Translate(Vec3d(0, 0, can_height / 2), [
    inner_wall,
    outer_wall,
])

############## bottom cap
butt_cap_edge_rad = outer_wall.wall
butt_cap = Difference([
    Minkowski([
        Cylinder(10, outer_wall.r2 - butt_cap_edge_rad, center=False),
        Sphere(butt_cap_edge_rad),
    ]),
    zAxisCube(10000)
])

############## top cap
top_cap_base_r = (outer_wall.r2 + inner_wall.r1) / 2
top_cap_curve_r = (outer_wall.r2 - inner_wall.r1) / 2


def top_cap_shell(r: float):
    return RotateExtrude(360, [Translate(Vec3d(top_cap_base_r, 0, 0), [Circle(r)])])


top_outer_shell = top_cap_shell(top_cap_curve_r)
top_inner_shell = top_cap_shell(top_cap_curve_r - wall_thickness)
ice_air_cap_wall = Intersection([
    top_outer_shell,
    outer_wall,
])

top_cap = Translate(Vec3d(0, 0, can_height), [
    Difference([
        Union([
            Difference([
                top_outer_shell,
                top_inner_shell,
            ]),
            ice_air_cap_wall
        ]),
        zAxisCube(-1000)
    ])
])

############## spout
spout_radius = 15
spout_height = 30
spout_curve_rad = inner_wall.r2 + 0.1
spout_shaper = Difference([
    Translate(
        Vec3d(spout_curve_rad, 0, can_height),
        [Cone(spout_height, 0, spout_radius)]
    ),
    Cylinder(can_height * 2, spout_curve_rad, center=False)
])

############## inner supports
n_supports = 8

support = Translate(Vec3d(inner_wall.r1 + wall_thickness / 2, 0, 0), [
    Cube(ice_thickness + wall_thickness, wall_thickness, can_height * 0.75, center=False)
])

supports = Union([
    RotateC(0, 0, d, [support])
    for d in frange(0, 360, 360 / n_supports)
])

solid: WritableExpr = Union([
    Difference([
        Union([
            walls,
            top_cap,
            butt_cap,
            supports,
        ]),
        spout_shaper,
    ])
])

solid = Difference([solid, yAxisCube(1000)])


with open('scad-demo.scad', 'w') as f:
    f.write("$fn=10;\n")
    f.write(solid.write())
