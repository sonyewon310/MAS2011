import pygame
import numpy as np

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 770

BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PINK = (252, 186, 203)
SKYBLUE = (0, 255, 255)
GREEN = (0, 255, 0)

clr = np.random.randint(0, 256, size=3)

pygame.init()
pygame.display.set_caption("20191106 손예원 P1. Solar system")
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

def getRegularPolygon(N, radius=1):
    v = np.zeros((N,2))
    for i in range(N):
        deg = i * 360. / N
        rad = deg * np.pi / 180.
        x = radius * np.cos(rad)
        y = radius * np.sin(rad)
        v[i] = [x, y]
    return v

def Rmat(degree):
    radian = np.deg2rad(degree)
    c = np.cos(radian)
    s = np.sin(radian)
    R = np.array([[c, -s, 0],
                  [s, c, 0],
                  [0, 0, 1]], dtype='float')
    return R

def Tmat(tx, ty):
    T = np.array([ [1, 0, tx], 
                   [0, 1, ty], 
                   [0, 0, 1]], dtype='float')
    return T 

def getRectangle(width, height, x=0, y=0):
    points = np.array([ [0, 0], 
                        [width, 0], 
                        [width, height], 
                        [0, height]], dtype='float')
    points = points + [x, y]
    return points

def draw(M, points, color=(255,255,0), p0=None):
    R = M[0:2, 0:2]
    t = M[0:2, 2]

    points_transformed = (R @ points.T).T + t
    pygame.draw.polygon(screen, color, points_transformed, 3)
    if p0 is not None:
        pygame.draw.line(screen, color, p0, points_transformed[0])



Sun = getRegularPolygon(20, 50)
distSE = 150
Earth = getRegularPolygon(10, 20)
distEM = 50
Moon = getRegularPolygon(4, 5)
PlanetA = getRegularPolygon(10, 30)
distSA = 300
A_moon1 = getRegularPolygon(5, 10)
distA1 =100
A_moon2 = getRegularPolygon(5, 5)
distA2 = 50
A_moon1_1 = getRegularPolygon(3, 3)
distA1_1 = 20

angle = 0
angleSE = 0
angleE = 0
angleM = 0
angleEM = 0
angleA = 0
angleSA = 0
angle1 = 0
angleA1 = 0
angle2 = 0
angleA2 = 0
angle1_1 = 0
angleA1_1 = 0

spaceship = getRegularPolygon(4, 20)
spaceship_circle = [getRegularPolygon(3, 5), getRegularPolygon(10, 9)]

spaceship_pos = np.array([np.random.randint(0, WINDOW_WIDTH - 20 ),
                          np.random.randint(0, WINDOW_HEIGHT - 20)])

movement_range = 3
spaceship_speed = 1

done = False
while not done:
    angle += 3
    angleSE += 1
    angleE += 5
    angleM += 7
    angleEM += 8
    angleA += 2
    angleSA += 1
    angle1 += 2
    angleA1 += 3
    angle2 += 2
    angleA2 += 4
    angle1_1 += 5
    angleA1_1 += 6
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True

    screen.fill(BLACK)

    center=(WINDOW_WIDTH/2., WINDOW_HEIGHT/2.)
    Msun = Tmat(center[0], center[1]) @ Rmat(angle)
    draw(Msun, Sun, RED, center)

    Mearth = Tmat(center[0], center[1]) @ Rmat(angleSE) @ Tmat(distSE, 0) @ Rmat(-angleSE) @ Rmat(angleE)
    draw(Mearth, Earth, BLUE, Mearth[:2,2])

    Mmoon = Mearth @ Rmat(angleEM) @ Tmat(distEM, 0) @ Rmat(angleM)
    draw(Mmoon, Moon, YELLOW, Mmoon[:2,2])

    MPlanetA = Tmat(center[0], center[1]) @ Rmat(angleSA) @ Tmat(distSA, 0) @ Rmat(-angleSA) @ Rmat(angleA)
    draw(MPlanetA, PlanetA, clr, MPlanetA[:2,2])

    MA_moon1 = MPlanetA @ Rmat(angleA1) @ Tmat(distA1, 0) @ Rmat(angle1)
    draw(MA_moon1, A_moon1, PINK , MA_moon1[:2,2])

    MA_moon2 = MPlanetA @ Rmat(angleA2) @ Tmat(distA2, 0) @ Rmat(angle2)
    draw(MA_moon2, A_moon2, SKYBLUE, MA_moon2[:2,2])

    MA_moon1_1 = MA_moon1 @ Rmat(angleA1_1) @ Tmat(distA1_1, 0) @ Rmat(angle1_1)
    draw(MA_moon1_1, A_moon1_1, WHITE, MA_moon1_1[:2,2])

    spaceship_movement = np.array([np.random.randint(-movement_range, movement_range),
                                   np.random.randint(-movement_range, movement_range)])
    spaceship_pos += spaceship_movement * spaceship_speed
    spaceship_pos = np.clip(spaceship_pos, [60, 60], [WINDOW_WIDTH - 20, WINDOW_HEIGHT - 20])
    Mspaceship = Tmat(spaceship_pos[0], spaceship_pos[1])
    draw(Mspaceship, spaceship, GREEN)
    for circle in spaceship_circle:
        draw(Mspaceship, circle, GREEN)

    pygame.display.flip()
    clock.tick(50)

pygame.quit()