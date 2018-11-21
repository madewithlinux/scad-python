from scad import *
from scad.shapes import *

r = 2

cable_diameter = 2

remote_height = 6
remote_width = 10
remote_length = 45
remote_cable_connector_length = 3
remote_cable_connector_diameter = 3.5

outer_smooth_box_height = remote_height + 2
outer_smooth_box_length = remote_length + remote_cable_connector_length * 2
outer_smooth_box_width = 24
outer_smooth_box_radius = r
outer_smooth_box = tran(0, 0, -outer_smooth_box_height / 2, [
    FilletCube(outer_smooth_box_width,
               outer_smooth_box_length,
               outer_smooth_box_height,
               outer_smooth_box_radius)
])

################################################################################################
remote_slot_center_dist = remote_length - remote_width
remote_body_slot = Hull([
    tran(0,
         -remote_slot_center_dist / 2,
         -remote_height,
         [Cylinder(remote_height, remote_width / 2, center=False)]),
    tran(0,
         remote_slot_center_dist / 2,
         -remote_height,
         [Cylinder(remote_height, remote_width / 2, center=False)]),
])

remote_cable_slot = Hull([
    tran(0, 100, -remote_height / 2, [Sphere(remote_cable_connector_diameter / 2)]),
    tran(0, -100, -remote_height / 2, [Sphere(remote_cable_connector_diameter / 2)]),
    tran(0, 100, 10, [Sphere(remote_cable_connector_diameter / 2)]),
    tran(0, -100, 10, [Sphere(remote_cable_connector_diameter / 2)]),
])

remote_slot = Union([remote_body_slot, remote_cable_slot])

################################################################################################
cable_slot_center_x = (remote_width + outer_smooth_box_width) / 2 / 2
cable_slot_diameter = cable_diameter * 1.5
cable_slot = tran(cable_slot_center_x, 0, 0, [
    Hull([
        tran(0, 100, -cable_diameter, [Sphere(cable_slot_diameter / 2)]),
        tran(0, -100, -cable_diameter, [Sphere(cable_slot_diameter / 2)]),
        tran(0, 100, 10, [Sphere(cable_slot_diameter / 2)]),
        tran(0, -100, 10, [Sphere(cable_slot_diameter / 2)]),
    ])
])

cable_slot = Union([
    cable_slot,
    RotateC(0, 0, 180, [cable_slot]),
])

################################################################################################
cable_slot_edge_fix = Hull([
    tran(0, 0, -r, FilletCube(2 * r, 2 * r, 2 * r, 0.1)),
    tran(0, 0, -(outer_smooth_box_height - r), Sphere(r))
])
cable_slot_edge_fix = Hull([
    tran(outer_smooth_box_width / 2 - r, outer_smooth_box_length / 2 - r, 0, cable_slot_edge_fix),
    tran(outer_smooth_box_width / 2 - r, -(outer_smooth_box_length / 2 - r), 0, cable_slot_edge_fix),
])
cable_slot_edge_fix = Difference([
    cable_slot_edge_fix,
    cable_slot,
    tran(outer_smooth_box_width / 2 - r, 0, 0, xAxisCube(-1000)),
    zAxisCube(10000)
])
cable_slot_edge_fix = Union([
    cable_slot_edge_fix,
    RotateC(0, 0, 180, [cable_slot_edge_fix]),
])

################################################################################################
cable_ridge_radius = (cable_slot_diameter - cable_diameter) / 2
cable_ridge_y_start = 0.7 * outer_smooth_box_length / 2
cable_ridge_spacing = cable_ridge_radius * 2 * 2
n_cable_ridges = 3
cable_ridge = Cylinder(outer_smooth_box_height, cable_ridge_radius, center=False)
cable_ridges = Union([
    tran(cable_slot_center + d,
         y_offset + y_delta * sgn(y_offset),
         -outer_smooth_box_height,
         Cylinder(outer_smooth_box_height, cable_ridge_radius, center=False))
    for d in [-cable_slot_diameter / 2, cable_slot_diameter / 2]
    for cable_slot_center in [-cable_slot_center_x, cable_slot_center_x]
    for y_offset in [-cable_ridge_y_start, cable_ridge_y_start]
    for y_delta in [cable_ridge_spacing * n for n in range(n_cable_ridges)]
])

################################################################################################
solid = Union([
    Difference([
        outer_smooth_box,
        remote_slot,
        cable_slot,
    ]),
    cable_slot_edge_fix,
    cable_ridges,
])

with open('scad-demo.scad', 'w') as f:
    f.write("$fn=20;\n")
    f.write(solid.write())
