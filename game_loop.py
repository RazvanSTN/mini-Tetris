"""game_loop.py - the pygame side of a single-player match.

Reads the keyboard, tells Game what the player did, and draws the result.
No game rules live here: Game decides what every move means.

Coordinates used by the logic: x = 1..10 (left to right), y = 1.. (bottom to top).
Rows y = 1..20 are visible; spawn rows above 20 are hidden.
"""
import pygame
from game import Game

# ---------------------------------------------------------------- layout
CELL = 30
COLS = 10
VISIBLE_ROWS = 20
BOARD_X, BOARD_Y = 40, 30
BOARD_W, BOARD_H = COLS * CELL, VISIBLE_ROWS * CELL
PANEL_X = BOARD_X + BOARD_W + 40
WINDOW_SIZE = (PANEL_X + 190, BOARD_Y + BOARD_H + 30)
FPS = 60

# ---------------------------------------------------------------- timing (ms)
GRAVITY_MS = 800      # time between automatic downward steps
DAS_MS = 150          # delay before a held key starts repeating
ARR_MS = 50           # repeat interval for left/right
SOFT_DROP_MS = 40     # repeat interval while soft drop is held

# ---------------------------------------------------------------- colors
BG = (18, 18, 24)
GRID_LINE = (40, 40, 52)
BOARD_BG = (10, 10, 14)
BORDER = (120, 120, 140)
TEXT = (230, 230, 240)
DIM_TEXT = (140, 140, 160)
BLOCK_COLORS = {            # names come from piece_logic.colors
    "yellow": (240, 220, 0),
    "light_blue": (0, 200, 240),
    "purple": (160, 40, 220),
    "orange": (240, 140, 0),
    "blue": (40, 60, 240),
    "green": (40, 210, 60),
    "red": (230, 40, 40),
}
FALLBACK_COLOR = (150, 150, 150)

# ---------------------------------------------------------------- keybinds
# action -> pygame key. The settings screen can pass its own dict to run().
DEFAULT_KEYBINDS = {
    "left": pygame.K_LEFT,
    "right": pygame.K_RIGHT,
    "soft_drop": pygame.K_DOWN,
    "rotate": pygame.K_UP,
    "hard_drop": pygame.K_SPACE,
    "pause": pygame.K_p,
    "restart": pygame.K_r,
    "menu": pygame.K_ESCAPE,
}
REPEAT_INTERVALS = {"left": ARR_MS, "right": ARR_MS, "soft_drop": SOFT_DROP_MS}


# ================================================================ helpers
def color_of(name):
    return BLOCK_COLORS.get(name, FALLBACK_COLOR)


def cell_rect(x, y):
    """Screen rectangle of the board cell (x, y)."""
    return pygame.Rect(
        BOARD_X + (x - 1) * CELL,
        BOARD_Y + (VISIBLE_ROWS - y) * CELL,
        CELL,
        CELL,
    )


def is_visible(x, y):
    return 1 <= x <= COLS and 1 <= y <= VISIBLE_ROWS


def apply_action(game, action):
    """Translate a player action into calls on Game."""
    if action == "left":
        game.move_left()
    elif action == "right":
        game.move_right()
    elif action == "soft_drop":
        game.move_down()
    elif action == "rotate":
        game.rotate()
    elif action == "hard_drop":
        # tick() returns None while the piece keeps falling and a line count
        # (an int) once it locks, so this stops right after the lock.
        while game.move_down() is None:
            pass


def ghost_cells(game):
    """Where the current piece would land. Does not modify the game."""
    cells = [(b.x, b.y) for b in game.piece.blocks]
    while game.board.is_valid([(x, y - 1) for x, y in cells]):
        cells = [(x, y - 1) for x, y in cells]
    return cells


# ================================================================ drawing
def draw_block(screen, x, y, color_name):
    if not is_visible(x, y):
        return
    rect = cell_rect(x, y).inflate(0, 0)
    base = color_of(color_name)
    pygame.draw.rect(screen, base, rect)
    # little highlight so blocks do not look flat
    light = tuple(min(255, c + 60) for c in base)
    pygame.draw.line(screen, light, rect.topleft, rect.topright, 2)
    pygame.draw.line(screen, light, rect.topleft, rect.bottomleft, 2)


def draw_ghost(screen, x, y, color_name):
    if not is_visible(x, y):
        return
    rect = cell_rect(x, y).inflate(-4, -4)
    pygame.draw.rect(screen, color_of(color_name), rect, 2)


