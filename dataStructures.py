import pygame
from dataclasses import dataclass
from typing import List, Optional

from configuration import BACKGROUND, BLACK, BLUE, DARK_GREY, GREEN, HEIGHT, ORANGE, PANEL, WHITE, WIDTH
from userInterface import Button, drawText

#Stack & Queue

class stack:
    def __init__(self) -> None:
        self._data: List[int] = []

    def push(self, item: int) -> None:
        self._data.append(item)

    def pop(self) -> Optional[int]:
        if self.isEmpty():
            return None
        return self._data.pop()

    def peek(self) -> Optional[int]:
        if self.isEmpty():
            return None
        return self._data[-1]

    def isEmpty(self) -> bool:
        return len(self._data) == 0

    def size(self) -> int:
        return len(self._data)

    def items(self) -> List[int]:
        return self._data[:]

class queue:
    def __init__(self) -> None:
        self._data: List[int] = []

    def insert(self, item: int) -> None:
        self._data.append(item)

    def remove(self) -> Optional[int]:
        if self.isEmpty():
            return None
        return self._data.pop(0)

    def isEmpty(self) -> bool:
        return len(self._data) == 0

    def size(self) -> int:
        return len(self._data)

    def items(self) -> List[int]:
        return self._data[:]


# Linked List
@dataclass
class listNode:
    value: int
    next: object = None

class linkedList:
    def __init__(self) -> None:
        self.head = None

    def insertAt(self, value: int, position: int) -> None:
        newNode = listNode(value)

        if position <= 0 or self.head is None:
            newNode.next = self.head
            self.head = newNode
            return

        current = self.head
        index = 0

        while current.next is not None and index < position - 1:
            current = current.next
            index += 1

        newNode.next = current.next
        current.next = newNode

    def delete(self, value: int) -> bool:
        if self.head is None:
            return False

        if self.head.value == value:
            self.head = self.head.next
            return True

        current = self.head

        while current.next is not None:
            if current.next.value == value:
                current.next = current.next.next
                return True

            current = current.next

        return False

    def reverse(self) -> None:
        previous = None
        current = self.head

        while current is not None:
            nextNode = current.next
            current.next = previous
            previous = current
            current = nextNode

        self.head = previous

    def traverse(self) -> List[int]:
        current = self.head
        values = []

        while current is not None:
            values.append(current.value)
            current = current.next

        return values


# BST
@dataclass
class BSTNode:
    value: int
    left: object = None
    right: object = None

class BST:
    def __init__(self) -> None:
        self.root = None

    def insert(self, value: int) -> None:
        self.root = self._insert(self.root, value)

    def _insert(self, node, value: int):
        if node is None:
            return BSTNode(value)

        if value < node.value:
            node.left = self._insert(node.left, value)
        elif value > node.value:
            node.right = self._insert(node.right, value)

        return node

    def inorder(self) -> List[int]:
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result) -> None:
        if node:
            self._inorder(node.left, result)
            result.append(node.value)
            self._inorder(node.right, result)

    def preorder(self) -> List[int]:
        result = []
        self._preorder(self.root, result)
        return result

    def _preorder(self, node, result) -> None:
        if node:
            result.append(node.value)
            self._preorder(node.left, result)
            self._preorder(node.right, result)

    def postorder(self) -> List[int]:
        result = []
        self._postorder(self.root, result)
        return result

    def _postorder(self, node, result) -> None:
        if node:
            self._postorder(node.left, result)
            self._postorder(node.right, result)
            result.append(node.value)

