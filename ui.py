import pygame

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
