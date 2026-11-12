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


# PowerUp Class (Item +1 Bola)
class PowerUp:
    def __init__(self, posx, posy):
        self.posx = posx
        self.posy = posy
        self.radius = 12
        self.speed = 2.5

    def update(self):
        self.posy += self.speed

    def display(self):
        pygame.draw.circle(screen, MINT_POWERUP, (int(self.posx), int(self.posy)), self.radius)
        pygame.draw.circle(screen, WHITE, (int(self.posx), int(self.posy)), self.radius, 2)
        txt = font.render("+1", True, TEXT_DARK)
        screen.blit(txt, txt.get_rect(center=(int(self.posx), int(self.posy))))

    def getRect(self):
        return pygame.Rect(self.posx - self.radius, self.posy - self.radius, self.radius * 2, self.radius * 2)


# Block / Kotak Angka Kecil dan Padat ala Grid
class Block:
    def __init__(self, posx, posy, width, height, health, color):
        self.posx, self.posy = posx, posy
        self.width, self.height = width, height
        self.health = health
        self.color = color
        self.blockRect = pygame.Rect(self.posx, self.posy, self.width, self.height)

    def display(self):
        if self.health > 0:
            pygame.draw.rect(screen, self.color, self.blockRect, border_radius=2)
            pygame.draw.rect(screen, WHITE, self.blockRect, 1, border_radius=2)

            txt = font.render(str(self.health), True, TEXT_DARK)
            txt_rect = txt.get_rect(center=self.blockRect.center)
            screen.blit(txt, txt_rect)

    def hit(self):
        self.health -= 10
        self.color = random.choice(PASTEL_COLORS)

    def getRect(self):
        return self.blockRect

    def getHealth(self):
        return self.health


# Ball Class dengan Efek Jejak Pastel Smooth
class Ball:
    def __init__(self, posx, posy, radius, speed, color, xFac=1, yFac=-1):
        self.posx, self.posy = posx, posy
        self.radius = radius
        self.speed = speed
        self.color = color
        self.xFac, self.yFac = xFac, yFac
        self.trail = []

    def display(self):
        for idx, pt in enumerate(self.trail):
            fraction = (idx + 1) / len(self.trail) if self.trail else 1
            trail_radius = max(1, int(self.radius * fraction * 0.8))
            pygame.draw.circle(screen, PINK_PASTEL, (int(pt[0]), int(pt[1])), trail_radius)

        pygame.draw.circle(screen, self.color, (int(self.posx), int(self.posy)), self.radius)
        pygame.draw.circle(screen, TEXT_DARK, (int(self.posx), int(self.posy)), self.radius, 1)

    def update(self):
        self.trail.append((self.posx, self.posy))
        if len(self.trail) > 12:
            self.trail.pop(0)

        self.posx += self.xFac * self.speed
        self.posy += self.yFac * self.speed

        if self.posx <= self.radius or self.posx >= WIDTH - self.radius:
            self.xFac *= -1
            sound_wall()

        if self.posy <= self.radius + 45:
            self.yFac *= -1
            sound_wall()

        if self.posy >= HEIGHT:
            return True

        return False

    def hit_paddle(self):
        self.yFac = -abs(self.yFac)
        sound_boing()

    def hit_block(self):
        self.yFac *= -1
        sound_pop()

    def getRect(self):
        return pygame.Rect(self.posx - self.radius, self.posy - self.radius, self.radius * 2, self.radius * 2)


def collisionChecker(rect, obj_rect):
    return rect.colliderect(obj_rect)


def populateBlocks(blockWidth, blockHeight, horizontalGap, verticalGap):
    listOfBlocks = []
    num_rows = 5
    start_y = 52

    for row in range(num_rows):
        j = start_y + row * (blockHeight + verticalGap)
        for i in range(10, WIDTH - blockWidth + 5, blockWidth + horizontalGap):
            # Angka acak di bawah 50 (kelipatan 10 dari 10 sampai 50)
            initial_health = random.choice([10, 20, 30, 40, 50])
            chosen_color = random.choice(PASTEL_COLORS)
            listOfBlocks.append(Block(i, j, blockWidth, blockHeight, initial_health, chosen_color))
    return listOfBlocks


def gameOver(final_score):
    sound_game_over()
    while True:
        screen.fill(BG_CREAM)

        over_text = game_over_font.render("YAH KOK GAME OVER SIH", True, TEXT_DARK)
        score_text = ui_font.render(f"Skor Akhir Kamu: {final_score}", True, TEXT_DARK)
        restart_text = ui_font.render("Tekan Tombol Spasi di Keyboard untuk Main Lagi Ya", True, TEXT_DARK)

        box_rect = pygame.Rect(WIDTH // 2 - 230, HEIGHT // 2 - 70, 460, 145)
        pygame.draw.rect(screen, PINK_PASTEL, box_rect, border_radius=15)
        pygame.draw.rect(screen, WHITE, box_rect, 3, border_radius=15)

        screen.blit(over_text, over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 35)))
        screen.blit(score_text, score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 5)))
        screen.blit(restart_text, restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40)))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True