# Pygame Module
class DataStructuresModule:
    def __init__(self):
        self.font = pygame.font.SysFont(None, 28)
        self.smallFont = pygame.font.SysFont(None, 22)
        self.tinyFont = pygame.font.SysFont(None, 19)

        self.stack = stack()
        self.queue = queue()
        self.linkedList = linkedList()
        self.bst = BST()

        self.nextValue = 10
        self.status = "Use the provided buttons to interact structure"

        self.buttons = [
            Button("Back", (20, 20, 90, 40), "back"),

            Button("Stack Push", (40, 125, 140, 42), "stackPush"),
            Button("Stack Pop", (190, 125, 130, 42), "stackPop"),

            Button("Queue Insert", (365, 125, 160, 42), "queueInsert"),
            Button("Queue Remove", (535, 125, 160, 42), "queueRemove"),

            Button("List Insert", (40, 445, 140, 42), "listInsert"),
            Button("List Delete", (190, 445, 130, 42), "listDelete"),
            Button("List Reverse", (330, 445, 140, 42), "listReverse"),

            Button("BST Insert", (650, 445, 140, 42), "bstInsert"),
            Button("Reset", (800, 445, 120, 42), "reset"),
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

            self.draw(screen)
            pygame.display.flip()
            clock.tick(60)

    def handleAction(self, action):
        if action == "stackPush":
            self.stack.push(self.nextValue)
            self.status = f"Pushed {self.nextValue} onto the stack"
            self.nextValue += 10

        elif action == "stackPop":
            self.status = f"Popped {self.stack.pop()} off the stack"

        elif action == "queueInsert":
            self.queue.insert(self.nextValue)
            self.status = f"Inserted {self.nextValue} into the queue"
            self.nextValue += 10

        elif action == "queueRemove":
            self.status = f"Removed {self.queue.remove()} from the queue"

        elif action == "listInsert":
            position = len(self.linkedList.traverse())
            self.linkedList.insertAt(self.nextValue, position)
            self.status = f"Inserted {self.nextValue} at the end of the linked list"
            self.nextValue += 10

        elif action == "listDelete":
            values = self.linkedList.traverse()
            self.status = "List is empty"

            if values:
                self.linkedList.delete(values[0])
                self.status = f"Deleted {values[0]} from the linked list"

        elif action == "listReverse":
            self.linkedList.reverse()
            self.status = f"Reversed the linked list"

        elif action == "bstInsert":
            sequence = [50, 30, 70, 20, 40, 60, 80]
            value = sequence[len(self.bst.inorder()) % len(sequence)]
            self.bst.insert(value)
            self.status = f"Inserted {value} into the bst"

        elif action == "reset":
            self.__init__()

    def draw(self, screen):
        screen.fill(BACKGROUND)

        drawText(screen, "Data Structures Playground", WIDTH // 2, 35, pygame.font.SysFont(None, 42),
                 BLACK, center=True,)

        drawText(screen, "ESC or Back", 20, 68, self.smallFont, DARK_GREY)
        drawText(screen, "returns to menu", 20, 88, self.smallFont, DARK_GREY)

        for button in self.buttons:
            button.draw(screen, self.font)

        self.drawStack(screen)
        self.drawQueue(screen)
        self.drawLinkedList(screen)
        self.drawBST(screen)

        drawText(screen, f"Status: {self.status}", 40, HEIGHT - 35, self.font, BLACK)

    def drawStack(self, screen):
        x, y = 60, 210

        drawText(screen, "Stack - LIFO", x, y - 35, self.font, BLACK)
        pygame.draw.rect(screen, PANEL, (x, y, 260, 190), border_radius=12)

        for i, value in enumerate(reversed(self.stack.items())):
            rect = pygame.Rect(x + 70, y + 20 + i * 35, 120, 28)
            pygame.draw.rect(screen, BLUE, rect, border_radius=6)

            drawText(screen, value, rect.centerx, rect.centery,self.smallFont, WHITE, center=True)

    def drawQueue(self, screen):
        x, y = 365, 210

        drawText(screen, "Queue - FIFO", x, y - 35, self.font, BLACK)
        pygame.draw.rect(screen, PANEL, (x, y, 600, 110), border_radius=12)

        for i, value in enumerate(self.queue.items()):
            rect = pygame.Rect(x + 20 + i * 75, y + 38, 58, 35)
            pygame.draw.rect(screen, GREEN, rect, border_radius=6)

            drawText(screen, value, rect.centerx, rect.centery,self.smallFont, WHITE, center=True)

        drawText(screen, "Front", x + 18, y + 82, self.font, DARK_GREY)
        drawText(screen, "Back", x + 510, y + 82, self.font, DARK_GREY)

    def drawLinkedList(self, screen):
        x, y = 40, 530

        drawText(screen, "Linked List", x, y - 35, self.font, BLACK)
        values = self.linkedList.traverse()

        for i, value in enumerate(values):
            rect = pygame.Rect(x + i * 105, y, 65, 40)
            pygame.draw.rect(screen, ORANGE, rect, border_radius=8)

            drawText(screen, value, rect.centerx, rect.centery, self.smallFont, WHITE, center=True)

            if i < len(values) - 1:
                pygame.draw.line(screen, BLACK, (rect.right + 5, rect.centery), (rect.right + 35, rect.centery), 3)
                pygame.draw.polygon(screen, BLACK, [
                    (rect.right + 35, rect.centery),
                    (rect.right + 25, rect.centery - 6),
                    (rect.right + 25, rect.centery + 6),
                ],
                                    )

    def drawBST(self, screen):
        x = 650
        y = 535
        panelWidth = 315
        panelHeight = 150

        pygame.draw.rect(
            screen,
            PANEL,
            (x, y, panelWidth, panelHeight),
            border_radius=12
        )

        drawText(
            screen,
            "BST Visualiser",
            x + 12,
            y + 8,
            self.smallFont,
            BLACK
        )

        if self.bst.root is None:
            drawText(
                screen,
                "Click BST Insert to add nodes",
                x + 20,
                y + 55,
                self.tinyFont,
                DARK_GREY
            )
        else:
            self.drawBSTNode(
                screen,
                self.bst.root,
                x + panelWidth // 2,
                y + 38,
                62
            )

        dividerY = y + 95

        pygame.draw.line(
            screen,
            DARK_GREY,
            (x + 12, dividerY),
            (x + panelWidth - 12, dividerY),
            1
        )

        traversalY = y + 102

        drawText(
            screen,
            f"Inorder: {self.bst.inorder()}",
            x + 12,
            traversalY,
            self.tinyFont,
            BLACK
        )

        drawText(
            screen,
            f"Preorder: {self.bst.preorder()}",
            x + 12,
            traversalY + 20,
            self.tinyFont,
            BLACK
        )

        drawText(
            screen,
            f"Postorder: {self.bst.postorder()}",
            x + 12,
            traversalY + 40,
            self.tinyFont,
            BLACK
        )

    def drawBSTNode(self, screen, node, x, y, spacing):
        if node is None:
            return

        radius = 11
        levelGap = 25

        if node.left is not None:
            childX = x - spacing
            childY = y + levelGap

            pygame.draw.line(
                screen,
                BLACK,
                (x, y + radius),
                (childX, childY - radius),
                2
            )

            self.drawBSTNode(
                screen,
                node.left,
                childX,
                childY,
                max(spacing // 2, 22)
            )

        if node.right is not None:
            childX = x + spacing
            childY = y + levelGap

            pygame.draw.line(
                screen,
                BLACK,
                (x, y + radius),
                (childX, childY - radius),
                2
            )

            self.drawBSTNode(
                screen,
                node.right,
                childX,
                childY,
                max(spacing // 2, 22)
            )

        pygame.draw.circle(screen, BLUE, (x, y), radius)
        pygame.draw.circle(screen, BLACK, (x, y), radius, 2)

        drawText(
            screen,
            node.value,
            x,
            y,
            self.tinyFont,
            WHITE,
            center=True
        )

if __name__ == "__main__":
    s = stack()
    s.push(10)
    s.push(20)
    print("Stack pop:", s.pop())

