import pygame
import game as g
from typing import Tuple
import random as rd


class Settings:
    map_width = 9
    map_height = 16

    grid_width = 95 // 2
    game_width = map_width * grid_width
    game_height = map_height * grid_width

    screen_padding_top = 150
    screen_padding_left = 50
    screen_padding_bottom = 50

    screen_width = game_width + screen_padding_left * 2
    screen_height = game_height + screen_padding_top + screen_padding_bottom

    num_candies = 5

    # turning_duration = 100
    detection_interval = 4000
    detection_duration = 1500
    detection_random_offset = 500


class Color:
    background = (39, 42, 54)
    border = (177, 177, 182)

    red = (172, 50, 50)


def idx_to_px(x: int, y: int) -> Tuple[int, int]:
    return (
        Settings.screen_padding_left + x * Settings.grid_width,
        Settings.screen_padding_top + y * Settings.grid_width,
    )


def draw_map(game: g.Game, turning: bool):
    if turning:
        screen.fill(Color.red)
    else:
        screen.fill(Color.background)

    candy_img = pygame.image.load("./assets/candy.png")
    candy_img = pygame.transform.scale(
        candy_img, (Settings.grid_width, Settings.grid_width)
    )
    tomb_img = pygame.image.load("./assets/tombstone.png")
    tomb_img = pygame.transform.scale(
        tomb_img, (Settings.grid_width, Settings.grid_width)
    )
    for x in range(0, Settings.map_width):
        for y in range(0, Settings.map_height):
            sx, sy = idx_to_px(x, y)
            rect = pygame.Rect(sx, sy, Settings.grid_width, Settings.grid_width)
            if game.map[x][y] == g.Grid.EMPTY:
                pass
            elif game.map[x][y] == g.Grid.WALL:
                screen.blit(tomb_img, (sx, sy))
            elif game.map[x][y] == g.Grid.CANDY:
                screen.blit(candy_img, (sx, sy))
            pygame.draw.rect(screen, Color.border, rect, 1)

    pygame.draw.rect(
        screen,
        Color.border,
        pygame.Rect(
            idx_to_px(0, 0)[0] - 1,
            idx_to_px(0, 0)[1] - 1,
            Settings.game_width + 2,
            Settings.game_height + 2,
        ),
        1,
    )
    # draw_ghost(turning)


def draw_player(
    game: g.Game, dir: g.Direction, idx: int, moving: bool
) -> pygame.Surface:
    path = "./assets/"
    flip = False
    match dir:
        case g.Direction.UP:
            path += f"Char_back{idx}.png"
        case g.Direction.DOWN:
            path += f"Char{idx}.png"
        case g.Direction.LEFT:
            if not moving:
                path += f"Char_side0.png"
            else:
                path += f"Char_side{idx}.png"
        case g.Direction.RIGHT:
            flip = True
            if not moving:
                path += f"Char_side0.png"
            else:
                path += f"Char_side{idx}.png"

    player_img = pygame.image.load(path)
    scale = 10
    player_img = pygame.transform.scale(
        player_img, (Settings.grid_width + scale, Settings.grid_width + scale)
    )
    if flip:
        player_img = pygame.transform.flip(player_img, True, False)
    screen.blit(
        player_img,
        (
            idx_to_px(game.player.x, game.player.y)[0] - scale // 2,
            idx_to_px(game.player.x, game.player.y)[1] - scale // 2,
        ),
    )
    return player_img


def draw_ghost(turning: bool) -> pygame.Surface:
    if turning:
        ghost_img = pygame.image.load("./assets/Ghost_front.png")
    else:
        ghost_img = pygame.image.load("./assets/Ghost_back.png")
    ghost_img = pygame.transform.scale(
        ghost_img, (Settings.grid_width * 2, Settings.grid_width * 2)
    )
    screen.blit(
        ghost_img,
        (
            Settings.screen_width // 2 - Settings.grid_width,
            Settings.screen_padding_top - Settings.grid_width * 2,
        ),
    )
    return ghost_img


