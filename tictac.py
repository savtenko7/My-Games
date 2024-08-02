import pygame as pg
import random

pg.init()
width = 300
height = 300
purple = (158, 148, 217)
black = (0, 0, 0)
white = (255, 255, 255)
yellow = (205, 217, 147)
blue = (138, 200, 255)
fps = 144
field = [["", "", ""], ["", "", ""], ["", "", ""]]
window = pg.display.set_mode((width, height))
pg.display.set_caption("крестики-нолики")

clock = pg.time.Clock()
game_over = False
win_index = [[0, 0], [1, 1], [2, 2]]
click_sound = pg.mixer.Sound("sound/клик.mp3")



def print_text(message, x, y, font_color = (purple), font_type="source/digit.ttf", font_size=50):
    font = pg.font.Font(font_type, font_size)
    text = font.render(message, True, font_color)
    window.blit(text, (x, y))


def draw_field():
    pg.draw.line(window, white, (100, 0), (100, 300))
    pg.draw.line(window, white, (200, 0), (200, 300))
    pg.draw.line(window, white, (0, 100), (300, 100))
    pg.draw.line(window, white, (0, 200), (300, 200))


def xo():
    for g in range(3):
        for i in range(3):
            if field[g][i] == "x":
                pg.draw.line(window, white, (i * 100, g * 100), (i * 100 + 100, g * 100 + 100))
                pg.draw.line(window, white, (i * 100, g * 100 + 100), (i * 100 + 100, g * 100))
            if field[g][i] == "o":
                pg.draw.circle(window, white, (i * 100 + 50, g * 100 + 50), 50, 1)


def check_win(simvol):
    global win_index
    win = False
    for i in field:
        if i.count(simvol) == 3:
            asd = field.index(i)
            win_index = [[0, asd], [1, asd], [2, asd]]
            win = True
            return win
    if field[0][0] == field[1][1] == field[2][2] == simvol:
        win_index = [[0, 0], [1, 1], [2, 2]]
        win = True
        return win
    if field[2][0] == field[1][1] == field[0][2] == simvol:
        win_index = [[2, 0], [1, 1], [0, 2]]
        win = True
        return win
    for i in range(3):
        if field[0][i] == field[1][i] == field[2][i] == simvol:
            win_index = [[i, 0], [i, 1], [i, 2]]
            win = True
            return win

def tic_tac():
    run = True
    clock = pg.time.Clock()
    game_over = False
    okmo = pg.display.set_mode((300, 300))
    while run:
        x_win = check_win("x")
        o_win = check_win("o")
        result = field[0].count("x") + field[0].count("o") + field[1].count("x") + field[1].count("o") + field[2].count(
            "x") + field[2].count("o")
        clock.tick(fps)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.MOUSEBUTTONDOWN and not game_over:
                pg.mixer.Sound.play(click_sound)
                pos = pg.mouse.get_pos()
                if field[pos[1] // 100][pos[0] // 100] == "":
                    field[pos[1] // 100][pos[0] // 100] = "x"
                    x_win = check_win("x")
                    if not x_win and result < 8:
                        x, y = random.randint(0, 2), random.randint(0, 2)
                        while field[x][y] != "":
                            x, y = random.randint(0, 2), random.randint(0, 2)
                            print(result)
                        field[x][y] = "o"
        window.fill(black)
        draw_field()
        xo()
        if x_win or o_win:
            print(win_index)
            game_over = True
            pg.draw.rect(window, blue, (win_index[0][0] * 100, win_index[0][1] * 100, 100, 100))
            pg.draw.rect(window, blue, (win_index[1][0] * 100, win_index[1][1] * 100, 100, 100))
            pg.draw.rect(window, blue, (win_index[2][0] * 100, win_index[2][1] * 100, 100, 100))
            if x_win:
                pg.display.set_caption("you win!")
                print_text("you win!", 50, 50)

            if o_win:
                pg.display.set_caption("you lose")
                print_text("you lose", 50, 50)
        if result == 9 and (not x_win and not o_win):
            game_over = True
            pg.display.set_caption("draw")
            print_text("draw", 50, 50)
        pg.display.flip()
