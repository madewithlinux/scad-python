package com.scad_scala

case class Difference(exprs: WritableExpr*) extends WritableExpr {
  override def write(): String =
    s"difference() {\n${
      exprs.map(_.write()).mkString
    }};\n"
}

