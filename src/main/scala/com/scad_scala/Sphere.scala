package com.scad_scala

case class Sphere(radius: Double) extends WritableExpr {
  override def write(): String = s"sphere(r=$radius);\n"
}
