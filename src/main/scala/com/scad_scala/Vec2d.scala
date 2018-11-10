package com.scad_scala

case class Vec2d(x: Double,
                 y: Double,
                ) {
  def bracketed: String = s"[$x, $y]"
}
