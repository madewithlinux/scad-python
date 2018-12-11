from scad import *
from scad.shapes import *

r = 10

house_key_base_height = 4.0 / 2
house_key_middle_height = 8.0 / 2
house_key_middle_width = 24.7
house_key_dist_to_middle = 25
house_key_dist_overall = 60
house_key_nozzle_radius = 6.2 / 2

pivot_hole = Translate(Vec3d(0, 0, house_key_base_height), [
    Cylinder(4, 4, center=True),
])

foo = Translate(Vec3d(0, house_key_dist_to_middle, house_key_middle_height), [
    Cube(house_key_middle_width, 1, 1),
])

house_key_part_1 = PairwiseHull([
    pivot_hole,
    foo,
    Translate(Vec3d(0, 40, house_key_middle_height), [
        Cube(house_key_middle_width, 1, 1),
    ])
], loop=False)

solid = house_key_part_1

with open('scad-demo.scad', 'w') as f:
    f.write("$fn=20;\n")
    f.write(solid.write())
