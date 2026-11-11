import sys
import pygame

WIDTH = 800
HEIGHT = 600

BG = (20, 24, 40)
WHITE = (240, 230, 230)
button_font = pygame.font.Font(None, 48) 


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

def draw_game(text):
    screen.fill(BG)
    msg = button_font.render(text + " (ESC to go back)", True, WHITE)
    screen.blit(msg, msg.get_rect(center = (WIDTH // 2, HEIGHT // 2)))
