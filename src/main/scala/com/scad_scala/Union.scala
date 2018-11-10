package com.scad_scala

case class Union(exprs: WritableExpr*) extends WritableExpr {
  override def write(): String =
    s"union() {\n${
      exprs.map(_.write()).mkString
    }};\n"
}

//object Union {
//  def apply(exprs: WritableExpr*): Union = new Union(exprs)
//}
