package com.scad_scala

case class Minkowski(a: WritableExpr, b: WritableExpr) extends WritableExpr {
  override def write(): String =
    s"minkowski() {\n${a.write()}\n${b.write()}\n};\n"
}
