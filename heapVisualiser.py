import heapq

import pygame
import random
from typing import List, Optional, Tuple

from configuration import BACKGROUND, BLACK, BLUE, DARK_GREY, GREEN, PANEL, PURPLE, HEIGHT, WIDTH, WHITE
from userInterface import Button, drawText

# Heap & event queue

class Heap:
    def __init__(self) -> None:
        self._data: List[int] = []

    def insert(self, item: int) -> None:
        heapq.heappush(self._data, item)

    def remove(self) -> Optional[int]:
        if self.isEmpty():
            return None

        return heapq.heappop(self._data)

    def peek(self) -> Optional[int]:
        if self.isEmpty():
            return None

        return self._data[0]

    def isEmpty(self) -> bool:
        return len(self._data) == 0

    def traverse(self) -> List[int]:
        return self._data

class EventQueue:
    def __init__(self) -> None:
        self._data: List[Tuple[int, int, int, str]] = []
        self._counter = 0

    def insert(self, priority: int, time: int, description: str) -> None:
        heapq.heappush(self._data, (priority, time, self._counter, description))
        self._counter += 1

    def remove(self):
        if self.isEmpty():
            return None

        priority, time, _, description = heapq.heappop(self._data)

        return {"priority": priority, "time": time, "description": description}

    def isEmpty(self) -> bool:
        return len(self._data) == 0

    def traverse(self):
        return [(priority, time, description) for priority, time, _, description in sorted(self._data)]


# Pygame visualisation