def move_ghost(game: g.Game, ghost: pygame.Surface, player: pygame.Surface):
    player_pos = idx_to_px(game.player.x, game.player.y)
    ghost = pygame.image.load("./assets/Ghost_front.png")
    ghost = pygame.transform.scale(
        ghost, (Settings.grid_width * 8, Settings.grid_width * 8)
    )

    screen.blit(
        ghost,
        (
            Settings.screen_width // 2 - Settings.grid_width * 4,
            Settings.screen_height // 2 - Settings.grid_width * 4,
        ),
    )
    pygame.display.update()


pygame.init()

screen = pygame.display.set_mode((Settings.screen_width, Settings.screen_height))


def game_loop():
    game = g.Game(Settings.map_width, Settings.map_height, Settings.num_candies)
    game.import_map("./map1.txt")

    running = True
    dead = False
    turning = False
    turning_event = pygame.USEREVENT + 0
    turning_back_event = pygame.USEREVENT + 1
    direction = g.Direction.UP
    clock = pygame.time.Clock()

    pygame.time.set_timer(
        turning_event,
        rd.randint(
            Settings.detection_interval - Settings.detection_random_offset,
            Settings.detection_interval + Settings.detection_random_offset,
        ),
    )
    while running:
        draw_map(game, turning)
        ghost = draw_ghost(turning)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
            if not dead:
                if event.type == turning_event:
                    if not turning:
                        turning = True
                        pygame.time.set_timer(
                            turning_back_event,
                            Settings.detection_duration,
                        )
                elif event.type == turning_back_event:
                    if turning:
                        turning = False
                        pygame.time.set_timer(
                            turning_event,
                            rd.randint(
                                Settings.detection_interval
                                - Settings.detection_random_offset,
                                Settings.detection_interval
                                + Settings.detection_random_offset,
                            ),
                        )

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        game.move(g.Direction.LEFT)
                        draw_player(game, g.Direction.LEFT, 1, True)
                        direction = g.Direction.LEFT

                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        game.move(g.Direction.RIGHT)
                        draw_player(game, g.Direction.RIGHT, 1, True)
                        direction = g.Direction.RIGHT
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        game.move(g.Direction.UP)
                        draw_player(game, g.Direction.UP, 1, True)
                        direction = g.Direction.UP
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        game.move(g.Direction.DOWN)
                        draw_player(game, g.Direction.DOWN, 1, True)
                        direction = g.Direction.DOWN

            player = draw_player(game, direction, 1, False)
            if not dead and game.num_candies == 0:
                draw_map(game, turning)
                pygame.display.update()
                font = pygame.font.Font("freesansbold.ttf", 32)
                text = font.render("You Win!", True, (255, 255, 255))
                screen.blit(text, (Settings.screen_width // 2 - 80, 15))
                font = pygame.font.Font("freesansbold.ttf", 20)
                text = font.render("Press space to restart", True, (255, 255, 255))
                screen.blit(text, (Settings.screen_width // 2 - 100, 50))
                pygame.display.update()
                pygame.time.delay(1000)
                finished = False
                while not finished:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                            game_loop()

                        if event.type == pygame.QUIT:
                            pygame.quit()
                            quit()
                            # running = False
            if turning and game.detect_player():
                
                draw_ghost(turning)
                draw_map(game, turning)
                pygame.display.update()
                pygame.time.delay(1000)
                print("Detected!")
                dead = True
                # ghost.set_alpha(0)
                pygame.display.update()
                pygame.time.delay(1000)
                move_ghost(game, ghost, player)
                font = pygame.font.Font("freesansbold.ttf", 32)
                text = font.render("Game Over", True, (255, 255, 255))
                screen.blit(text, (Settings.screen_width // 2 - 90, 15))
                font = pygame.font.Font("freesansbold.ttf", 20)
                text = font.render("Press space to restart", True, (255, 255, 255))
                screen.blit(text, (Settings.screen_width // 2 - 120, 50))
                pygame.display.update()
                pygame.time.delay(1000)
                restart = False
                while not restart:
                    move_ghost(game, ghost, player)
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                            restart = True
                            game_loop()
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            quit()
                            # running = False

            pygame.display.update()


game_loop()
