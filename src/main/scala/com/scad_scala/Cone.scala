package com.scad_scala

case class Cone(h: Double,
                    r1: Double,
                    r2: Double,
                    center: Boolean = true
                   ) extends WritableExpr {
  override def write(): String =
    s"cylinder(h=$h,r1=$r1,r2=$r2${
      if (center) ",center=true"
      else ""
    });\n"
}
