package com.scad_scala

case class RotateV(a_deg: Double,
                   v: Vec3d,
                   exprs: WritableExpr*
                  ) extends WritableExpr {
  override def write(): String =
    s"rotate(a=$a_deg,v=${v.bracketed}) {\n${
      exprs.map(_.write()).mkString
    }};\n"

}
