package com.scad_scala

case class RotateExtrude(angle: Double, exprs: WritableExpr*) extends WritableExpr {
  override def write(): String =
    s"rotate_extrude(angle=$angle) {\n${
      exprs.map(_.write()).mkString
    }};\n"
}
