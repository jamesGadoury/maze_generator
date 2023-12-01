from argparse import ArgumentParser

# TODO This script relies on the x,y being 1 for box extents. It could handle arbitrary x,y extents if smarter.

def main(args):

    # Create an SDF string based on the maze
    sdf_content = f"""<?xml version="1.0" ?>
    <sdf version="1.6">
    <world name="default">
        <!-- Define a simple ground plane -->
        <include>
        <uri>model://ground_plane</uri>
        </include>
    """

    with open(args.input_file) as f:
        lines = [line.rstrip() for line in f.readlines()]

    y = 0
    for line in lines:
        x = 0
        for c in line:
            if c == "x":
                sdf_content += f"""
                    <model name="maze_wall_{x}_{y}">
                    <static>true</static>
                    <link name="link">
                        <collision name="collision">
                        <geometry>
                            <box>
                            <size>1 1 {args.wall_height}</size>
                            </box>
                        </geometry>
                        </collision>
                        <visual name="visual">
                        <geometry>
                            <box>
                            <size>1 1 {args.wall_height}</size>
                            </box>
                        </geometry>
                        <material>
                            <script>
                            <uri>file://media/materials/scripts/gazebo.material</uri>
                            <name>Gazebo/White</name>
                            </script>
                        </material>
                        </visual>
                    </link>
                    <pose>{x} {y} 0 0 0 0</pose>
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
    parser.add_argument("--input-file", default="input_maze.txt")
    parser.add_argument("--output-file", default="maze_world.sdf")
    parser.add_argument("--wall-height", type=float, default=0.5)

    main(parser.parse_args())