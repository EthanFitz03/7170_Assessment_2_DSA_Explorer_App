import pygame
from collections import deque
from typing import Dict, List, Tuple

from configuration import BACKGROUND, BLACK, BLUE, DARK_GREY, GREEN, ORANGE, PANEL, WHITE, WIDTH


from userInterface import Button, drawText


# Graph Data Structure

class Graph:
    def __init__(self) -> None:
        self._adjList: Dict[str, List[str]] = {}

    def newVertex(self, vertex: str) -> None:
        if vertex not in self._adjList:
            self._adjList[vertex] = []

    def newEdge(self, vertexA: str, vertexB: str, directed: bool = False) -> None:
        if vertexA == vertexB:
            raise ValueError("Self-loops are not allowed.")

        self.newVertex(vertexA)
        self.newVertex(vertexB)

        if vertexB not in self._adjList[vertexA]:
            self._adjList[vertexA].append(vertexB)

        if not directed and vertexA not in self._adjList[vertexB]:
            self._adjList[vertexB].append(vertexA)

    def vertices(self) -> List[str]:
        return list(self._adjList.keys())

    def neighbours(self, vertex: str) -> List[str]:
        return self._adjList.get(vertex, [])

    def edges(self) -> List[Tuple[str, str]]:
        edgeList = []
        seen = set()

        for vertex in self._adjList:
            for neighbour in self._adjList[vertex]:
                edgeKey = tuple(sorted((vertex, neighbour)))

                if edgeKey not in seen:
                    edgeList.append((vertex, neighbour))
                    seen.add(edgeKey)

        return edgeList

    def breadthFirst(self, start: str) -> List[str]:
        if start not in self._adjList:
            return []

        visitedOrder = []
        visited = set()
        queue = deque()

        queue.append(start)
        visited.add(start)

        while queue:
            current = queue.popleft()
            visitedOrder.append(current)

            for neighbour in sorted(self.neighbours(current)):
                if neighbour not in visited:
                    visited.add(neighbour)
                    queue.append(neighbour)

        return visitedOrder

    def breadthFirstL(self, start: str) -> Dict[int, List[str]]:
        if start not in self._adjList:
            return {}

        levels: Dict[int, List[str]] = {}
        visited = set()
        queue = deque()

        queue.append((start, 0))
        visited.add(start)

        while queue:
            current, level = queue.popleft()

            if level not in levels:
                levels[level] = []

            levels[level].append(current)

            for neighbour in sorted(self.neighbours(current)):
                if neighbour not in visited:
                    visited.add(neighbour)
                    queue.append((neighbour, level + 1))

        return levels

    def depthFirst(self, start: str) -> List[str]:
        if start not in self._adjList:
            return []

        visitedOrder = []
        visited = set()
        stack = [start]

        while stack:
            current = stack.pop()

            if current not in visited:
                visited.add(current)
                visitedOrder.append(current)

                for neighbour in reversed(sorted(self.neighbours(current))):
                    if neighbour not in visited:
                        stack.append(neighbour)

        return visitedOrder

    def depthFirstD(self, start: str) -> Dict[int, List[str]]:
        if start not in self._adjList:
            return {}

        depths: Dict[int, List[str]] = {}
        visited = set()
        stack = [(start, 0)]

        while stack:
            current, depth = stack.pop()

            if current not in visited:
                visited.add(current)

                if depth not in depths:
                    depths[depth] = []

                depths[depth].append(current)

                for neighbour in reversed(sorted(self.neighbours(current))):
                    if neighbour not in visited:
                        stack.append((neighbour, depth + 1))

        return depths


# PyGame Visualiser

