package com.scad_scala

case class LinearExtrude(height: Double,
                         twist: Option[Double],
                         slices: Option[Double],
                         exprs: WritableExpr*) extends WritableExpr {
  override def write(): String =
    s"linear_extrude(height=$height${
      twist match {
        case None => ""
        case Some(value) => s",twist=$value"
      }
    }${
      slices match {
        case None => ""
        case Some(value) => s",slices=$value"
      }
    }) {\n${
      exprs.map(_.write()).mkString
    }};\n"
}


object LinearExtrude {
  def apply(height: Double,
            exprs: WritableExpr*): LinearExtrude = new LinearExtrude(height, None, None, exprs: _*)

  def withTwistAndSlices(height: Double,
                         twist: Option[Double],
                         slices: Option[Double],
                         exprs: WritableExpr*) =
    new LinearExtrude(height, twist, slices, exprs: _*)
}
