package com

package object scad_scala {
  def xAxisCube(size: Double): WritableExpr = {
    Translate(Vec3d(size / 2, 0, 0), Cube(math.abs(size), math.abs(size), math.abs(size)))
  }

  def yAxisCube(size: Double): WritableExpr = {
    Translate(Vec3d(0, size / 2, 0), Cube(math.abs(size), math.abs(size), math.abs(size)))
  }

  def zAxisCube(size: Double): WritableExpr = {
    Translate(Vec3d(0, 0, size / 2), Cube(math.abs(size), math.abs(size), math.abs(size)))
  }
}
