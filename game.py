# Import necessary libraries
import random
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from math import cos, sin, pi
import time

# Initialize variables for day/night
toggle_timer = time.time()
is_daytime = True

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Camera position
camera_x = 5
camera_y = 5
camera_z = 10

# camera movement
camera_speed = 0.2
yaw = 0
pitch = 0

# Light properties
light_position = (50, 5, 10)
light_ambient = (1.2, 1.2, 1.2, 10.0)
light_diffuse = (1.0, 1.0, 1.0, 1.0)


# Player properties
arm_angle = 0
leg_angle = 0
arm_direction = 1
leg_direction = 1
isPlayer = True
player_x = 0
player_y = 1  # height of the player above the ground
player_z = 5
player_speed = 0.2
is_player_animated = False


# Car properties
car_x = 4
car_z = 0.5
car_speed = 0.1
wheel_rotation = 0
front_wheel_rotation = 0
car_rotation=0

# Clouds and stars initialization
clouds = []
stars=[]

# to handle special key events  
def handle_special_key(key, x, y):
    global camera_x, camera_y, camera_z

    if key == GLUT_KEY_UP:
        camera_z -= camera_speed
    elif key == GLUT_KEY_DOWN:
        camera_z += camera_speed
    elif key == GLUT_KEY_LEFT:
        camera_x -= camera_speed
    elif key == GLUT_KEY_RIGHT:
        camera_x += camera_speed

    glutPostRedisplay()

# to handle regular key events
def handle_key(key, x, y):
    global player_x, player_z, is_player_animated, front_wheel_rotation, car_speed, isPlayer, car_rotation
    if key==b' ':
        isPlayer = not isPlayer
    if(isPlayer):
        if key == b'w':
            is_player_animated = True
            player_z -= player_speed * cos(yaw)
            player_x += player_speed * sin(yaw)
        elif key == b's':
            is_player_animated = True
            player_z += player_speed * cos(yaw)
            player_x -= player_speed * sin(yaw)
        elif key == b'a':
            is_player_animated = True
            player_x -= player_speed * cos(yaw)
            player_z -= player_speed * sin(yaw)
        elif key == b'd':
            is_player_animated = True
            player_x += player_speed * cos(yaw)
            player_z += player_speed * sin(yaw)
    else:
        if key == b'w':
            update_car(False)
            if(front_wheel_rotation!=0 and front_wheel_rotation<0):
                front_wheel_rotation+=15
            elif(front_wheel_rotation!=0 and front_wheel_rotation>0):
                front_wheel_rotation-=15
        elif key == b's':
            update_car(True)
            if(front_wheel_rotation!=0 and front_wheel_rotation<0):
                front_wheel_rotation+=15
            elif(front_wheel_rotation!=0 and front_wheel_rotation>0):
                front_wheel_rotation-=15
        elif key == b'a':
            if (front_wheel_rotation<=45):
                front_wheel_rotation += 15
            car_rotation+=15/50
        elif key == b'd':
            if(front_wheel_rotation>=-45):
                front_wheel_rotation -= 15
            car_rotation-=15/50
    glutPostRedisplay()

# to handle key release events
def handle_key_up(key, x, y):
    global is_player_animated
    is_player_animated = False

