from argparse import ArgumentParser

OLD_GAZEBO_GROUND_PLANE = """
        <!-- Define a simple ground plane -->
        <include>
            <uri>model://ground_plane</uri>
        </include>
"""

OLD_GAZEBO_WHITE_MATERIAL = """
            <material>
                <script>
                <uri>file://media/materials/scripts/gazebo.material</uri>
                <name>Gazebo/White</name>
                </script>
            </material>
"""

IGN_GAZEBO_GROUND_PLANE = """
        <!-- Define a simple ground plane -->
        <include>
            <uri>https://fuel.ignitionrobotics.org/1.0/OpenRobotics/models/Ground Plane</uri>{
        </include>
"""

def main(args):

    # Create an SDF string based on the maze
    sdf_content = f"""<?xml version="1.0" ?>
    <sdf version="1.6">
    <world name="default">
    {OLD_GAZEBO_GROUND_PLANE}
    """

    with open(args.input_file) as f:
        lines = [line.rstrip() for line in f.readlines()]

    y = 0
    for line in lines:
        x = 0
        for c in line:
            if c == "x":
                x_offset = x * args.wall_scale
                y_offset = y * args.wall_scale

                sdf_content += f"""
        <model name="maze_wall_{x_offset}_{y_offset}">
        <static>true</static>
        <link name="link">
            <collision name="collision">
            <geometry>
                <box>
                <size>{args.wall_scale} {args.wall_scale} {args.wall_height}</size>
                </box>
            </geometry>
            </collision>
            <visual name="visual">
            <geometry>
                <box>
                <size>{args.wall_scale} {args.wall_scale} {args.wall_height}</size>
                </box>
            </geometry>
            {OLD_GAZEBO_WHITE_MATERIAL}
            </visual>
        </link>
        <pose>{x_offset} {y_offset} 0 0 0 0</pose>
        </model>
                """
            x += 1
        y -= 1

    sdf_content += """
    </world>
    </sdf>
    """
    # Save the SDF content to a file
    with open(args.output_file, "w") as sdf_file:
        sdf_file.write(sdf_content)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("input_file", default="input_maze.txt")
    parser.add_argument("--output-file", default="maze_world.sdf")
    parser.add_argument("--wall-scale", type=float, default=0.5)
    parser.add_argument("--wall-height", type=float, default=0.5)

    main(parser.parse_args())