def main():
    running = True
    lives = 5
    score = 0
    level = 1
    base_speed = 3

    striker = Striker(WIDTH // 2 - 50, HEIGHT - 50, 100, 15, 10, PINK_PASTEL)
    strikerXFac = 0

    balls = [Ball(WIDTH // 2, HEIGHT - 150, 7, base_speed, YELLOW_BALL)]
    powerups = []

    blockWidth, blockHeight = 22, 22
    horizontalGap, verticalGap = 3, 3

    listOfBlocks = populateBlocks(blockWidth, blockHeight, horizontalGap, verticalGap)

    while running:
        screen.fill(BG_CREAM)

        # Header atas warna Pink Pastel
        pygame.draw.rect(screen, PINK_PASTEL, (0, 0, WIDTH, 45))
        pygame.draw.line(screen, WHITE, (0, 45), (WIDTH, 45), 2)
        titleText = title_font.render("BRICK BREAKER - CANDY RUSH", True, TEXT_DARK)
        screen.blit(titleText, titleText.get_rect(center=(WIDTH // 2, 22.5)))

        # Panel Bawah warna Biru Pastel (Score, Lives, Level, Balls)
        pygame.draw.rect(screen, BLUE_PASTEL, (0, HEIGHT - 35, WIDTH, 35))
        pygame.draw.line(screen, WHITE, (0, HEIGHT - 35), (WIDTH, HEIGHT - 35), 2)
        scoreText = ui_font.render(f"Score: {score}", True, TEXT_DARK)
        livesText = ui_font.render(f"Lives: {lives}", True, TEXT_DARK)
        ballsText = ui_font.render(f"Balls: {len(balls)}", True, TEXT_DARK)
        levelText = ui_font.render(f"Level: {level}", True, TEXT_DARK)

        screen.blit(scoreText, (20, HEIGHT - 25))
        screen.blit(livesText, (170, HEIGHT - 25))
        screen.blit(ballsText, (320, HEIGHT - 25))
        screen.blit(levelText, (WIDTH - 95, HEIGHT - 25))

        if not listOfBlocks:
            sound_level_up()
            level += 1
            base_speed += 0.3
            powerups.clear()
            balls = [Ball(WIDTH // 2, HEIGHT - 150, 7, base_speed, YELLOW_BALL)]
            listOfBlocks = populateBlocks(blockWidth, blockHeight, horizontalGap, verticalGap)

        if lives <= 0:
            running = gameOver(score)
            if not running:
                break
            lives = 5
            score = 0
            level = 1
            base_speed = 3
            powerups.clear()
            balls = [Ball(WIDTH // 2, HEIGHT - 150, 7, base_speed, YELLOW_BALL)]
            listOfBlocks = populateBlocks(blockWidth, blockHeight, horizontalGap, verticalGap)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    strikerXFac = -1
                if event.key == pygame.K_RIGHT:
                    strikerXFac = 1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    strikerXFac = 0

        striker.update(strikerXFac)

        for b in balls[:]:
            ball_rect = b.getRect()
            if collisionChecker(striker.getRect(), ball_rect):
                b.hit_paddle()

            for block in listOfBlocks[:]:
                if collisionChecker(block.getRect(), ball_rect):
                    b.hit_block()
                    block.hit()
                    if block.getHealth() <= 0:
                        listOfBlocks.remove(block)
                        score += 10
                        if random.random() < 0.25:
                            powerups.append(PowerUp(block.posx + block.width // 2, block.posy + block.height // 2))
                    break

            fell = b.update()
            if fell:
                balls.remove(b)

        if len(balls) == 0:
            sound_oops()
            lives -= 1
            if lives > 0:
                balls.append(Ball(WIDTH // 2, HEIGHT - 150, 7, base_speed, YELLOW_BALL))

        for p in powerups[:]:
            p.update()
            if collisionChecker(striker.getRect(), p.getRect()):
                sound_powerup()
                new_dir = random.choice([-1, 1])
                balls.append(Ball(striker.posx + striker.width // 2, striker.posy - 15, 7, base_speed, YELLOW_BALL, xFac=new_dir, yFac=-1))
                powerups.remove(p)
            elif p.posy > HEIGHT:
                powerups.remove(p)

        striker.display()
        for b in balls:
            b.display()
        for p in powerups:
            p.display()
        for block in listOfBlocks:
            block.display()

        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
    pygame.quit()