# to handle mouse events
def handle_mouse(button, state, x, y):
    # handle mouse interaction (rotation and player movement)
    global yaw, pitch
    global player_x, player_z

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        glutSetCursor(GLUT_CURSOR_NONE)
        glutWarpPointer(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
    elif button == GLUT_LEFT_BUTTON and state == GLUT_UP:
        glutSetCursor(GLUT_CURSOR_INHERIT)
        glutPostRedisplay()

# to handle mouse motion
def handle_motion(x, y):
    # update yaw and pitch based on mouse movement
    global yaw, pitch
    yaw += (x - WINDOW_WIDTH // 2) * 0.1
    pitch += (y - WINDOW_HEIGHT // 2) * 0.1
    glutWarpPointer(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
    glutPostRedisplay()

# to draw a cube
def draw_cube(x, y, z, width, height, depth, color):
    glColor3f(*color)
    vertices = [
        (x, y, z), (x + width, y, z), (x + width, y + height, z), (x, y + height, z),
        (x, y, z - depth), (x, y + height, z - depth), (x + width, y + height, z - depth), (x + width, y, z - depth)
    ]
    indices = [
        (0, 1, 2, 3), (4, 5, 6, 7), (0, 3, 5, 4), (1, 2, 6, 7), (0, 1, 7, 4), (2, 3, 5, 6)
    ]

    glBegin(GL_QUADS)
    for index in indices:
        for vertex_index in index:
            glVertex3f(*vertices[vertex_index])
    glEnd()

# to draw a sphere
def draw_sphere(x, y, z, radius, color):
    glColor3f(*color)
    sides = 30
    rings = 30
    glBegin(GL_QUADS)
    for i in range(rings + 1):
        theta1 = i * pi / rings
        theta2 = (i + 1) * pi / rings
        for j in range(sides + 1):
            phi1 = j * 2.0 * pi / sides
            phi2 = (j + 1) * 2.0 * pi / sides
            x1 = x + radius * sin(theta1) * cos(phi1)
            y1 = y + radius * sin(theta1) * sin(phi1)
            z1 = z + radius * cos(theta1)
            x2 = x + radius * sin(theta1) * cos(phi2)
            y2 = y + radius * sin(theta1) * sin(phi2)
            z2 = z + radius * cos(theta1)
            x3 = x + radius * sin(theta2) * cos(phi2)
            y3 = y + radius * sin(theta2) * sin(phi2)
            z3 = z + radius * cos(theta2)
            x4 = x + radius * sin(theta2) * cos(phi1)
            y4 = y + radius * sin(theta2) * sin(phi1)
            z4 = z + radius * cos(theta2)
            glVertex3f(x1, y1, z1)
            glVertex3f(x2, y2, z2)
            glVertex3f(x3, y3, z3)
            glVertex3f(x4, y4, z4)
    glEnd()

# to draw the ground
def draw_ground():
    glColor3f(0.2, 0.8, 0.2)  # Green color for the ground
    glBegin(GL_QUADS)
    glVertex3f(-100, 0, -100)
    glVertex3f(100, 0, -100)
    glVertex3f(100, 0, 100)
    glVertex3f(-100, 0, 100)
    glEnd()

# to generate stars
def generate_stars():
    global stars
    while len(stars)<20:
        x = random.uniform(-10, 10)
        y = random.uniform(5, 15)
        z = random.uniform(-10, 10)
        stars.append((x, y, z))

# to generate clouds
def generate_clouds():
    global clouds
    while len(clouds)<11:
        x = random.uniform(-10, 10)
        y = random.uniform(8, 12)
        z = random.uniform(-10, 10)
        clouds.append((x, y, z))

# to draw stars
def draw_stars():
    global stars
    generate_stars()
    glColor3f(1.0, 1.0, 1.0)
    for star in stars:
        draw_sphere(star[0], star[1], star[2], radius=0.05, color=(1.0, 1.0, 1.0))

# to draw clouds
def draw_clouds():
    global clouds
    generate_clouds()
    glColor4f(1.0, 1.0, 1.0, 0.1)  # Semi-transparent white for clouds
    for cloud in clouds:
        draw_sphere(cloud[0], cloud[1], cloud[2], radius=1.5, color=(0.9, 0.9, 0.9))

# to draw the car
def draw_car():
    global car_x, car_z, wheel_rotation, front_wheel_rotation,car_rotation

    # Draw car body
    glRotatef(car_rotation, 0, 1, 0)
    draw_cube(car_x-0.7, 0.5, car_z+0.3, 1.5, 0.5, 0.8, color=(0.5, 0.5, 0.5))
    glShadeModel(GL_FLAT)

    # Draw front LEDs (white)
    draw_cube(car_x + 0.8, 0.6, car_z + 0.2, 0.05, 0.05, 0.05, color=(1.0, 1.0, 1.0))  # White LED
    draw_cube(car_x + 0.8, 0.6, car_z - 0.2, 0.05, 0.05, 0.05, color=(1.0, 1.0, 1.0))  # White LED

    # Draw rear LEDs (red)
    draw_cube(car_x - 0.75, 0.6, car_z + 0.2, 0.05, 0.05, 0.05, color=(1.0, 0.0, 0.0))  # Red LED
    draw_cube(car_x - 0.75, 0.6, car_z - 0.2, 0.05, 0.05, 0.05, color=(1.0, 0.0, 0.0))  # Red LED

    
    # Draw wheels with clear division between black and white halves
    wheel_radius = 0.25
    wheel_thickness = 0.1

    def draw_half_torus(x, y, z, rotation_height, rotation_width, color1, color2):
        glPushMatrix()
        glTranslatef(x, y, z)
        glRotatef(rotation_height, 0, 0, 1)  # Rotate around the height axis
        glRotatef(rotation_width, 1, 1, 0)  # Rotate around the width axis

        # Draw black half
        glColor3f(*color1)
        glutSolidTorus(wheel_thickness, wheel_radius, 20, 20)

        # Draw white half
        glColor3f(*color2)
        glRotated(180, 0, 0, 1)
        glutSolidTorus(wheel_thickness, wheel_radius, 20, 20)

        glPopMatrix()

     # Draw rear left wheel
    draw_half_torus(car_x - 0.6, 0.25, car_z + 0.4, wheel_rotation, 0, (0, 0, 0), (1, 1, 1))

    # Draw front right wheel with rotation
    draw_half_torus(car_x + 0.6, 0.25, car_z + 0.4, wheel_rotation, front_wheel_rotation, (0, 0, 0), (1, 1, 1))

    # Draw rear left wheel
    draw_half_torus(car_x - 0.6, 0.25, car_z - 0.5, wheel_rotation, 0, (0, 0, 0), (1, 1, 1))

    # Draw front right wheel with rotation
    draw_half_torus(car_x + 0.6, 0.25, car_z - 0.5, wheel_rotation, front_wheel_rotation, (0, 0, 0), (1, 1, 1))

# to draw a cone on a cube
def draw_cone_on_cube(cube_x, cube_y, cube_z, cube_width, cube_height, cube_depth, cone_radius, cone_height, color):
    cone_x = cube_x + cube_width / 2
    cone_y = cube_y + cube_height
    cone_z = cube_z + cube_depth / 2 + cone_height / 2  # Adjust the cone position

    glColor3f(*color)
    glPushMatrix()
    glTranslatef(cone_x, cone_y, cone_z)
    glRotatef(-90, 1, 0, 0)  # Rotate 180 degrees around the X-axis
    glutSolidCone(cone_radius, cone_height, 30, 30)
    glPopMatrix()

# to draw the sun
def draw_sun(x, y, z, radius):
    draw_sphere(x, y, z, radius, color=(1.0, 1.0, 0.0))

# to draw the moon
def draw_moon(x, y, z, radius):
    draw_sphere(x, y, z, radius, color=(0.8, 0.8, 0.8))

# to draw the player
def draw_player():
    global player_x, player_y, player_z, arm_angle, leg_angle, arm_direction, leg_direction

    # Draw head with eyes and mouth
    draw_sphere(player_x, player_y + 0.5, player_z - 0.1, radius=0.1, color=(1.0, 0.0, 0.0))
    glShadeModel(GL_FLAT)

    # Draw eyes
    glColor3f(0.0, 0.0, 0.0)
    draw_sphere(player_x - 0.03, player_y + 0.52, player_z , radius=0.02, color=(0.0, 0.0, 0.0))
    draw_sphere(player_x + 0.03, player_y + 0.52, player_z , radius=0.02, color=(0.0, 0.0, 0.0))

    # Draw mouth
    glColor3f(0.0, 0.0, 0.0)
    glBegin(GL_LINES)
    glVertex3f(player_x - 0.03, player_y + 0.48, player_z)
    glVertex3f(player_x + 0.03, player_y + 0.48, player_z)
    glEnd()

    # Draw body
    draw_cube(player_x - 0.1, player_y, player_z - 0.05, 0.2, 0.4, 0.1, color=(0.0, 1.0, 1.0))
    if is_player_animated:
        arm_angle += arm_direction * 5  # Adjust the speed of arm movement
        if arm_angle > 30 or arm_angle < -30:
            arm_direction *= -1

    # Draw arms with animation
    draw_cube(player_x - 0.25, player_y + 0.3, player_z, 0.05, 0.05, 0.2, color=(0.0, 0.0, 1.0))
    glPushMatrix()
    glTranslatef(player_x - 0.25, player_y + 0.3, player_z)
    glRotatef(arm_angle, 1, 0, 0)
    draw_cube(0, 0, 0, 0.05, 0.2, 0.05, color=(0.0, 0.0, 1.0))
    glPopMatrix()

    draw_cube(player_x + 0.2, player_y + 0.3, player_z, 0.05, 0.05, 0.2, color=(0.0, 0.0, 1.0))
    glPushMatrix()
    glTranslatef(player_x + 0.2, player_y + 0.3, player_z)
    glRotatef(-arm_angle, 1, 0, 0)
    draw_cube(0, 0, 0, 0.05, 0.2, 0.05, color=(0.0, 0.0, 1.0))
    glPopMatrix()

    # Animate legs
    if is_player_animated:
        leg_angle += leg_direction * 5  # Adjust the speed of leg movement
        if leg_angle > 30 or leg_angle < -30:
            leg_direction *= -1

    # Draw legs with animation
    draw_cube(player_x - 0.1, player_y - 0.5, player_z - 0.05, 0.1, 0.5, 0.1, color=(1.0, 1.0, 0.0))
    glPushMatrix()
    glTranslatef(player_x - 0.1, player_y - 0.5, player_z)
    glRotatef(leg_angle, 1, 0, 0)

    # Draw legs with feet
    draw_cube(0, 0, 0, 0.1, 0.1, 0.1, color=(1.0, 1.0, 0.0))  # Lower leg
    glTranslatef(0, -0.1, 0)  # Move to the feet position
    draw_cube(0, 0, 0, 0.1, 0.1, 0.1, color=(1.0, 1.0, 1.0))  # Feet
    glPopMatrix()

    draw_cube(player_x, player_y - 0.5, player_z - 0.05, 0.1, 0.5, 0.1, color=(1.0, 1.0, 0.0))
    glPushMatrix()
    glTranslatef(player_x, player_y - 0.5, player_z)
    glRotatef(-leg_angle, 1, 0, 0)

    # Draw legs with feet
    draw_cube(0, 0, 0, 0.1, 0.1, 0.1, color=(1.0, 1.0, 0.0))  # Lower leg
    glTranslatef(0, -0.1, 0)  # Move to the feet position
    draw_cube(0, 0, 0, 0.1, 0.1, 0.1, color=(1.0, 1.0, 1.0))  # Feet
    glPopMatrix()



# to update and draw the scene
def draw_scene():
    global is_daytime, light_ambient
    # glColor3f(0.529, 0.808, 0.922)
    if is_daytime:
        glClearColor(0.529, 0.808, 0.922, 1.0)  # Set clear color toblue as sky color
        light_ambient=(1.2, 1.2, 1.2, 10.0)
    else:
        glClearColor(0.0, 0.0, 0.0, 1.0)
        light_ambient=(.2, .2, .2, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    draw_ground()

    if is_daytime:
        draw_sun(-8, 12, -5, 1)
        # Add clouds for daytime
        draw_clouds()
    else:
        draw_moon(-8, 12, -5, 1)
        # Add stars for nighttime
        draw_stars()

    # Draw house
    draw_cube(0, 0, 0, 2, 2, 2, color=(0.8, 0.6, 0.4))

    # Draw roof (cone on top of the cube)
    draw_cone_on_cube(0, 0, -2.2, 2, 2, 1, 1.5, 1.5, color=(0.3, 0.3, 0.8))

    # Draw door
    draw_cube(1, 0, .005, 0.4, 1, 0.05, color=(1, 0, 0))

    # Draw window
    draw_cube(2, .5, -1, 0.05, .5, 0.5, color=(0.8, 0.8, 1))

    # Draw window
    draw_cube(0.2, 0.5, .005, 0.6, 0.3, 0.05, color=(0.8, 0.8, 1))

    # draw soba
    draw_cube(1.8, 2.2, -0.6, 0.3, .8, 0.3, color=(0.8, 0.8, 1))

    # Draw player (smaller size)
    draw_player()

# to set up lighting
def setup_lighting():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)

# to update car position
def update_car(back):
    global car_x, car_speed, wheel_rotation
    if(back==True):
        car_x -= car_speed
    else:
        car_x += car_speed

    # Update wheel rotation
    wheel_rotation += (360 * car_speed) / (2 * pi * 0.25)  # circumference = 2 * pi * radius

# to display the scene
def display():
    global toggle_timer, is_daytime
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluPerspective(45, (WINDOW_WIDTH / WINDOW_HEIGHT), 0.1, 50.0)
    gluLookAt(camera_x, camera_y, camera_z,
              camera_x + 10 * sin(yaw), camera_y + 10 * sin(pitch), camera_z - 10 * cos(yaw),
              0, 1, 0)

    setup_lighting()

    if time.time() - toggle_timer > 10:
        is_daytime = not is_daytime  # Toggle the day/night cycle
        toggle_timer = time.time()  # Reset the timer


    draw_scene()

    # Draw the car
    draw_car()

    glutSwapBuffers()

# Initialize OpenGL and register callback functions
glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
glutInitWindowPosition(0, 0)
glutCreateWindow(b'Mini project')
glEnable(GL_DEPTH_TEST)
glEnable(GL_COLOR_MATERIAL)
glEnable(GL_NORMALIZE)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
# glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)

# Register callback functions for keyboard and mouse input
glutKeyboardFunc(handle_key)
glutSpecialFunc(handle_special_key)
glutKeyboardUpFunc(handle_key_up)
glutMouseFunc(handle_mouse)
glutMotionFunc(handle_motion)
glutDisplayFunc(display)
glutIdleFunc(display)

# Main event loop
glutMainLoop()
