# Create an SDF string based on the maze
sdf_content = f"""<?xml version="1.0" ?>
<sdf version="1.6">
  <world name="default">
    <!-- Define a simple ground plane -->
    <include>
      <uri>model://ground_plane</uri>
    </include>
"""

pairs = []

with open("input_maze.txt") as f:
    lines = [line.rstrip() for line in f.readlines()]

y = 0
for line in lines:
    print(line)
for line in lines:
    x = 0
    for c in line:
        if c == "x":
            pairs.append((x,y))
            sdf_content += f"""
                <model name="maze_wall_{x}_{y}">
                <static>true</static>
                <link name="link">
                    <collision name="collision">
                    <geometry>
                        <box>
                        <size>1 1 1</size>
                        </box>
                    </geometry>
                    </collision>
                    <visual name="visual">
                    <geometry>
                        <box>
                        <size>1 1 1</size>
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
print(pairs)
# Save the SDF content to a file
with open("maze_world.sdf", "w") as sdf_file:
    sdf_file.write(sdf_content)
