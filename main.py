import pygame
import sys

from configuration import BACKGROUND, BLACK, HEIGHT, PANEL, WIDTH, FPS
from userInterface import Button, drawText
from dataStructures import DataStructuresModule
from sortingAlgorithmVisualiser import sortingModule
from graphVisualiser import GraphModule
from heapVisualiser import HeapModule
from puzzleChallenge import PuzzlesModule

class DSAApp:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('DSA Explorer and Visualiser App')
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        self.title_font = pygame.font.SysFont(None, 48)
        self.font = pygame.font.SysFont(None, 30)
        self.small_font = pygame.font.SysFont(None, 24)

        self.buttons = [
            Button("Data Structures", (380, 180, 240, 55), "data"),
            Button("Heap", (380, 390, 240, 55), "heap"),
            Button("Quit", (380, 530, 240, 55), "quit"),
            Button("Sorting", (380, 250, 240, 55), "sorting"),
            Button("Graphs", (380, 320, 240, 55), "graphs"),
            Button("Puzzles", (380, 460, 240, 55), "puzzles"),
        ]

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_app()

                for button in self.buttons:
                    if button.clicked(event):
                        self.open_module(button.action)

            self.draw_menu()
            pygame.display.flip()
            self.clock.tick(FPS)

    def draw_menu(self):
        self.screen.fill(BACKGROUND)

        pygame.draw.rect(self.screen, PANEL, (250, 100, 500, 520), border_radius=18)

        drawText(self.screen, "DSA Explorer and Visualiser App", WIDTH // 2, 70, self.title_font, BLACK, center=True)

        drawText(self.screen, "Use menu to open the interactive Pygame modules", WIDTH // 2, 130, self.small_font, BLACK, center=True)

        for button in self.buttons:
            button.draw(self.screen, self.font)

    def open_module(self, action):
        if action == "quit":
            self.quit_app()

        module = None

        if action == "data":
            module = DataStructuresModule() #naming conventions that will be used for modules
        elif action == "sorting":
            module = sortingModule()
        elif action == "graphs":
            module = GraphModule()
        elif action == "heap":
            module = HeapModule()
        elif action == "puzzles":
            module = PuzzlesModule()

        if module is not None:
            result = module.run(self.screen, self.clock)
            if result == "quit":
                self.quit_app

    def quit_app(self):
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    DSAApp().run()

