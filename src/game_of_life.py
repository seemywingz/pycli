# game_of_life.py

width, height = 10, 10
activeCell = "X"
inactiveCell = "O"
grid = [[inactiveCell] * width for _ in range(height)]


def setCell(x, y, value):
    y = height - 1 - y
    if 0 <= x < width and 0 <= y < height:
        grid[y][x] = value


def randomizeGrid():
    from random import choice

    for row in grid:
        for i, _ in enumerate(row):
            row[i] = choice([activeCell, inactiveCell])


def printGrid():
    print()
    print("\n".join(" ".join(row) for row in grid))


def start(maxWidth, maxHeight):
    global grid, width, height
    width, height = maxWidth, maxHeight
    grid = [[inactiveCell] * width for _ in range(height)]
    # randomizeGrid()  # Uncomment this line if you want a randomized grid.
    setCell(0, 0, activeCell)  # Set a cell to "X" at coordinate (0, 0)
    printGrid()


if __name__ == "__main__":
    # For testing, call start with your desired dimensions.
    start(10, 10)
