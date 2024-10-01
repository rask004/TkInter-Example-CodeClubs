from random import randint

SPACE = " "
MINE = "M"
BOOM = "*"
MARK = "X"
MINE_COUNT = 10
GRID_SIZE = 9

grid = []


def mines_grid_init():
  """initializes a grid of determined size, with randomly placed mines"""
  mines = []

  for _ in range(MINE_COUNT):
    x, y = randint(0, GRID_SIZE - 1), randint(0, GRID_SIZE - 1)
    while (x, y) in mines:
      x, y = randint(0, GRID_SIZE - 1), randint(0, GRID_SIZE - 1)
    mines.append((x, y))

  for y in range(GRID_SIZE):
    grid.append([])
    for _ in range(GRID_SIZE):
      grid[y].append(SPACE)

  for x, y in mines:
    grid[y][x] = MINE

  for y in range(GRID_SIZE):
    grid[y] = tuple(grid[y])


def check_grid(x, y):
  """check the contents of Grid"""
  if 0 > x >= GRID_SIZE or 0 > y >= GRID_SIZE:
    raise ValueError(
        f"x and y arguments must be numbers from 0 to {GRID_SIZE}")
  return grid[y][x]


def get_neighbours(x: int, y: int) -> tuple[tuple[int, int, str], ...]:
  """finds all neighbours of a given grid position.
  x : int     x coordinate
  y : int     y coordinate

  returns    tuple containing tuples[x:int, y:int, grid_value:str]
  """
  neighbours = []
  for i in [x - 1, x, x + 1]:
    for j in [y - 1, y, y + 1]:
      if i < 0 or j < 0 or i >= GRID_SIZE or j >= GRID_SIZE:
        continue
      if i == x and j == y:
        continue
      neighbours.append((i, j, grid[j][i]))
  # print(">>>>\t\t", neighbours)
  return tuple(neighbours)


def get_count_neighbours_mine(x: int, y: int) -> int:
  """counts mines neighbouring location [x, y]"""
  return len([m for _, _, m in get_neighbours(x, y) if m == MINE])


def get_neighbours_empty(x: int, y: int) -> tuple[tuple[int, int, str], ...]:
  """similar to get_neigbours(x, y) but only returns empty space neighbours"""
  return tuple([(i, j, n) for i, j, n in get_neighbours(x, y) if n == SPACE])
