import java.io.{BufferedWriter, File, FileWriter}

import com.scad_scala.{zAxisCube, _}

object Example {
  def main(args: Array[String]): Unit = {

    //////////////////////////// constants
//    val can_diameter = 66.04
    val can_diameter = 67.0
    val can_rad = can_diameter / 2
//    val can_height = 122.682
    val can_height = 100.0

    val wall_thickness = 0.5
    val ice_thickness = 5
    val airgap_thickness = ice_thickness * 0.75


    //////////////////////////// walls
    val inner_wall = Tube(can_rad, can_rad + wall_thickness, can_height)
    val ice_air_wall = Tube.r1WallHeight(inner_wall.r2 + ice_thickness, wall_thickness, can_height)
    val outer_wall = Tube.r1WallHeight(ice_air_wall.r2 + airgap_thickness, wall_thickness, can_height)

    val walls = Translate(Vec3d(0, 0, can_height / 2),
      inner_wall,
      ice_air_wall,
      outer_wall,
    )


    //////////////////////////// bottom cap
    // TODO: use minkowski sum for bottom can cap too?
    val bottom_can_cap = Cylinder(wall_thickness, inner_wall.r2, center = false)


    //////////////////////////// bottom cap (butt cap)
    val butt_cap_inner_rad = inner_wall.r2 //* 0.875

    def butt_cap(r: Double) = {
      Minkowski(
        Difference(
          Sphere(r),
          zAxisCube(3 * can_rad)
        ),
        Cylinder(wall_thickness, butt_cap_inner_rad, center = false)
      )
    }

    def butt_cap_shell(r1: Double, r2: Double) = {
      Difference(
        butt_cap(r1 - butt_cap_inner_rad),
        butt_cap(r2 - butt_cap_inner_rad),
      )
    }

    val outer_butt_cap = butt_cap_shell(outer_wall.r2, outer_wall.r1)
    val ice_air_butt_cap = butt_cap_shell(ice_air_wall.r2, ice_air_wall.r1)


    //////////////////////////// butt cap supports
    val support_height = outer_wall.r2 - butt_cap_inner_rad
    val support_radius = 1
    val r: Vector[Double] = (-can_rad to can_rad by can_rad / 4).toVector
    val pts = r.flatMap(x => r.map(y => (x, y)))
    val butt_cap_supports =
      Intersection(
        Union(pts.map {
          case (x, y) => Translate(Vec3d(x, y, -support_height / 2),
            Cylinder(support_height, support_radius))
          //            Cube(support_radius, support_radius, support_height))
        }: _*),
        Cylinder(100, can_rad - 0.1)
      )

    val total_butt_cap = Union(
      outer_butt_cap,
      ice_air_butt_cap,
      butt_cap_supports,
    )


    //////////////////////////// top cap
    val top_cap_base_r = (outer_wall.r2 + inner_wall.r1) / 2
    val top_cap_curve_r = (outer_wall.r2 - inner_wall.r1) / 2

    def top_cap_shell(r: Double) = RotateExtrude(360, Translate(Vec3d(top_cap_base_r, 0, 0), Circle(r)))

    val top_outer_shell = top_cap_shell(top_cap_curve_r)
    val top_inner_shell = top_cap_shell(top_cap_curve_r - wall_thickness)
    val ice_air_cap_wall = Intersection(
      top_outer_shell,
      ice_air_wall,
    )

    val top_cap = Translate(Vec3d(0, 0, can_height),
      Difference(
        Union(
          Difference(
            top_outer_shell,
            top_inner_shell,
          ),
          ice_air_cap_wall
        ),
        zAxisCube(-1000)
      )
    )


    //////////////////////////// spout
    val spout_radius = 18
    val spout_height = 40
    val spout_curve_rad = inner_wall.r2 + 0.1
    val spout_shaper =
      Difference(
        Translate(
          Vec3d(spout_curve_rad, 0, can_height),
          Cone(spout_height, 0, spout_radius)
        ),
        Cylinder(can_height * 2, spout_curve_rad, center = false)
      )

    val spout =
      Intersection(
        Difference(
          spout_shaper,
          Translate(Vec3d(0, 0, 2*wall_thickness), spout_shaper),
          Cylinder(can_height * 2, ice_air_wall.r1 - 0.1, center = false), // remove ice part
        ),
        Hull(Union(walls, top_cap)),
      )


    var solid: WritableExpr =
      Union(
        spout,
        Difference(
          Union(
            walls,
            top_cap,
            bottom_can_cap,
            //            top_air_cap,
            total_butt_cap,
          ),
          spout_shaper,
        )
      )

    // to make a cutaway view
//    solid = Difference(solid, yAxisCube(500))

    val bw = new BufferedWriter(new FileWriter(new File("/home/j0sh/Documents/code/scad-scala/scad-demo.scad")))
    bw.write("$fn=50;\n")
    bw.write(solid.write())
    bw.close()
  }

}
