import pygame
import sys
import requests
import math
import numpy as np
from pygame.locals import *

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rotating Pyramid")

# Define colors for each face
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

# Define pyramid vertices
vertices = [
    (0, 1, 0),  # Apex
    (-1, -1, 1),  # Base vertices
    (1, -1, 1),
    (1, -1, -1),
    (-1, -1, -1)
]

# Define pyramid faces
faces = [
    (0, 1, 2),  # Front face
    (0, 2, 3),  # Right face
    (0, 3, 4),  # Back face
    (0, 4, 1),  # Left face
    (1, 2, 3, 4)  # Base face
]

# Flask endpoint URL
FLASK_ENDPOINT = "http://localhost:5000/get_orientation"

# Function to get orientation data from Flask server
def get_orientation_data():
    try:
        response = requests.get(FLASK_ENDPOINT)
        if response.status_code == 200:
            orientation_data = response.json().get('orientation')
            if orientation_data and all(key in orientation_data for key in ['pitch', 'roll', 'yaw']):
                return orientation_data
            else:
                print("Invalid orientation data format:", orientation_data)
        else:
            print("Failed to fetch orientation data:", response.status_code)
    except Exception as e:
        print("Error fetching orientation data:", e)
    return None

# Rotation matrix calculation function
def calculate_rotation_matrix(pitch, roll, yaw):
    rotation_matrix_x = [
        [1, 0, 0],
        [0, math.cos(pitch), -math.sin(pitch)],
        [0, math.sin(pitch), math.cos(pitch)]
    ]
    rotation_matrix_y = [
        [math.cos(roll), 0, math.sin(roll)],
        [0, 1, 0],
        [-math.sin(roll), 0, math.cos(roll)]
    ]
    rotation_matrix_z = [
        [math.cos(yaw), -math.sin(yaw), 0],
        [math.sin(yaw), math.cos(yaw), 0],
        [0, 0, 1]
    ]
    rotation_matrix = np.dot(rotation_matrix_z, np.dot(rotation_matrix_y, rotation_matrix_x))
    return rotation_matrix

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Clear the screen
    screen.fill((0, 0, 0))

    # Get orientation data from the server
    orientation_data = get_orientation_data()
    if orientation_data is not None:
        # Extract pitch, roll, and yaw from orientation data
        pitch = math.radians(orientation_data['pitch'])
        roll = math.radians(orientation_data['roll'])
        yaw = math.radians(orientation_data['yaw'])

        # Calculate rotation matrix
        rotation_matrix = calculate_rotation_matrix(pitch, roll, yaw)

        # Process vertices and apply rotation
        rotated_vertices = []
        for vertex in vertices:
            rotated_vertex = np.dot(rotation_matrix, vertex)
            rotated_vertices.append(rotated_vertex)

        # Draw pyramid faces with different colors
        for face_index, face in enumerate(faces):
            vertices_list = []
            for vertex_index in face:
                vertex = rotated_vertices[vertex_index]
                x = vertex[0] * 100 + WIDTH / 2
                y = vertex[1] * 100 + HEIGHT / 2
                vertices_list.append((x, y))
            # Assign a color to each face
            COLORS = [RED, GREEN, BLUE, YELLOW, CYAN]
            color = COLORS[face_index] if face_index < len(COLORS) else MAGENTA
            pygame.draw.polygon(screen, color, vertices_list)

    # Update display
    pygame.display.flip()
    pygame.time.Clock().tick(60)
