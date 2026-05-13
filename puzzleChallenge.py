import pygame
from typing import List, Set, Tuple
import heapq

from configuration import BLACK, BACKGROUND, DARK_GREY, GREEN, ORANGE, PANEL, RED, WHITE, WIDTH, YELLOW
from userInterface import Button, drawText

INF = float("inf")
GridCell = Tuple[int, int]

# Path and dynamic program

def dijkstra(rows: int, cols: int, start: GridCell, end: GridCell, obstacles: Set[GridCell]):

    distances = {start: 0}
    previous = {}
    heap = [(0, start)]
    visited = set()
    visitOrder = []

    while heap:
        currentDistance, current = heapq.heappop(heap)

        if current in visited:
            continue

        visited.add(current)
        visitOrder.append(current)

        if current == end:
            break

        row, col = current

        neighbours = [
            (row - 1, col),
            (row + 1, col),
            (row, col - 1),
            (row, col + 1),
        ]

        for neighbour in neighbours:
            nr, nc = neighbour

            if 0 <= nr < rows and 0 <= nc < cols and neighbour not in obstacles:
                newDistance = currentDistance + 1

                if newDistance < distances.get(neighbour, INF):
                    distances[neighbour] = newDistance
                    previous[neighbour] = current
                    heapq.heappush(heap, (newDistance, neighbour))

    path = []

    if end in distances:
        node = end

        while node != start:
            path.append(node)
            node = previous[node]

        path.append(start)
        path.reverse()

    return path, visitOrder

def gridPaths(rows: int, cols: int, obstacles: Set[GridCell]) -> List[List[int]]:

    dp = [[0 for _ in range(cols)] for _ in range(rows)]

    for row in range(rows):
        for col in range(cols):
            cell = (row, col)

            if cell in obstacles:
                dp[row][col] = 0

            elif row == 0 and col == 0:
                dp[row][col] = 1

            else:
                top = dp[row - 1][col] if row > 0 else 0
                left = dp[row][col - 1] if col > 0 else 0
                dp[row][col] = top + left

    return dp

# pygame visualisation

class PuzzlesModule:
    def __init__(self):
        self.font = pygame.font.SysFont(None, 28)
        self.smallFont = pygame.font.SysFont(None, 22)

        self.rows = 10
        self.cols = 10
        self.cellSize = 42

        self.gridX = 80
        self.gridY = 180

        self.start = (0, 0)
        self.end = (9, 9)

        self.obstacles = set()
        self.path = []
        self.visited = []
        self.dp = None

        self.status = "Left click cells to toggle obstacles."

        self.buttons = [
            Button("Back", (20, 20, 90, 40), "back"),
            Button("Run Dijkstra", (130, 90, 160, 42), "dijkstra"),
            Button("DP Path Count", (310, 90, 170, 42), "dp"),
            Button("Reset", (500, 90, 120, 42), "reset"),
        ]

    def run(self, screen, clock):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return "menu"

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.handleGridClick(event.pos)

                for button in self.buttons:
                    if button.clicked(event):
                        if button.action == "back":
                            return "menu"

                        self.handleAction(button.action)

            self.draw(screen)
            pygame.display.flip()
            clock.tick(60)

    def handleGridClick(self, pos):
        x, y = pos

        col = (x - self.gridX) // self.cellSize
        row = (y - self.gridY) // self.cellSize

        if 0 <= row < self.rows and 0 <= col < self.cols:
            cell = (row, col)

            if cell != self.start and cell != self.end:
                if cell in self.obstacles:
                    self.obstacles.remove(cell)
                else:
                    self.obstacles.add(cell)

                self.path = []
                self.visited = []
                self.dp = None
                self.status = f"Toggled obstacle at {cell}."

    def handleAction(self, action):
        if action == "dijkstra":
            self.path, self.visited = dijkstra(
                self.rows,
                self.cols,
                self.start,
                self.end,
                self.obstacles,
            )

            if self.path:
                self.status = f"Path length: {len(self.path)}"
            else:
                self.status = "No path exists."

        elif action == "dp":
            self.dp = gridPaths(self.rows, self.cols, self.obstacles)
            self.status = f"Number of paths to end: {self.dp[-1][-1]}"

        elif action == "reset":
            self.__init__()

    def draw(self, screen):
        screen.fill(BACKGROUND)

        drawText(
            screen,
            "Puzzle Challenges: Pathfinding and Dynamic Programming",
            WIDTH // 2,
            40,
            pygame.font.SysFont(None, 38),
            BLACK,
            center=True,
        )

        for button in self.buttons:
            button.draw(screen, self.font)

        pygame.draw.rect(screen, PANEL, (55, 155, 470, 470), border_radius=12)

        self.grid(screen)
        self.infoPanel(screen)

    def grid(self, screen):
        for row in range(self.rows):
            for col in range(self.cols):
                cell = (row, col)

                rect = pygame.Rect(
                    self.gridX + col * self.cellSize,
                    self.gridY + row * self.cellSize,
                    self.cellSize - 2,
                    self.cellSize - 2,
                )

                colour = WHITE

                if cell in self.visited:
                    colour = YELLOW

                if cell in self.path:
                    colour = ORANGE

                if cell in self.obstacles:
                    colour = DARK_GREY

                if cell == self.start:
                    colour = GREEN

                if cell == self.end:
                    colour = RED

                pygame.draw.rect(screen, colour, rect)
                pygame.draw.rect(screen, BLACK, rect, 1)

                if self.dp is not None and cell not in self.obstacles:
                    drawText(
                        screen,
                        self.dp[row][col],
                        rect.centerx,
                        rect.centery,
                        self.smallFont,
                        BLACK,
                        center=True,
                    )

    def infoPanel(self, screen):
        x = 580

        pygame.draw.rect(screen, PANEL, (560, 150, 370, 390), border_radius=12)

        drawText(screen, "Instructions", x, 180, self.font, BLACK)
        drawText(screen, "Green = start, red = end", x, 230, self.smallFont)
        drawText(screen, "Grey = obstacle", x, 260, self.smallFont)
        drawText(screen, "Yellow = visited", x, 290, self.smallFont)
        drawText(screen, "Orange = shortest path", x, 320, self.smallFont)

        drawText(screen, "Dijkstra: shortest path", x, 375, self.smallFont, BLACK)
        drawText(screen, "DP: counts possible paths", x, 405, self.smallFont, BLACK)

        drawText(
            screen,
            f"Obstacles: {len(self.obstacles)}",
            x,
            455,
            self.smallFont,
            BLACK,
        )

        drawText(screen, self.status, x, 500, self.smallFont, BLACK)


if __name__ == "__main__":
    path, visited = dijkstra(3, 3, (0, 0), (2, 2), {(1, 1)})

    print("Path:", path)
    print("DP:", gridPaths(3, 3, {(1, 1)}))

