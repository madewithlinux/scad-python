package com.scad_scala

case class Vec3d(x: Double,
                 y: Double,
                 z: Double,
                ) {
  def bracketed: String = s"[$x, $y, $z]"
}
