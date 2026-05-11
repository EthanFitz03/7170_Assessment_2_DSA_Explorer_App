import pygame
from typing import List, Tuple, Optional
import random

from configuration import BLACK, BACKGROUND, BLUE, DARK_GREY, ORANGE, PANEL, RED, WHITE, WIDTH

from userInterface import Button, drawText

Step = Tuple[List[int], Optional[int], Optional[int], bool]

# Algorithm

def bubblesort(values: List[int]) -> List[Step]:
    data = values[:]
    steps = []

    for i in range(len(data)):
        for j in range(0, len(data) - i - 1):
            steps.append((data[:], j, j + 1, False))

            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
                steps.append((data[:], j, j + 1, True))

    steps.append((data[:], None, None, False))
    return steps

def selectionsort(values: List[int]) -> List[Step]:
    data = values[:]
    steps = []

    for i in range(len(data)):
        min_index = i

        for j in range(i + 1, len(data)):
            steps.append((data[:], min_index, j, False))

            if data[j] < data[min_index]:
                min_index = j

        if min_index != i:
            data[i], data[min_index] = data[min_index], data[i]
            steps.append((data[:], i, min_index, True))

    steps.append((data[:], None, None, False))
    return steps

def merge(left: List[int], right: List[int]) -> List[int]:
    result = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])

    return result

def mergesort(values: List[int]) -> List[int]:
    if len(values) <= 1:
        return values[:]

    middle = len(values) // 2
    return merge(mergesort(values[:middle]), mergesort(values[middle:]))

def mergesortactions(values: List[int]) -> List[Step]:
    sorted_values = mergesort(values)
    current = values[:]
    steps = []

    for i, value in enumerate(sorted_values):
        current[i] = value
        steps.append((current[:], i, None, True))

    steps.append((sorted_values[:], None, None, False))
    return steps

# Pygame Visualisation

class sortingModule:
    def __init__(self):
        self.font = pygame.font.SysFont(None, 28)
        self.smallFont = pygame.font.SysFont(None, 22)

        self.values = [random.randint(25, 280) for _ in range(12)]

        self.algorithmName = "Bubble"
        self.steps = bubblesort(self.values)
        self.stepIndex = 0
        self.running = False
        self.status = "Choose an algorithm, then press start/pause"

        self.buttons = [
            Button("Back", (20, 20, 90, 40), "back"),
            Button("Bubble", (130, 90, 120, 42), "bubble"),
            Button("Selection", (260, 90, 130, 42), "selection"),
            Button("Merge", (400, 90, 110, 42), "merge"),
            Button("Start/Pause", (540, 90, 150, 42), "start"),
            Button("Reset", (710, 90, 120, 42), "reset"),
        ]

    def run(self, screen, clock):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return "menu"

                for button in self.buttons:
                    if button.clicked(event):
                        if button.action == "back":
                            return "menu"

                        self.handleAction(button.action)

            if self.running and self.stepIndex < len(self.steps) - 1:
                self.stepIndex += 1
                self.status = (
                    f"{self.algorithmName} sort step "
                    f"{self.stepIndex}/{len(self.steps) - 1}"
                )
                pygame.time.delay(120)

            elif self.running:
                self.running = False
                self.status = "Sorting complete."

            self.draw(screen)
            pygame.display.flip()
            clock.tick(60)

    def handleAction(self, action):
        if action == "bubble":
            self.algorithmName = "Bubble"
            self.steps = bubblesort(self.values)
            self.stepIndex = 0
            self.running = False
            self.status = "Bubble sort selected."

        elif action == "selection":
            self.algorithmName = "Selection"
            self.steps = selectionsort(self.values)
            self.stepIndex = 0
            self.running = False
            self.status = "Selection sort selected."

        elif action == "merge":
            self.algorithmName = "Merge"
            self.steps = mergesortactions(self.values)
            self.stepIndex = 0
            self.running = False
            self.status = "Merge sort selected."

        elif action == "start":
            self.running = not self.running

            if self.running:
                self.status = f"{self.algorithmName} sort running."
            else:
                self.status = f"{self.algorithmName} sort paused."

        elif action == "reset":
            selected = self.algorithmName.lower()
            self.values = [random.randint(25, 280) for _ in range(12)]
            self.algorithmName = selected.capitalize()
            self.stepIndex = 0
            self.running = False

            if selected == "bubble":
                self.steps = bubblesort(self.values)
            elif selected == "selection":
                self.steps = selectionsort(self.values)
            elif selected == "merge":
                self.steps = mergesortactions(self.values)

            self.status = f"Reset values. {self.algorithmName} sort selected."

    def draw(self, screen):
        screen.fill(BACKGROUND)

        drawText(
            screen,
            "Sorting Algorithm Visualizer",
            WIDTH // 2,
            40,
            pygame.font.SysFont(None, 42),
            BLACK,
            center=True,
        )

        for button in self.buttons:
            button.draw(screen, self.font)

        pygame.draw.rect(screen, PANEL, (60, 170, 880, 400), border_radius=12)

        current, compareA, compareB, swapped = self.steps[self.stepIndex]

        barWidth = 55
        gap = 15
        baseY = 530

        for i, value in enumerate(current):
            x = 95 + i * (barWidth + gap)
            colour = BLUE

            if i == compareA or i == compareB:
                colour = RED if swapped else ORANGE

            pygame.draw.rect(
                screen,
                colour,
                (x, baseY - value, barWidth, value),
                border_radius=5,
            )

            drawText(
                screen,
                value,
                x + barWidth // 2,
                baseY + 20,
                self.smallFont,
                BLACK,
                center=True,
            )

        drawText(
            screen,
            f"Algorithm: {self.algorithmName} sort",
            60,
            610,
            self.font,
            BLACK,
        )

        drawText(
            screen,
            f"Status: {self.status}",
            60,
            645,
            self.font,
            DARK_GREY,
        )

if __name__ == "__main__":
    print(mergesort([5, 3, 8, 1, 2]))
