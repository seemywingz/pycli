# game_of_life.py
import os
import time
from random import choice

# 1. Any live cell with fewer than two live neighbors dies, as if by underpopulation.
# 2. Any live cell with two or three live neighbors lives on to the next generation.
# 3. Any live cell with more than three live neighbors dies, as if by overpopulation.
# 4. Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction.


class GameOfLife:
    def __init__(self, width, height, generations):
        self.width = width
        self.height = height
        self.generations = generations
        self.currentGen = 0
        self.stop = False
        self.activeCell = "󰝤"
        self.inactiveCell = " "
        self.grid = [
            [self.inactiveCell] * self.width for _ in range(self.height)
        ]

    def setCell(self, x, y, value):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y][x] = value

    def randomizeGrid(self):
        for row in self.grid:
            for i, _ in enumerate(row):
                row[i] = choice([self.activeCell, self.inactiveCell])

    def printGrid(self):
        print()
        print("\n".join(" ".join(row) for row in self.grid))

    def countNeighbors(self, x, y):
        neighbors = 0
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                if 0 <= x + dx < self.width and 0 <= y + dy < self.height:
                    if self.grid[y + dy][x + dx] == self.activeCell:
                        neighbors += 1
        return neighbors

    def applyRules(self):
        curGrid = [row[:] for row in self.grid]
        print("Current Generation:", self.currentGen)
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                neighbors = self.countNeighbors(x, y)
                if cell == self.activeCell:
                    if neighbors < 2 or neighbors > 3:
                        self.setCell(x, y, self.inactiveCell)
                else:
                    if neighbors == 3:
                        self.setCell(x, y, self.activeCell)
        self.currentGen += 1
        if curGrid == self.grid:
            print("Stable configuration found. Stopping...")
            self.stop = True

    def start(self, loop=False):
        self.randomizeGrid()
        while not self.stop:
            os.system("cls" if os.name == "nt" else "clear")
            self.printGrid()
            self.applyRules()
            time.sleep(0.05)
            if not loop or not self.stop:
                self.stop = self.currentGen >= self.generations


def main():
    game = GameOfLife(10, 10, 300)
    game.start()


if __name__ == "__main__":
    main()
