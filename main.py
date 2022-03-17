import random
import numpy as np
import pygame

N = 4
WIN_WIDTH = 600
WIN_HEIGHT = 600
Spacing = 10
pygame.init()
Font = pygame.font.SysFont("arialblack", 30)
max_score = 0
pause = False
global game

win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
quit_img = pygame.image.load("quit.png")
play_img = pygame.image.load("play.png")
restart_img = pygame.image.load("restart.png")
button_width = play_img.get_width()
button_height = play_img.get_height()

# RGB colour for squares
RGB = {
    'background': (189, 172, 161),
    0: (204, 192, 172),
    2: (238, 228, 219),
    4: (240, 226, 202),
    8: (242, 177, 121),
    16: (236, 141, 85),
    32: (250, 123, 92),
    64: (234, 90, 56),
    128: (237, 207, 114),
    256: (242, 208, 75),
    512: (237, 200, 80),
    1024: (227, 186, 19),
    2048: (236, 196, 2),
    4096: (96, 217, 146)
}


# button class
class button():
    def __init__(self, x, y, image, ids):
        self.img = image
        self.rect = self.img.get_rect()
        self.rect.topleft = (x, y)
        self.id = ids

    def draw(self, win):
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                if self.id == 0 or self.id == 1:
                    game_2048()
                elif self.id == 2:
                    pygame.quit()
                    quit()
                elif self.id == 3:
                    global pause
                    pause = False

        win.blit(self.img, (self.rect.x, self.rect.y))


class Game:

    def __init__(self):
        self.grid = np.zeros((N, N), dtype=int)

    def __str__(self):
        return str(self.grid)

    def random_number(self, k):
        free_poss = list(zip(*np.where(self.grid == 0)))

        for pos in random.sample(free_poss, k):
            if random.random() < .1:
                self.grid[pos] = 4
            else:
                self.grid[pos] = 2

    def add(self, row_col):
        numbers_in_row = row_col[row_col != 0]
        sum_numbers = []
        skip = False
        for j in range(len(numbers_in_row)):
            if skip:
                skip = False
                continue
            if j != len(numbers_in_row) - 1 and numbers_in_row[j] == numbers_in_row[j + 1]:
                number = numbers_in_row[j] * 2
                skip = True
            else:
                number = numbers_in_row[j]
            sum_numbers.append(number)
        return sum_numbers

    def move(self, move):
        try:
            for i in range(N):
                if move in 'lr':
                    row_col = self.grid[i, :]
                elif move in 'ud':
                    row_col = self.grid[:, i]

                if move in 'rd':
                    row_col = row_col[::-1]

                sum_numbers = self.add(row_col)
                row_col_moved = np.zeros_like(row_col)
                row_col_moved[:len(sum_numbers)] = sum_numbers

                if move in 'rd':
                    row_col_moved = row_col_moved[::-1]

                if move in 'lr':
                    self.grid[i, :] = row_col_moved
                elif move in 'ud':
                    self.grid[:, i] = row_col_moved
        except:
            pass

    def game_over(self):
        copy_grid = self.grid.copy()
        for move in 'lrud':
            self.move(move)
            if not all((self.grid == copy_grid).flatten()):
                self.grid = copy_grid
                return True
        return False


def draw_game(win, grid):
    win.fill(RGB['background'])
    for i in range(N):
        for j in range(N):
            n = grid[i][j]

            rect_y = i * WIN_HEIGHT // N + Spacing
            rect_x = j * WIN_WIDTH // N + Spacing
            rect_w = WIN_WIDTH // N - 2 * Spacing
            rect_h = WIN_HEIGHT // N - 2 * Spacing

            pygame.draw.rect(win, RGB[n], pygame.Rect(rect_x, rect_y, rect_w, rect_h), border_radius=8)
            text = Font.render(str(n), True, (0, 0, 0))
            if n != 0:
                text_rect = text.get_rect(center=(rect_x + rect_w / 2, rect_y + rect_h / 2))
                win.blit(text, text_rect)


def wait_for_key():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    return 'u'
                elif event.key == pygame.K_DOWN:
                    return 'd'
                elif event.key == pygame.K_LEFT:
                    return 'l'
                elif event.key == pygame.K_RIGHT:
                    return 'r'
                elif event.key == pygame.K_ESCAPE:
                    Pause(win)

def Pause(win):
    global pause
    pause = True

    win.fill(RGB['background'])

    while pause:
        play_button = button(WIN_WIDTH / 2 - button_width / 2, WIN_HEIGHT - button_height / 2 - 500, play_img, 3)
        play_button.draw(win)
        restart_button = button(WIN_WIDTH / 2 - button_width / 2, WIN_HEIGHT - button_height / 2 - 300, restart_img, 1)
        restart_button.draw(win)
        quit_button = button(WIN_WIDTH / 2 - button_width / 2, WIN_HEIGHT - button_height / 2 - 100, quit_img, 2)
        quit_button.draw(win)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pause = False
        global game
    draw_game(win, game.grid)
    pygame.display.update()

def intro(score):
    intro = True
    global max_score
    max_score = max(score, max_score)
    max_score_text = Font.render("Max Score: " + str(max_score), True, (0, 0, 0))
    lastgame_score_text = Font.render("Score From Last game:" + str(score), True, (0, 0, 0))

    win.fill(RGB['background'])

    while intro:
        pygame.display.update()
        play_button = button(WIN_WIDTH / 2 - button_width / 2, WIN_HEIGHT - button_height / 2 - 150, play_img, 0)
        play_button.draw(win)
        win.blit(max_score_text, (WIN_WIDTH / 2 - max_score_text.get_width() / 2, WIN_HEIGHT / 2 - 100))
        win.blit(lastgame_score_text, (WIN_WIDTH / 2 - lastgame_score_text.get_width() / 2, WIN_HEIGHT / 2 - 200))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


def game_2048():
    pygame.display.set_caption("2048")
    pygame.display.set_icon(pygame.image.load("2048_logo.png"))
    global game
    game = Game()
    game.random_number(2)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        print(game.grid)
        draw_game(win, game.grid)
        pygame.display.update()
        cmd = wait_for_key()
        grid_copy = game.grid.copy()
        game.move(cmd)
        running = game.game_over()
        if not all((game.grid == grid_copy).flatten()):
            game.random_number(1)

    intro(np.sum(game.grid))


if __name__ == '__main__':
    intro(0)