class HeapModule:
    def __init__(self):
        self.font = pygame.font.SysFont(None, 28)
        self.smallFont = pygame.font.SysFont(None, 22)

        self.heap = Heap()
        self.events = EventQueue()

        self.eventScrollIndex = 0
        self.eventVisibleRows = 8

        self.status = "Insert heap values or add priority events"

        self.buttons = [
            Button("Back", (20, 20, 90, 40), "back"),
            Button("Insert Heap", (120, 90, 150, 42), "insertHeap"),
            Button("Extract Min", (285, 90, 150, 42), "extractMin"),
            Button("Add Event", (470, 90, 140, 42), "addEvent"),
            Button("Process Event", (625, 90, 160, 42), "processEvent"),
            Button("Reset", (810, 90, 110, 42), "reset"),
        ]

    def getMaxEventScroll(self):
        totalEvents = len(self.events.traverse())
        return max(0, totalEvents - self.eventVisibleRows)

    def scrollEvents(self, amount):
        maxScroll = self.getMaxEventScroll()

        self.eventScrollIndex += amount

        if self.eventScrollIndex < 0:
            self.eventScrollIndex = 0

        if self.eventScrollIndex > maxScroll:
            self.eventScrollIndex = maxScroll

    def eventQueueRect(self):
        return pygame.Rect(520, 160, 420, 420)

    def drawStatus(self, screen):
        statusPanel = pygame.Rect(40, HEIGHT - 65, 920, 45)

        pygame.draw.rect(
            screen,
            PANEL,
            statusPanel,
            border_radius=10
        )

        pygame.draw.rect(
            screen,
            DARK_GREY,
            statusPanel,
            width=1,
            border_radius=10
        )

        drawText(
            screen,
            f"Status: {self.status}",
            statusPanel.x + 15,
            statusPanel.y + 13,
            self.font,
            BLACK
        )

    def run(self, screen, clock):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return "menu"

                if event.type == pygame.MOUSEWHEEL:
                    if self.eventQueueRect().collidepoint(pygame.mouse.get_pos()):
                        self.scrollEvents(-event.y)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.eventQueueRect().collidepoint(event.pos):
                        if event.button == 4:
                            self.scrollEvents(-1)
                        elif event.button == 5:
                            self.scrollEvents(1)

                for button in self.buttons:
                    if button.clicked(event):
                        if button.action == "back":
                            return "menu"

                        self.handleAction(button.action)

            self.draw(screen)
            pygame.display.flip()
            clock.tick(60)

    def handleAction(self, action):
        if action == "insertHeap":
            value = random.randint(1, 99)
            self.heap.insert(value)
            self.status = f"Inserted {value}. Minimum is now {self.heap.peek()}."

        elif action == "extractMin":
            value = self.heap.remove()
            self.status = f"Extracted minimum value: {value}."

        elif action == "addEvent":
            priority = random.randint(1, 6)
            time = random.randint(1, 20)
            description = f"Event {random.randint(100, 999)}"

            self.events.insert(priority, time, description)

            if self.eventScrollIndex > self.getMaxEventScroll():
                self.eventScrollIndex = self.getMaxEventScroll()

            self.status = (
                f"Added {description}. Priority {priority}, time {time}. "
                "Priority 1 is highest."
            )

        elif action == "processEvent":
            event = self.events.remove()

            if self.eventScrollIndex > self.getMaxEventScroll():
                self.eventScrollIndex = self.getMaxEventScroll()

            self.status = f"Processed event: {event}."

        elif action == "reset":
            self.__init__()

    def draw(self, screen):
        screen.fill(BACKGROUND)

        drawText(
            screen,
            "Heap and Event Queue Visualizer",
            WIDTH // 2, 40,
            pygame.font.SysFont(None, 42),
            BLACK,
            center=True
        )

        for button in self.buttons:
            button.draw(screen, self.font)

        pygame.draw.rect(screen, PANEL, (60, 160, 400, 420), border_radius=12)
        pygame.draw.rect(screen, PANEL, (520, 160, 420, 420), border_radius=12)

        drawText(screen, "Min Heap", 80, 180, self.font, BLACK)
        self.drawHeapTree(screen)

        drawText(screen, f"Internal heap list: {self.heap.traverse()}", 80, 535,self.smallFont, DARK_GREY)
        drawText(screen, "Priority Event Queue", 545, 180, self.font, BLACK)
        drawText(screen, "Priority 1 = highest. Larger numbers = lower priority", 545, 210, self.smallFont, DARK_GREY)

        pendingEvents = self.events.traverse()

        queueArea = pygame.Rect(545, 250, 350, 285)

        oldClip = screen.get_clip()
        screen.set_clip(queueArea)

        start = self.eventScrollIndex
        end = start + self.eventVisibleRows
        visibleEvents = pendingEvents[start:end]

        for i, event in enumerate(visibleEvents):
            priority, time, description = event

            rect = pygame.Rect(
                queueArea.x,
                queueArea.y + i * 35,
                335,
                28
            )

            pygame.draw.rect(screen, PURPLE, rect, border_radius=6)

            drawText(
                screen,
                f"P{priority} | Time {time} | {description}",
                rect.x + 10,
                rect.y + 6,
                self.smallFont,
                WHITE,
            )

        screen.set_clip(oldClip)

        if len(pendingEvents) > self.eventVisibleRows:
            scrollTrack = pygame.Rect(910, 250, 10, 285)
            pygame.draw.rect(screen, DARK_GREY, scrollTrack, border_radius=5)

            maxScroll = self.getMaxEventScroll()
            thumbHeight = max(35, int(285 * self.eventVisibleRows / len(pendingEvents)))
            scrollRatio = self.eventScrollIndex / maxScroll if maxScroll > 0 else 0
            thumbY = 250 + int((285 - thumbHeight) * scrollRatio)

            scrollThumb = pygame.Rect(910, thumbY, 10, thumbHeight)
            pygame.draw.rect(screen, BLUE, scrollThumb, border_radius=5)

        self.drawStatus(screen)

    def priorityLabel(self, priority):
        if priority == 1:
            return "Highest Priority"
        elif priority == 2:
            return "High Priority"
        elif priority == 3:
            return "Medium Priority"
        else:
            return "Low Priority"

    def drawHeapTree(self, screen):
        values = self.heap.traverse()

        if not values:
            drawText(screen, "Heap is empty", 175, 360, self.font, DARK_GREY)
            return

        positions = [
            (260, 240),
            (170, 330),
            (350, 330),
            (125, 430),
            (215, 430),
            (305, 430),
            (395, 430),
        ]

        for i in range(min(len(values), len(positions))):
            left = 2 * i + 1
            right = 2 * i + 2

            for child in [left, right]:
                if child < len(values) and child < len(positions):
                    pygame.draw.line(screen, BLACK, positions[i], positions[child], 2,)

        for i, value in enumerate(values[:7]):
            colour = GREEN if i == 0 else BLUE
            pygame.draw.circle(screen, colour, positions[i], 28)
            pygame.draw.circle(screen, BLACK, positions[i], 28, 2)

            drawText(screen, value, positions[i][0], positions[i][1], self.font, WHITE, center=True)

if __name__ == "__main__":
    h = Heap()

    for value in [5, 1, 9, 3]:
        h.insert(value)

    print(h.remove(), h.remove())
