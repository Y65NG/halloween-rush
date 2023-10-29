from enum import Enum


class Grid(Enum):
    EMPTY = 0
    WALL = 1
    CANDY = 2


class Player:
    x: int
    y: int

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class Direction(Enum):
    UP = 0
    LEFT = 1
    DOWN = 2
    RIGHT = 3


class Game:
    width: int
    height: int
    map: list[list[Grid]]
    player: Player
    num_candies: int

    def __init__(self, width: int, height: int, num_candies: int):
        self.width = width
        self.height = height
        self.map = [[Grid.EMPTY for _ in range(height)] for _ in range(width)]
        self.num_candies = num_candies
        print(width, height)
        self.player = Player(width // 2, height // 2)

    def import_map(self, path: str):
        with open(path) as f:
            lines = f.readlines()
            for y, line in enumerate(lines):
                for x, char in enumerate(line):
                    # print(x, y)
                    match char:
                        case ".":
                            self.map[x][y] = Grid.EMPTY
                        case "o":
                            self.map[x][y] = Grid.CANDY
                        case "#":
                            self.map[x][y] = Grid.WALL
                        case "^":
                            self.player.x = x
                            self.player.y = y

    def move(self, dir: Direction) -> bool:
        x, y = self.player.x, self.player.y
        match dir:
            case Direction.UP:
                if y > 0 and self.map[x][y - 1] != Grid.WALL:
                    self.player.y -= 1
                    if self.map[x][y - 1] == Grid.CANDY:
                        self.map[x][y - 1] = Grid.EMPTY
                        self.num_candies -= 1
                        pass
                    return True
            case Direction.LEFT:
                if x > 0 and self.map[x - 1][y] != Grid.WALL:
                    self.player.x -= 1
                    if self.map[x - 1][y] == Grid.CANDY:
                        self.map[x - 1][y] = Grid.EMPTY
                        self.num_candies -= 1
                        pass
                    return True
            case Direction.DOWN:
                if y < self.height - 1 and self.map[x][y + 1] != Grid.WALL:
                    self.player.y += 1
                    if self.map[x][y + 1] == Grid.CANDY:
                        self.map[x][y + 1] = Grid.EMPTY
                        self.num_candies -= 1
                        pass
                    return True
            case Direction.RIGHT:
                if x < self.width - 1 and self.map[x + 1][y] != Grid.WALL:
                    self.player.x += 1
                    if self.map[x + 1][y] == Grid.CANDY:
                        self.map[x + 1][y] = Grid.EMPTY
                        self.num_candies -= 1
                        pass
                    return True
        return False

    def detect_player(self) -> bool:
        for x in range(self.width):
            for y in range(self.height):
                if self.map[x][y] == Grid.WALL:
                    break
                if self.player.x == x and self.player.y == y:
                    return True
        return False
