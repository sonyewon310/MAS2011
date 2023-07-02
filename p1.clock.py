import pygame
import numpy as np
import time
import os

pygame.init()
clock = pygame.time.Clock()

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('20191106 손예원 P1. Clock')

clock_radius = 150
clock_center = (WINDOW_WIDTH/2., WINDOW_HEIGHT/2.)
hour_hand_length = 100
minute_hand_length = 140
second_hand_length = 180

current_path = os.path.dirname(__file__)
assets_path = os.path.join(current_path, 'assets')
ringing_sound = pygame.mixer.Sound(os.path.join(assets_path, 'ringing_sound.wav'))

WHITE = (255, 255, 255)
PINK = (255, 153, 204)
MINT = (51, 204, 204)
GREY = (150, 150, 150)
NAVY = (25, 25, 112)

color = np.random.randint(0, 256, size=3)


done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True


    screen.fill(PINK)

    current_time = time.gmtime()
    hours = current_time.tm_hour + 9
    minutes = current_time.tm_min
    seconds = current_time.tm_sec

    hour_angle = (360 / 12) * hours + (360 / (12 * 60)) * minutes
    minute_angle = (360 / 60) * minutes + (360 / (60 * 60)) * seconds
    second_angle = (360 / 60) * seconds

    hour_angle_rad = np.radians(-hour_angle + 90)
    minute_angle_rad = np.radians(-minute_angle + 90)
    second_angle_rad = np.radians(-second_angle + 90)

    hour_hand_pos = (
        int(clock_center[0] + hour_hand_length * np.cos(hour_angle_rad)),
        int(clock_center[1] - hour_hand_length * np.sin(hour_angle_rad)))
    minute_hand_pos = (
        int(clock_center[0] + minute_hand_length * np.cos(minute_angle_rad)),
        int(clock_center[1] - minute_hand_length * np.sin(minute_angle_rad)))
    second_hand_pos = (
        int(clock_center[0] + second_hand_length * np.cos(second_angle_rad)),
        int(clock_center[1] - second_hand_length * np.sin(second_angle_rad)))

    # Draw the clock hands
    pygame.draw.line(screen, MINT, clock_center, hour_hand_pos, 10)
    pygame.draw.line(screen, GREY, clock_center, minute_hand_pos, 7)
    pygame.draw.line(screen, NAVY, clock_center, second_hand_pos, 2)

    # Draw the clock center
    pygame.draw.circle(screen, WHITE, clock_center, 10)

    if minutes == 0 and seconds == 0:
         ringing_sound.play()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
