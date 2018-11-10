package com.scad_scala

case class Translate(vec: Vec3d, exprs: WritableExpr*) extends WritableExpr {
  override def write(): String =
    s"translate(${vec.bracketed}) {\n${
      exprs.map(_.write()).mkString
    }};\n"
}