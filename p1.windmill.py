import pygame
import numpy as np

WINDOW_WIDTH = 700
WINDOW_HEIGHT = 700

WHITE = (255, 255, 255)
BackGround = (204, 255, 204)

pygame.init()
pygame.display.set_caption("20191106 손예원 Own Creation_Pinwheel")
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()


def getRegularPolygon(N, radius=1):
    v = np.zeros((N, 2))
    for i in range(N):
        deg = i * 360. / N
        rad = deg * np.pi / 180.
        x = radius * np.cos(rad)
        y = radius * np.sin(rad)
        v[i] = [x, y]
    return v

def getRectangle(width, height, x=0, y=0):
    points = np.array([[0, 0], [width,0], [width,height], [0,height]], dtype='float')
    points = points + [x, y]
    return points

def Rmat(degree):
    radian = np.deg2rad(degree)
    c = np.cos(radian)
    s = np.sin(radian)
    R = np.array([[c, -s, 0],
                  [s, c, 0],
                  [0, 0, 1]], dtype='float')
    return R

def Tmat(tx, ty):
    T = np.array([[1, 0, tx],
                  [0, 1, ty],
                  [0, 0, 1]], dtype='float')
    return T

def draw(M, points, color=(0,0,0), p0=None):
    R = M[0:2, 0:2]
    t = M[0:2, 2]

    points_transformed = (R @ points.T).T + t
    pygame.draw.polygon(screen, color , points_transformed, 10)
    if p0 is not None:
        pygame.draw.line(screen, (0,0,0), p0, points_transformed[0])

center1 = [100, 500.]
angle = 0
width1 = 300
height1 = 100
height2 = 70
height3 = 150
rect1 = getRectangle(width1, height1)
gap12 = 30

done = False
while not done:
    angle += 3
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                    done = True

    screen.fill(BackGround)

    center=(WINDOW_WIDTH/2., WINDOW_HEIGHT/2.)
    M = Tmat(center[0], center[1]) @ Tmat(0, -height1/2.)
    draw(M, rect1, (0,0,0))
    M1 = M @ Tmat(0, height1/2.) @ Rmat(angle) @ Tmat(0, -height1/2.)
    draw(M1, rect1, (0,0,0))
    M2 = M1 @ Tmat(0, height1/2.) @ Rmat(70) @ Tmat(0, -height1/2.)
    draw(M1, rect1, (0,0,255))
    M3 = M2 @ Tmat(0, height1/2.) @ Rmat(70) @ Tmat(0, -height1/2.)
    draw(M3, rect1, (255,0,0))
    M4 = M3 @ Tmat(0, height1/2.) @ Rmat(70) @ Tmat(0, -height1/2.)
    draw(M4, rect1, (0,255,255))
    M5 = M4 @ Tmat(0, height1/2.) @ Rmat(70) @ Tmat(0, -height1/2.)
    draw(M5, rect1, (255,255,0))
    M6 = M1 @ Tmat(0, height1/2.) @ Rmat(70) @ Tmat(0, -height1/2.)
    draw(M6, rect1, (255,0,255))

    pygame.draw.circle(screen, WHITE, center, 20)
   


    pygame.display.flip()
    clock.tick(60)

pygame.quit()

