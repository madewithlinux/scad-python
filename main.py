from scad.shapes import *

print(Cylinder(1, 2, 3).write())
print(Cone(1, 2, 3).write())

print(Difference([
    Cube(1, 2, 3),
    Cube(1, 4, 1),
]).write())

print(Hull([
    Cube(1, 2, 3),
    Cube(1, 4, 1),
]).write())

print(Translate(Vec3d(1, 2, 3), [Cube(1, 2, 3)]).write())


@dataclass
class A:
    xs: List[str]


@dataclass
class B(A):
    y: int

    def foo(self):
        return self.xs
