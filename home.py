import sys
import pygame
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

class Button:

    BTN = (60, 70, 110)
    BTN_HOVER = (90, 105, 160)
    TEXT_COLOUR = (240, 230, 230)

    def __init__(self, text, center, action, size=(300, 60)):
        self.text = text
        self.action = action
        self.rect = pygame.Rect(0, 0, *size)
        self.rect.center = center
        self.font = pygame.font.Font(None, 48)

    def draw(self, surface):
        hovered = self.rect.collidepoint(pygame.mouse.get_pos())
        if hovered:
            colour = self.BTN_HOVER
        else:
            colour = self.BTN
        pygame.draw.rect(surface, colour, self.rect, border_radius=10)
        label = self.font.render(self.text, True, self.TEXT_COLOUR)
        surface.blit(label, label.get_rect(center = self.rect.center))

    def clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )


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

def start_game():
    global screen, running
    screen = pygame.display.set_mode(game_loop.WINDOW_SIZE)
    result = game_loop.run(screen)

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.event.clear()
    if result == "quit":
        running = False

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
                    elif b.action == "game":
                        start_game()
                    else:
                        state = b.action
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                state = "menu"
    
    if state == "menu":
        draw_menu()
    elif state == "options":
        draw_placeholder("Options")

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()