def draw_board(screen, game):
    board_rect = pygame.Rect(BOARD_X, BOARD_Y, BOARD_W, BOARD_H)
    pygame.draw.rect(screen, BOARD_BG, board_rect)

    # grid lines
    for i in range(1, COLS):
        px = BOARD_X + i * CELL
        pygame.draw.line(screen, GRID_LINE, (px, BOARD_Y), (px, BOARD_Y + BOARD_H))
    for j in range(1, VISIBLE_ROWS):
        py = BOARD_Y + j * CELL
        pygame.draw.line(screen, GRID_LINE, (BOARD_X, py), (BOARD_X + BOARD_W, py))

    # locked blocks
    for (x, y, color) in game.board.occupied_cells:
        draw_block(screen, x, y, color)

    # current piece (+ ghost). After game over the new piece overlaps the
    # stack, so it is not drawn.
    if not game.game_over:
        piece_color = game.piece.blocks[0].color
        for x, y in ghost_cells(game):
            draw_ghost(screen, x, y, piece_color)
        for b in game.piece.blocks:
            draw_block(screen, b.x, b.y, b.color)

    pygame.draw.rect(screen, BORDER, board_rect.inflate(4, 4), 2)


def draw_panel(screen, game, fonts):
    big, small = fonts
    y = BOARD_Y
    screen.blit(small.render("SCORE", True, DIM_TEXT), (PANEL_X, y))
    screen.blit(big.render(str(game.score), True, TEXT), (PANEL_X, y + 24))

    y += 110
    screen.blit(small.render("CONTROLS", True, DIM_TEXT), (PANEL_X, y))
    lines = [
        "Left/Right  move",
        "Up          rotate",
        "Down        soft drop",
        "Space       hard drop",
        "P  pause    R  restart",
        "Esc  menu",
    ]
    for i, line in enumerate(lines):
        screen.blit(small.render(line, True, TEXT), (PANEL_X, y + 26 + i * 22))


def draw_overlay(screen, title, subtitle, fonts):
    big, small = fonts
    shade = pygame.Surface((BOARD_W, BOARD_H), pygame.SRCALPHA)
    shade.fill((0, 0, 0, 170))
    screen.blit(shade, (BOARD_X, BOARD_Y))
    cx = BOARD_X + BOARD_W // 2
    cy = BOARD_Y + BOARD_H // 2
    t = big.render(title, True, TEXT)
    s = small.render(subtitle, True, DIM_TEXT)
    screen.blit(t, t.get_rect(center=(cx, cy - 15)))
    screen.blit(s, s.get_rect(center=(cx, cy + 20)))


# ================================================================ main loop
def run(screen, keybinds=None):
    """Run one single-player match.

    Returns "menu" when the player leaves the match, or "quit" when the
    window is closed, so home.py knows what to do next.
    """
    keybinds = keybinds or DEFAULT_KEYBINDS
    key_to_action = {key: action for action, key in keybinds.items()}

    clock = pygame.time.Clock()
    fonts = (pygame.font.Font(None, 48), pygame.font.Font(None, 26))

    game = Game()
    paused = False
    gravity_timer = 0
    held = {}  # action -> time (ms) of its next auto-repeat

    while True:
        dt = clock.tick(FPS)
        now = pygame.time.get_ticks()

        # ---------------------------------------------------------- input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.KEYDOWN:
                action = key_to_action.get(event.key)
                if action == "menu":
                    return "menu"
                if action == "restart":
                    game, paused, gravity_timer, held = Game(), False, 0, {}
                elif action == "pause":
                    if not game.game_over:
                        paused = not paused
                        held.clear()
                elif action and not paused and not game.game_over:
                    apply_action(game, action)
                    if action in REPEAT_INTERVALS:
                        held[action] = now + DAS_MS

            elif event.type == pygame.KEYUP:
                held.pop(key_to_action.get(event.key), None)

        # --------------------------------------------------------- update
        if not paused and not game.game_over:
            for action, next_fire in list(held.items()):
                if now >= next_fire and not game.game_over:
                    apply_action(game, action)
                    held[action] = now + REPEAT_INTERVALS[action]

            gravity_timer += dt
            if gravity_timer >= GRAVITY_MS and not game.game_over:
                gravity_timer = 0
                game.tick()

        # ----------------------------------------------------------- draw
        screen.fill(BG)
        draw_board(screen, game)
        draw_panel(screen, game, fonts)
        if paused:
            draw_overlay(screen, "PAUSED", "press P to resume", fonts)
        elif game.game_over:
            draw_overlay(screen, "GAME OVER", "R restart  |  Esc menu", fonts)
        pygame.display.flip()


# Lets you test the game without home.py:  python game_loop.py
if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Tetris")
    window = pygame.display.set_mode(WINDOW_SIZE)
    run(window)
    pygame.quit()