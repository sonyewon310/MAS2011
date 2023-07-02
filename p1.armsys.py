import pygame
import numpy as np

WINDOW_WIDTH = 1300
WINDOW_HEIGHT = 750

GREEN = (100, 200, 100)

pygame.init()
pygame.display.set_caption("20191106 손예원 P1. Arm System")
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

def getRectangle(width, height, x=0, y=0):
    points = np.array([ [0, 0], 
                        [width, 0], 
                        [width, height], 
                        [0, height]], dtype='float')
    points = points + [x, y]
  
    return points

def Rmat(degree):
    radian = np.deg2rad(degree)
    c = np.cos(radian)
    s = np.sin(radian)
    R = np.array([ [c, -s, 0], 
                   [s, c, 0], 
                   [0, 0, 1]], dtype='float')
    return R 

def Tmat(tx, ty):
    T = np.array([ [1, 0, tx], 
                   [0, 1, ty], 
                   [0, 0, 1]], dtype='float')
    return T 

def draw(M, points, color=(255,255,0), p0=None):
    R = M[0:2, 0:2]
    t = M[0:2, 2]

    points_transformed = (R @ points.T).T + t
    pygame.draw.polygon(screen, color, points_transformed, 4)
    if p0 is not None:
        pygame.draw.line(screen, color, p0, points_transformed[0])

center1 = [150, 200.]

angle1 = 20
width1 = 300
height1 = 100
rect1 = getRectangle(width1, height1)
gap12 = 30

angle2 = 0
width2 = 280
height2 = 70
rect2= getRectangle(width2, height2)
gap23 = 20

angle3 = 0
width3 = 260
height3 = 40
rect3 = getRectangle(width3, height3)
gap34 = 10

#gripper
angle4 = 0
width4 = 15
height4 = 35
rect4 = getRectangle(width4, height4)
gap45 = 20

#hand1
angle5 = 180
width5 = 20
height5 = 12
rect5 = getRectangle(width5, height5)

#hand2
angle6 = 0
width6 = 20
height6 = 12
rect6 = getRectangle(width6, height6)


angle = 0
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
            elif event.key == pygame.K_a:
                angle1 += 5
            elif event.key == pygame.K_b:
                angle1 -= 5
            elif event.key == pygame.K_c:
                angle2 += 5
            elif event.key == pygame.K_d:
                angle2 -= 5
            elif event.key == pygame.K_e:
                angle3 += 5
            elif event.key == pygame.K_f:
                angle3 -= 5 
            elif event.key == pygame.K_SPACE:
                Hand1 @ Tmat(10, 0) @ Tmat(0, 10) @ Tmat(10, 0) @ Rmat(0) @ Tmat(0, 10)
                Hand2 @ Tmat(-10, 0) @ Tmat(0, -10) @ Tmat(-10, 0) @ Rmat(0) @ Tmat(0, -10)
    
    screen.fill(GREEN)
    cent = (400, 400)

    M1 = np.eye(3) @ Tmat(center1[0], center1[1]) @ Rmat(angle1) @ Tmat(0, -height1/2.)
    draw(M1, rect1, (255, 0, 0)) 
    M2 = M1 @ Tmat(width1, 0) @ Tmat(0, height1/2.) @ Tmat(gap12, 0) @ Rmat(angle2) @ Tmat(0, -height2/2.)
    draw(M2, rect2, (255, 255, 0)) 
    M3 = M2 @Tmat(width2, 0) @ Tmat(0, height2/2.) @ Tmat(gap23, 0) @ Rmat(angle3) @ Tmat(0, -height3/2.)
    draw(M3, rect3, (0, 0, 255)) 
    Gripper = M3 @Tmat(width3, 0) @ Tmat(0, height3/2.) @ Tmat(gap34, 0) @ Rmat(angle4) @ Tmat(0, -height4/2.)
    draw(Gripper, rect4, (255, 255, 255))
    Hand1 = Gripper @Tmat(width4, 0) @ Tmat(0, height4/2.) @ Tmat(gap45, 0) @ Rmat(angle5) @ Tmat(0, height5/2.)
    draw(Hand1, rect5, (255, 255, 255))
    Hand2 = Hand1 @ Tmat(0, 0) @ Tmat(0, height4/2.) @ Tmat(0, -height4) @ Rmat(angle6) @ Tmat(0, -height6/2.)
    draw(Hand2, rect6, (255, 255, 255))

    pygame.draw.circle(screen, (0,0,0), center1, 4)

    C = M1 @ Tmat(width1, 0) @ Tmat(0, height1/2.)
    center2 = C[0:2, 2]
    pygame.draw.circle(screen, (0,0,0), center2, 5)
    C2 = C @ Tmat(gap12, 0)
    center3 = C2[0:2, 2]
    pygame.draw.circle(screen, (0,0,0), center3, 5)
    C3 = C2 @ Tmat(width2, 0)
    center4 = C3[0:2, 2]
    pygame.draw.circle(screen, (0,0,0), center4, 5)
    C4 = C3 @ Tmat(gap23, 0)
    center5 = C4[0:2, 2]
    pygame.draw.circle(screen, (0,0,0), center5, 5)
    C5 = C4 @ Tmat(width3, 0)
    center6 = C5[0:2, 2]
    pygame.draw.circle(screen, (0,0,0), center6, 10)

    pygame.draw.line(screen, (0,0,0), center2, center3, 1)
    pygame.draw.line(screen, (0,0,0), center4, center5, 1)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

