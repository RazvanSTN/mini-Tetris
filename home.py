import sys
import pygame
from ui import Button
import game_loop


pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

title_font = pygame.font.Font(None, 96)
text_font = pygame.font.Font(None, 48) 

BG = (20, 24, 40)
WHITE = (240, 230, 230)

button = [
    Button("Play", (WIDTH // 2, 300), "game"),
    Button("Settings", (WIDTH // 2, 380), "options"),
    Button("Quit", (WIDTH // 2, 460), "quit"),
]


state = "menu"

def draw_menu():
    screen.fill(BG)
    print("menu draw running")
    title = title_font.render("Mini Tetris", True, WHITE)
    screen.blit(title, title.get_rect(center = (WIDTH // 2, 140)))
    for b in button:
        b.draw(screen)

def draw_placeholder(text):
    screen.fill(BG)
    msg = text_font.render(text + " (ESC to go back)", True, WHITE)
    screen.blit(msg, msg.get_rect(center = (WIDTH // 2, HEIGHT // 2)))


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if state == "menu":
            for b in button:
                if b.clicked(event):
                    if b.action == "quit":
                        running = False
                    else:
                        state = b.action
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                state = "menu"
    
    if state == "menu":
        draw_menu()
    elif state == "game":
        draw_placeholder("Game running")
    elif state == "options":
        draw_placeholder("Options")

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()