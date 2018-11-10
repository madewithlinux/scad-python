package com.scad_scala

case class Intersection(exprs: WritableExpr*) extends WritableExpr {
  override def write(): String =
    s"intersection() {\n${
      exprs.map(_.write()).mkString
    }};\n"
}

