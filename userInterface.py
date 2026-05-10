import pygame
from configuration import BLACK, BLUE, DARK_GREY, LIGHT_BLUE, WHITE

def drawText(surface, text, x, y, font, colour=BLACK, center=False):
    textSurface = font.render(str(text), True, colour)
    textRect = textSurface.get_rect()

    if center:
        textRect.center = (x, y)
    else:
        textRect.topleft = (x, y)

    surface.blit(textSurface, textRect)
    return textRect

class Button:
    def __init__(self, text, rect, action=None, colour=LIGHT_BLUE, hoverColour=BLUE):
        self.text = text
        self.rect = pygame.Rect(rect)
        self.action = action
        self.colour = colour
        self.hoverColour = hoverColour

    def draw(self, surface, font):
        mousePos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mousePos):
            fill = self.hoverColour
            textColour = WHITE
        else:
            fill = self.colour
            textColour = BLACK

        pygame.draw.rect(surface, fill, self.rect, border_radius=10)
        pygame.draw.rect(surface, DARK_GREY, self.rect, width=2, border_radius=10)

        drawText(
            surface,
            self.text,
            self.rect.centerx,
            self.rect.centery,
            font,
            textColour,
            center=True
        )

    def clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )
