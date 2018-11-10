from scad.shapes import *


def frange(x, y, jump):
    while x < y:
        yield x
        x += jump


can_diameter = 68.0
can_rad = can_diameter / 2
can_height = 100.0

wall_thickness = 1.5
ice_thickness = 5
airgap_thickness = ice_thickness * 0.75

inner_wall = Tube(can_rad, can_rad + wall_thickness, can_height)
ice_air_wall = Tube.r1WallHeight(inner_wall.r2 + ice_thickness, wall_thickness, can_height)
outer_wall = Tube.r1WallHeight(ice_air_wall.r2 + airgap_thickness, wall_thickness, can_height)

walls = Translate(Vec3d(0, 0, can_height / 2), [
    inner_wall,
    ice_air_wall,
    outer_wall,
])

############## bottom cap
# TODO: use minkowski sum for bottom can cap too?
bottom_can_cap = Cylinder(wall_thickness, inner_wall.r2, center=False)

butt_cap_inner_rad = inner_wall.r2  # * 0.875


def butt_cap(r: float):
    return Minkowski([
        Difference([
            Sphere(r),
            zAxisCube(3 * can_rad)
        ]),
        Cylinder(wall_thickness, butt_cap_inner_rad, center=False)
    ])


def butt_cap_shell(r1: float, r2: float):
    return Difference([
        butt_cap(r1 - butt_cap_inner_rad),
        butt_cap(r2 - butt_cap_inner_rad),
    ])


outer_butt_cap = butt_cap_shell(outer_wall.r2, outer_wall.r1)
ice_air_butt_cap = butt_cap_shell(ice_air_wall.r2, ice_air_wall.r1)

############## butt cap supports
support_height = outer_wall.r2 - butt_cap_inner_rad
support_radius = 1
pts = [
    (x, y)
    for x in frange(-can_rad, can_rad, can_rad / 4)
    for y in frange(-can_rad, can_rad, can_rad / 4)
]
butt_cap_supports = Intersection([
    Union([Translate(Vec3d(x, y, -support_height / 2), [Cylinder(support_height, support_radius)])
           for (x, y) in pts]),
    Cylinder(100, inner_wall.r2)
])

total_butt_cap = Union([
    outer_butt_cap,
    ice_air_butt_cap,
    butt_cap_supports,
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
    ice_air_wall,
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
spout_radius = 18
spout_height = 40
spout_curve_rad = inner_wall.r2 + 0.1
spout_shaper = Difference([
    Translate(
        Vec3d(spout_curve_rad, 0, can_height),
        [Cone(spout_height, 0, spout_radius)]
    ),
    Cylinder(can_height * 2, spout_curve_rad, center=False)
])

spout = Intersection([
    Difference([
        spout_shaper,
        Translate(Vec3d(0, 0, 2 * wall_thickness), [spout_shaper]),
        Cylinder(can_height * 2, ice_air_wall.r1 - 0.1, center=False),  # remove ice part
    ]),
    Hull([Union([walls, top_cap])]),
])

solid: WritableExpr = Union([
    spout,
    Difference([
        Union([
            walls,
            top_cap,
            bottom_can_cap,
            #            top_air_cap,
            total_butt_cap,
        ]),
        spout_shaper,
    ])
])

solid = Difference([solid, yAxisCube(1000)])

with open('scad-demo.scad', 'w') as f:
    f.write("$fn=20;\n")
    f.write(solid.write())
