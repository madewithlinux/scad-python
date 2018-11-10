package com.scad_scala

case class Hull(exprs: WritableExpr*) extends WritableExpr {
  override def write(): String =
    s"hull() {\n${
      exprs.map(_.write()).mkString
    }};\n"
}

