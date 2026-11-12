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


# Fungsi efek suara lucu
def play_cute_sound(start_freq, end_freq, duration_ms, wave_type="sine"):
    try:
        sample_rate = 22050
        num_samples = int(sample_rate * (duration_ms / 1000.0))
        buffer = bytearray()
        phase = 0.0

        for i in range(num_samples):
            progress = i / num_samples
            current_freq = start_freq + (end_freq - start_freq) * progress
            envelope = (1.0 - progress) ** 1.5

            phase += 2 * math.pi * current_freq / sample_rate
            if wave_type == "triangle":
                raw = 2.0 * abs(2.0 * ((phase / (2 * math.pi)) % 1.0) - 1.0) - 1.0
            else:
                raw = math.sin(phase)

            value = int(32767 * 0.45 * envelope * raw)
            buffer += value.to_bytes(2, byteorder='little', signed=True)

        sound = pygame.mixer.Sound(buffer=buffer)
        sound.set_volume(0.35)
        sound.play()
    except Exception:
        pass


def sound_boing():
    play_cute_sound(300, 750, 90, "sine")


def sound_pop():
    play_cute_sound(550, 1100, 75, "triangle")


def sound_powerup():
    play_cute_sound(600, 1200, 110, "sine")


def sound_wall():
    play_cute_sound(420, 520, 45, "sine")


def sound_oops():
    play_cute_sound(500, 180, 220, "triangle")


def sound_level_up():
    play_cute_sound(523, 659, 100, "triangle")
    pygame.time.delay(80)
    play_cute_sound(659, 1046, 160, "triangle")


def sound_game_over():
    play_cute_sound(380, 320, 140, "triangle")
    pygame.time.delay(130)
    play_cute_sound(320, 260, 140, "triangle")
    pygame.time.delay(130)
    play_cute_sound(260, 140, 320, "triangle")


# Striker / Papan Pemantul Bawah
class Striker:
    def __init__(self, posx, posy, width, height, speed, color):
        self.posx, self.posy = posx, posy
        self.width, self.height = width, height
        self.speed = speed
        self.color = color

        self.strikerRect = pygame.Rect(self.posx, self.posy, self.width, self.height)

    def display(self):
        pygame.draw.rect(screen, self.color, self.strikerRect, border_radius=8)
        pygame.draw.rect(screen, TEXT_DARK, self.strikerRect, 2, border_radius=8)

    def update(self, xFac):
        self.posx += self.speed * xFac
        if self.posx <= 0:
            self.posx = 0
        elif self.posx + self.width >= WIDTH:
            self.posx = WIDTH - self.width
        self.strikerRect = pygame.Rect(self.posx, self.posy, self.width, self.height)

    def getRect(self):
        return self.strikerRect


