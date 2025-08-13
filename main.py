import cv2
import mediapipe as mp
import pygame
import numpy as np
import random
from merge import merger
from gravitation import gravity
from vision import gesture

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
hand = mp.solutions.hands.Hands(max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

pygame.init()

width = 1500
height = 1000
world_width = 3000
world_height = 2000

masslim = 30
dt = 0.1
G = 1
c = 3e8
theta = 0.5

camera_x = 0
camera_y = 0
camera_zoom = 1
camera_speed = 10
zoom_speed = 0.05

mingenrad = 2
maxgenrad = 5

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Stars")

class Particle():
    def __init__(self, x, y, density, radius, color, elasticity):
        self.x = x
        self.y = y
        self.density = density
        self.radius = radius
        self.mass = density * (4/3) * np.pi * radius ** 3
        self.color = color
        self.elasticity = elasticity

        self.x_vel = 0
        self.y_vel = 0
    
    def display(self, camx, camy, zoom):
        screen_x = (self.x - camx) * zoom
        screen_y = (self.y - camy) * zoom
        if self.radius + screen_x < width and self.radius + screen_y < height and screen_x > 0 and screen_y > 0:
            pygame.draw.circle(screen, self.color, (int(screen_x), int(screen_y)), int(self.radius * zoom))

my_particles = []
existing = []
for i in range(1000):
    x = random.randint(0, width)
    y = random.randint(0, height)
    if (x, y) not in existing:
        my_particles.append(Particle(x, y, random.randint(1, 10)/1000, random.randint(mingenrad, maxgenrad), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), random.randint(0, 10)/10))
        my_particles[-1].x_vel = random.uniform(-1, 1)
        my_particles[-1].y_vel = random.uniform(-1, 1)
        for i in [-5 + j for j in range(11)]:
            existing.append((x + i, y + i))
existing.clear()

clock = pygame.time.Clock()

pause = False
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    success, frame = cap.read()
    if success:
        RGB_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hand.process(RGB_frame)
        if result.multi_hand_landmarks:
            pause = True
            for hand_landmarks in result.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS)
                current = gesture(hand_landmarks.landmark)
                if current == "all":
                    if camera_zoom < 5:
                        camera_zoom += zoom_speed
                elif current == "thumb":
                    if camera_x > 0:
                        camera_x -= camera_speed
                elif current == "index":
                    if camera_y > 0:
                        camera_y -= camera_speed
                elif current == "out":
                    if camera_y < world_height - (height/camera_zoom):
                        camera_y += camera_speed
                elif current == "pinky":
                    if camera_x < world_width - (width/camera_zoom):
                        camera_x += camera_speed
                elif current == "middle":
                    if camera_zoom > width/world_width:
                        camera_zoom -= zoom_speed
        else:
            pause = 0
        cv2.imshow("capture image", frame)
        if cv2.waitKey(1) == ord('q'):
            running = False
    else:
        print("camera boom") #Not printing despite the camera showing only black screen...
    
    screen.fill((0, 0, 0))

    if not pause:
        gravity(my_particles, G, dt, theta)
        my_particles = merger(my_particles, G, masslim, c)

    for p in my_particles:
        p.display(camera_x, camera_y, camera_zoom)

    pygame.display.update() 
    clock.tick(120)

pygame.quit()