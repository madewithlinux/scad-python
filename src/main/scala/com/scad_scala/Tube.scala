package com.scad_scala

case class Tube(
                 r1: Double, // inner radius
                 r2: Double, // outer radius
                 h: Double,
               ) extends WritableExpr {

  assert(r1 >= 0)
  assert(r2 >= 0)
  assert(r2 >= r1)
  assert(h >= 0)

  // add on a small delta for the hole-cutting operation to work properly
  val innerCylinder = Cylinder(h + 1, r1)
  val outerCylinder = Cylinder(h, r2)
  val difference = Difference(outerCylinder, innerCylinder)

  def od: Double = 2 * r2

  def id: Double = 2 * r1

  def wall: Double = r2 - r1

  override def write(): String = difference.write()
}

object Tube {

  def atHeights(r1: Double,
                r2: Double,
                low_z: Double,
                high_z: Double
               ): WritableExpr = {
    val h = high_z - low_z
    val z_mid = (high_z + low_z) / 2
    val v = Vec3d(0, 0, z_mid)
    Translate(v, Tube(r1, r2, h))
  }

  def r1WallHeight(r1: Double, wall: Double, h: Double) = {
    val r2 = r1 + wall
    Tube(r1, r2, h)
  }
}