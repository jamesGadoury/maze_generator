import pygame
import random

# Set up Pygame
pygame.init()

# Maze dimensions
WIDTH, HEIGHT = 10, 10
CELL_SIZE = 30

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize the maze grid
maze = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]

# Function to generate the maze using recursive backtracking
def generate_maze(x, y):
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    random.shuffle(directions)

    for dx, dy in directions:
        nx, ny = x + 2 * dx, y + 2 * dy

        if 0 <= nx < WIDTH and 0 <= ny < HEIGHT and maze[ny][nx] == 0:
            maze[y + dy][x + dx] = 1
            maze[ny][nx] = 1
            generate_maze(nx, ny)

# Generate the maze starting from the top-left corner
generate_maze(0, 0)

# Create an SDF string based on the maze
sdf_content = f"""<?xml version="1.0" ?>
<sdf version="1.6">
  <world name="default">
    <!-- Define a simple ground plane -->
    <include>
      <uri>model://ground_plane</uri>
    </include>
"""

for y in range(HEIGHT):
    for x in range(WIDTH):
        if maze[y][x] == 1:
            model_name = f"maze_wall_{y}_{x}"
            sdf_content += f"""
    <model name="{model_name}">
      <static>true</static>
      <link name="link">
        <collision name="collision">
          <geometry>
            <box>
              <size>{CELL_SIZE / 100} {CELL_SIZE / 100} 0.1</size>
            </box>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <box>
              <size>{CELL_SIZE / 100} {CELL_SIZE / 100} 0.1</size>
            </box>
          </geometry>
          <material>
            <script>
              <uri>file://media/materials/scripts/gazebo.material</uri>
              <name>Gazebo/Grey</name>
            </script>
          </material>
        </visual>
      </link>
      <pose>{x * CELL_SIZE / 100} {y * CELL_SIZE / 100} 0 0 0 0</pose>
    </model>
"""

sdf_content += """
  </world>
</sdf>
"""

# Save the SDF content to a file
with open("maze_world.sdf", "w") as sdf_file:
    sdf_file.write(sdf_content)

# Visualization using Pygame
screen = pygame.display.set_mode((WIDTH * CELL_SIZE, HEIGHT * CELL_SIZE))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill(WHITE)

    for y in range(HEIGHT):
        for x in range(WIDTH):
            if maze[y][x] == 1:
                pygame.draw.rect(screen, BLACK, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    pygame.display.flip()

