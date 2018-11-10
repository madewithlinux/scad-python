package com.scad_scala

case class RotateC(deg_x: Double,
                   deg_y: Double,
                   deg_z: Double,
                   exprs: WritableExpr*
                  ) extends WritableExpr {
  override def write(): String =
    s"rotate(a=[$deg_x,$deg_y,$deg_z]) {\n${
      exprs.map(_.write()).mkString
    }};\n"

}
