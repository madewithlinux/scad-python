package com.scad_scala

case class Cylinder(h: Double,
                    r: Double,
                   // TODO: implement two diameters
                    center: Boolean = true
                   ) extends WritableExpr {
  override def write(): String =
    s"cylinder(h=$h,${
      s"r=$r"
    }${
      if (center) ",center=true"
      else ""
    });\n"
}
