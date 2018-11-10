package com.scad_scala

case class Cube(x: Double, y: Double, z: Double,
                center: Boolean = true
               ) extends WritableExpr {
  override def write(): String = s"cube([$x,$y,$z]${if (center) ",center=true" else ""});\n"
}
