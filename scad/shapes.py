from dataclasses import dataclass
import abc
import typing
from typing import List
from typing import Optional


class WritableExpr(object, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def write(self) -> str:
        pass


@dataclass
class Vec3d:
    x: float
    y: float
    z: float

    @property
    def bracketed(self):
        return f"[{self.x},{self.y},{self.z}]"


@dataclass
class Vec2d:
    x: float
    y: float

    @property
    def bracketed(self):
        return f"[{self.x},{self.y}]"


@dataclass
class Centerable:
    @property
    @abc.abstractmethod
    def center(self): pass

    @property
    def is_centered(self):
        return ",center=true" if self.center else ""


@dataclass
class Circle(WritableExpr):
    r: float

    def write(self) -> str:
        return f"circle(r={self.r});"


@dataclass
class Sphere(WritableExpr):
    r: float

    def write(self) -> str:
        return f"sphere(r={self.r});"


@dataclass
class Cone(WritableExpr, Centerable):
    h: float
    r1: float
    r2: float
    center: float = True

    def write(self) -> str:
        return f"""cylinder(h={self.h},r1={self.r1},r2={self.r2}{self.is_centered});"""


@dataclass
class Cube(WritableExpr, Centerable):
    x: float
    y: float
    z: float
    center: float = True

    def write(self) -> str:
        return f"""cube([{self.x},{self.y},{self.z}]{self.is_centered});"""


@dataclass
class Cylinder(WritableExpr, Centerable):
    h: float
    r: float
    center: bool = True

    def write(self) -> str:
        return f"""cylinder(h={self.h},r={self.r}{self.is_centered});"""


###################################################################################################


class NamedBlock(WritableExpr):
    exprs: List[WritableExpr]

    @property
    def blockname(self) -> str:
        return self.__class__.__name__.lower()

    def inner_exprs(self) -> str:
        return '\n'.join(x.write() for x in self.exprs)

    def in_parenthesis(self):
        return ""

    def write(self) -> str:
        return f"""{self.blockname}({self.in_parenthesis()}) {{\n{ self.inner_exprs() }\n}}\n"""


@dataclass
class Difference(NamedBlock):
    exprs: List[WritableExpr]


@dataclass
class Hull(NamedBlock):
    exprs: List[WritableExpr]


@dataclass
class Intersection(NamedBlock):
    exprs: List[WritableExpr]


@dataclass
class Union(NamedBlock):
    exprs: List[WritableExpr]


@dataclass
class Minkowski(NamedBlock):
    exprs: List[WritableExpr]


@dataclass
class Translate(NamedBlock):
    vec: Vec3d
    exprs: List[WritableExpr]

    def in_parenthesis(self):
        return self.vec.bracketed


@dataclass
class RotateExtrude(NamedBlock):
    angle: float
    exprs: List[WritableExpr]

    @property
    def blockname(self) -> str:
        return 'rotate_extrude'

    def in_parenthesis(self):
        return f"angle={self.angle}"


@dataclass
class RotateV(NamedBlock):
    a_deg: float
    v: Vec3d
    exprs: List[WritableExpr]

    @property
    def blockname(self) -> str:
        return 'rotate'

    def in_parenthesis(self):
        return f"a={self.a_deg},v={self.v.bracketed}"


@dataclass
class RotateC(NamedBlock):
    deg_x: float
    deg_y: float
    deg_z: float
    exprs: List[WritableExpr]

    @property
    def blockname(self) -> str:
        return 'rotate'

    def in_parenthesis(self):
        return f"[{self.deg_x},{self.deg_y},{self.deg_z}]"


###################################################################################################

@dataclass
class Tube(WritableExpr):
    r1: float
    r2: float
    h: float

    @property
    def od(self): return 2 * self.r2

    @property
    def id(self): return 2 * self.r1

    @property
    def wall(self): return self.r2 - self.r1

    def write(self) -> str:
        innerCylinder = Cylinder(self.h + 1, self.r1)
        outerCylinder = Cylinder(self.h, self.r2)
        difference = Difference([outerCylinder, innerCylinder])
        return difference.write()

    @staticmethod
    def r1WallHeight(r1: float, wall: float, h: float) -> 'Tube':
        r2 = r1 + wall
        return Tube(r1, r2, h)


@dataclass
class EdgeFillet(WritableExpr):
    r: float
    d: float

    def write(self) -> str:
        r = self.r
        d = self.d
        base = Cube(d, 2 * r, 2 * r)

        remove = Hull([
            Translate(Vec3d(d, r, r), [Sphere(r)]),
            Translate(Vec3d(-d, r, r), [Sphere(r)]),
        ])

        solid = Difference([
            base,
            remove,
        ])

        return solid.write()


@dataclass
class FilletCube(WritableExpr):
    x: float
    y: float
    z: float
    r: float

    def write(self) -> str:
        r = self.r
        x = self.x - 2 * r
        y = self.y - 2 * r
        z = self.z - 2 * r
        assert min([x, y, z]) > 0
        solid = Minkowski([
            Cube(x, y, z),
            Sphere(r),
        ])
        return solid.write()


@dataclass
class PairwiseHull(WritableExpr):
    exprs: List[WritableExpr]
    loop: bool = True

    def write(self) -> str:
        pairs: List[WritableExpr]
        if self.loop:
            pairs = zip(self.exprs, self.exprs[1:] + [self.exprs[0]])
        else:
            pairs = zip(self.exprs, self.exprs[1:])
        return Union([Hull([a, b]) for (a, b) in pairs]).write()


@dataclass
class RoundCorners(WritableExpr):
    r: float
    solid: WritableExpr

    def write(self) -> str:
        r = self.r
        cube = Cube(2 * r, 2 * r, 2 * r)
        sphere = Sphere(r)

        a = self.solid
        b = Minkowski([a, cube])
        c = Difference([b, a])  # hollow shell
        d = Minkowski([c, sphere])  # smaller hollow shell
        e = Difference([a, d])  # original solid, but cut away by radius
        f = Minkowski([e, sphere])
        return f.write()


###################################################################################################

def xAxisCube(size: float) -> WritableExpr:
    return Translate(Vec3d(size / 2, 0, 0), [Cube(abs(size), abs(size), abs(size))])


def yAxisCube(size: float) -> WritableExpr:
    return Translate(Vec3d(0, size / 2, 0), [Cube(abs(size), abs(size), abs(size))])


def zAxisCube(size: float) -> WritableExpr:
    return Translate(Vec3d(0, 0, size / 2), [Cube(abs(size), abs(size), abs(size))])


def tran(x: float, y: float, z: float, exprs: typing.Union[List[WritableExpr], WritableExpr]) -> WritableExpr:
    if isinstance(exprs, list):
        return Translate(Vec3d(x, y, z), exprs)
    else:
        return Translate(Vec3d(x, y, z), [exprs])
