import pygame
from configuration import BLACK, BLUE, DARK_GREY, LIGHT_BLUE, WHITE

def draw_text(surface, text, x, y, font, colour=BLACK, center=False):
    image = font.render(str(text), True, colour)
    rect = image.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topLeft = (x, y)
        surface.blit(image, rect)
        return rect

class Button:
    def __init__(self, text, rect, action=None, colour=LIGHT_BLUE, hover_colour=BLUE):
        self.text = text
        self.rect = pygame.Rect(rect)
        self.action = action
        self.colour = colour
        self.hover_colour = hover_colour

    def draw(self, surface, font):
        mouse_pos = pygame.mouse.get_pos()
        fill = self.hover_colour if self.rect.collidepoint(mouse_pos) else self.colour
        pygame.draw.rect(surface, fill, self.rect, border_radius=10)
        pygame.draw.rect(surface, DARK_GREY, self.rect, width=2, border_radius=10)

        text_colour = WHITE if fill == BLUE else BLACK
        draw_text(
            surface,
            self.text, self.rect.centerx, self.rect.centery,
            font, text_colour, center=True
        )

    def clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )
