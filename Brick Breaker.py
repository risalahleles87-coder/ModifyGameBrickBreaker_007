import pygame
import random
import math

pygame.init()
pygame.mixer.init()

# Dimensions of the screen
WIDTH, HEIGHT = 600, 500

# Colors - Palette Pastel Gelato Days + Background Krem Lembut
BG_CREAM = (248, 243, 238)
WHITE = (255, 255, 255)
TEXT_DARK = (85, 70, 75)

PINK_PASTEL = (255, 203, 225)   # #FFCBE1
GREEN_PASTEL = (214, 229, 189)  # #D6E5BD
YELLOW_PASTEL = (249, 225, 168) # #F9E1A8
BLUE_PASTEL = (188, 216, 236)   # #BCD8EC
PURPLE_PASTEL = (220, 204, 236) # #DCCCEC
ORANGE_PASTEL = (255, 218, 180) # #FFDAB4
YELLOW_BALL = (255, 215, 70)
MINT_POWERUP = (140, 220, 180)

PASTEL_COLORS = [
    PINK_PASTEL,
    GREEN_PASTEL,
    YELLOW_PASTEL,
    BLUE_PASTEL,
    PURPLE_PASTEL,
    ORANGE_PASTEL,
]

font = pygame.font.Font('freesansbold.ttf', 11)
ui_font = pygame.font.Font('freesansbold.ttf', 14)
title_font = pygame.font.Font('freesansbold.ttf', 18)
game_over_font = pygame.font.Font('freesansbold.ttf', 24)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brick Breaker - Candy Rush")

clock = pygame.time.Clock()
FPS = 60


