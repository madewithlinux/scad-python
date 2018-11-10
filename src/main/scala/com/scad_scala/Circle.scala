package com.scad_scala

case class Circle(r: Double) extends WritableExpr {
  override def write(): String =
    s"circle(r=$r);"
}