class GraphModule:
    def __init__(self):
        self.font = pygame.font.SysFont(None, 28)
        self.smallFont = pygame.font.SysFont(None, 22)
        self.tinyFont = pygame.font.SysFont(None, 19)

        self.graph = Graph()
        self.createSampleGraph()

        self.positions = {
            "A": (480, 190),
            "B": (310, 300),
            "C": (650, 300),
            "D": (230, 470),
            "E": (430, 490),
            "F": (720, 470),
        }

        self.selectedStart = "A"
        self.traversal = []
        self.bfsLevels = {}
        self.dfsDepths = {}
        self.currentMode = "None"

        self.status = "Click a node, then click BFS or DFS to run visualiser"

        self.buttons = [
            Button("Back", (20, 20, 90, 40), "back"),
            Button("Run BFS", (145, 120, 130, 42), "bfs"),
            Button("Run DFS", (295, 120, 130, 42), "dfs"),
            Button("Reset", (445, 120, 120, 42), "reset"),
        ]

    def createSampleGraph(self):
        for vertex in ["A", "B", "C", "D", "E", "F"]:
            self.graph.newVertex(vertex)

        self.graph.newEdge("A", "B")
        self.graph.newEdge("A", "C")
        self.graph.newEdge("B", "D")
        self.graph.newEdge("B", "E")
        self.graph.newEdge("C", "F")
        self.graph.newEdge("E", "F")

    def run(self, screen, clock):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return "menu"

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.handleNodeClick(event.pos)

                for button in self.buttons:
                    if button.clicked(event):
                        if button.action == "back":
                            return "menu"

                        self.handleAction(button.action)

            self.draw(screen)
            pygame.display.flip()
            clock.tick(60)

    def handleNodeClick(self, mousePosition):
        for vertex, position in self.positions.items():
            distance = pygame.Vector2(mousePosition).distance_to(position)

            if distance <= 30:
                self.selectedStart = vertex
                self.traversal = []
                self.bfsLevels = {}
                self.dfsDepths = {}
                self.currentMode = "None"
                self.status = f"Selected start node: {vertex}"

    def handleAction(self, action):
        if action == "bfs":
            self.traversal = self.graph.breadthFirst(self.selectedStart)
            self.bfsLevels = self.graph.breadthFirstL(self.selectedStart)
            self.dfsDepths = {}
            self.currentMode = "BFS"

            self.status = (
                f"BFS traversal from {self.selectedStart}: "
                f"{', '.join(self.traversal)}"
            )

        elif action == "dfs":
            self.traversal = self.graph.depthFirst(self.selectedStart)
            self.dfsDepths = self.graph.depthFirstD(self.selectedStart)
            self.bfsLevels = {}
            self.currentMode = "DFS"

            self.status = (
                f"DFS traversal from {self.selectedStart}: "
                f"{', '.join(self.traversal)}"
            )

        elif action == "reset":
            self.selectedStart = "A"
            self.traversal = []
            self.bfsLevels = {}
            self.dfsDepths = {}
            self.currentMode = "None"
            self.status = "Traversal reset. Start node set back to A"

    def draw(self, screen):
        screen.fill(BACKGROUND)

        drawText(
            screen,
            "Graph Traversal Visualiser",
            WIDTH // 2,
            45,
            pygame.font.SysFont(None, 42),
            BLACK,
            center=True,
        )

        drawText(
            screen,
            "Click a node to choose a start point. Run BFS or DFS to view traversal order",
            WIDTH // 2,
            85,
            self.smallFont,
            DARK_GREY,
            center=True,
        )

        for button in self.buttons:
            button.draw(screen, self.font)

        pygame.draw.rect(
            screen,
            PANEL,
            (85, 175, 820, 400),
            border_radius=12
        )

        self.drawEdges(screen)
        self.drawNodes(screen)
        self.drawStatus(screen)

    def drawEdges(self, screen):
        for vertexA, vertexB in self.graph.edges():
            pygame.draw.line(
                screen,
                DARK_GREY,
                self.positions[vertexA],
                self.positions[vertexB],
                3,
            )

    def drawNodes(self, screen):
        for vertex in self.graph.vertices():
            position = self.positions[vertex]
            colour = BLUE

            if vertex == self.selectedStart:
                colour = GREEN

            if vertex in self.traversal:
                colour = ORANGE

            pygame.draw.circle(screen, colour, position, 30)
            pygame.draw.circle(screen, BLACK, position, 30, 2)

            label = vertex

            if vertex in self.traversal:
                visitNumber = self.traversal.index(vertex) + 1
                label = f"{vertex}{visitNumber}"

            drawText(
                screen,
                label,
                position[0],
                position[1],
                self.font,
                WHITE,
                center=True,
            )

    def drawStatus(self, screen):
        drawText(
            screen,
            f"Selected start node: {self.selectedStart}",
            85,
            605,
            self.font,
            BLACK,
        )

        drawText(
            screen,
            f"Mode: {self.currentMode}",
            85,
            635,
            self.font,
            BLACK,
        )

        drawText(
            screen,
            f"Traversal order: {self.traversal}",
            85,
            665,
            self.smallFont,
            BLACK,
        )

        if self.currentMode == "BFS":
            drawText(
                screen,
                f"BFS levels: {self.bfsLevels}",
                540,
                605,
                self.smallFont,
                BLACK,
            )

            drawText(
                screen,
                "BFS levels show distance from the start node",
                540,
                635,
                self.tinyFont,
                DARK_GREY,
            )

        elif self.currentMode == "DFS":
            drawText(
                screen,
                f"DFS depths: {self.dfsDepths}",
                540,
                605,
                self.smallFont,
                BLACK,
            )

            drawText(
                screen,
                "DFS depths show branch depth, not shortest distance",
                540,
                635,
                self.tinyFont,
                DARK_GREY,
            )

        else:
            drawText(
                screen,
                self.status,
                540,
                605,
                self.smallFont,
                DARK_GREY,
            )


if __name__ == "__main__":
    graph = Graph()

    for vertex in ["A", "B", "C", "D", "E", "F"]:
        graph.newVertex(vertex)

    graph.newEdge("A", "B")
    graph.newEdge("A", "C")
    graph.newEdge("B", "D")
    graph.newEdge("B", "E")
    graph.newEdge("C", "F")
    graph.newEdge("E", "F")

    print("BFS from F:", graph.breadthFirst("F"))
    print("BFS levels from F:", graph.breadthFirstL("F"))
    print("DFS from F:", graph.depthFirst("F"))
    print("DFS depths from F:", graph.depthFirstD("F"))
