import pygame as pg
import pygame.image
import random
from tictac import tic_tac

pg.init()

okno_widht = 800
okno_height = 600
land = pg.image.load('image/land1.jpg ')
okno = pg.display.set_mode((okno_widht, okno_height))
clock = pg.time.Clock()

button_sound = pg.mixer.Sound('sound/клик.mp3')



pg.init()


pg.display.set_caption('Resident Evil 9: Blood Desert')

pg.mixer.music.load("sound/фон.mp3")
pg.mixer.music.set_volume(0.2)

jump_sound = pg.mixer.Sound('sound/прыжок.mp3')
after_jump = pg.mixer.Sound('sound/приземление.mp3')
hit = pg.mixer.Sound("sound/столкнулся.mp3")
g_o = pg.mixer.Sound('sound/game_over.mp3')

make_jump = False


enemy_img = [pg.image.load('image/enemy1_walk2.png'), pg.image.load('image/zombie_walk0.png'), pg.image.load('image/soldier_stand.png')]
enemy_options = [65, 412, 75, 397, 59, 409] #высота = высота экрана - 100 - высота изображения

hero_img = [pg.image.load('image/hero_run.png'), pg.image.load('image/hero_run2.png'), pg.image.load('image/hero_run3.png')]
img_counter = 0



scores = 0
max_scores = 100
health = 3
health_img = pg.image.load('image/life.png')
health_img = pg.transform.scale(health_img, (30, 30))

class Enemy():
    def __init__(self, x, y, width, speed, image):
        self.x = x
        self.y = y
        self.image = image
        self.width = width
        self.speed = speed

    def move(self):
        if self.x >= self.width - 100:
            okno.blit(self.image,(self.x, self.y))
            #pg.draw.rect(okno, (224, 121, 13), (self.x, self.y, self.width, self.height))
            self.x -= self.speed
            return True


        else:
            self.x = okno_widht + 100 + random.randint(-80, 60)
            return False
    def return_self(self, radius, y, width, image):
        self.x = radius
        self.y = y
        self.width = width
        self.image = image
        okno.blit(self.image,(self.x, self.y))



def create_enemy(array):
    choice = random.randint(0, 2 )
    img = enemy_img[choice]
    width = enemy_options[choice * 2]
    height = enemy_options[choice * 2 + 1]
    array.append(Enemy(okno_widht +  20, height,width, 4, img))

    choice = random.randint(0, 2)
    img = enemy_img[choice]
    width = enemy_options[choice * 2]
    height = enemy_options[choice * 2 + 1]
    array.append(Enemy(okno_widht + 300, height, width, 4, img))

    choice = random.randint(0, 2)
    img = enemy_img[choice]
    width = enemy_options[choice * 2]
    height = enemy_options[choice * 2 + 1]
    array.append(Enemy(okno_widht + 600, height, width, 4, img))

def find_rad(array):
    maximum = max(array[0].x,  array[1].x)
    if maximum < okno_widht:
        radius = okno_widht
        if radius - maximum < 50:
            radius += 150
    else:
        radius = maximum

    choice = random.randint(0, 5)

    if choice == 0:
        radius += 15

    else:
        radius += random.randint(200, 300)
    return radius
def draw_enemy_arr(enemy_arr):
    for enemy in enemy_arr:
        check = enemy.move()
        if not check:
            return_enemy(enemy_arr, enemy)


def draw_hero():
    global img_counter, make_jump
    if img_counter == 30:
        img_counter = 0
    if make_jump:
        okno.blit(pg.image.load('image/hero_jump.png'), (hero_x, hero_y))
    else:
        okno.blit(hero_img[img_counter // 10], (hero_x, hero_y))
        img_counter += 1


def jump():
    global hero_y, make_jump, jump_counter
    if jump_counter >= -30:
        if jump_counter == 30:
            pg.mixer.Sound.play(jump_sound)
        if jump_counter == -10:
            pg.mixer.Sound.play(after_jump)
        hero_y -= jump_counter / 2.5
        jump_counter -= 1

    else:
        jump_counter = 30
        make_jump = False

def show_health():
    global health
    show = 0
    x = 20
    for i in range(health):

        okno.blit(health_img, (x, 30))
        x += 20
        show += 1

def check_health():
    global health
    health -= 1
    if health == 0:
        return False
    else:
        return True

def return_enemy(enemy_list, enemy):
    radius = find_rad(enemy_list)
    choice = random.randint(0, 2)
    img = enemy_img[choice]
    width = enemy_options[choice * 2]
    y = enemy_options[choice * 2 + 1]
    enemy.return_self(radius, y, width, img)

def check_collision(enemy_list):
    global scores
    for enemy in enemy_list:
        if not make_jump:
            if enemy.x <= hero_x + hero_width + 5 <= enemy.x + enemy.width:
                if check_health():
                    pg.mixer.Sound.play(hit)
                    return_enemy(enemy_list, enemy)
                    return False
                else:
                    return True
            else:
                if hero_y + hero_height - 3 >= enemy.y:
                    if enemy.x <= hero_x + hero_width + 5 <= enemy.x + enemy.width:
                        if check_health():
                            pg.mixer.Sound.play(hit)
                            return_enemy(enemy_list, enemy)
                            return False
                        else:
                            return True
        elif jump_counter >= 1:
            if hero_y + hero_height - 2 >= enemy.y:
                if enemy.x <= hero_x + hero_width - 22 <= enemy.x + enemy.width:
                    if check_health():
                        pg.mixer.Sound.play(hit)
                        return_enemy(enemy_list, enemy)
                        return False
                    else:
                        return True
        elif jump_counter == 10:
            if hero_y + hero_height - 5 >= enemy.y:
                if enemy.x <= hero_x + hero_width - 5 <= enemy.x + enemy.width:
                    scores += 1
                    return_enemy(enemy_list, enemy)
                    return False
        elif jump_counter <=1:
            if hero_y + hero_height >= enemy.y:
                if enemy.x <= hero_x + hero_width - 5 <= enemy.x + enemy.width:
                    scores += 1
                    return_enemy(enemy_list, enemy)
                    return False
    return False

def game_cycle():
    global make_jump
    run = True
    enemy_arr = []
    create_enemy(enemy_arr)
    pg.mixer.music.play(-1)



    while run:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                run = False
        keys = pg.key.get_pressed()
        if keys[pg.K_ESCAPE]:
            pause()

        if keys[pg.K_SPACE]:
            make_jump = True

        if make_jump:
            jump()


        okno.blit(land, (-900, -750))
        print_text(f"Scores: {scores}", 600, 100)

        draw_enemy_arr(enemy_arr)

        draw_hero()
        show_health()
        pg.display.update()

        if check_collision(enemy_arr):
            pg.mixer.music.stop()
            pg.mixer.Sound.play(g_o)
            run = False

        clock.tick(90)

    return game_over()


def pause():
    paused = True
    pg.mixer.music.pause()
    while paused:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                run = False
        print_text("""Pause""", 350, 260)
        print_text("""Press Space to continue""", 230, 290)

        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE]:
            paused = False
        pg.display.update()
        clock.tick(15)
    pg.mixer.music.unpause()
def game_over():
    global scores
    stoped = True
    while stoped:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                run = False
        print_text("""Game Over""", 350, 260)
        print_text("""Press Enter to play again""", 230, 290)
        print_text("""Press Esc to exit""", 260, 320)

        keys = pg.key.get_pressed()
        if keys[pg.K_RETURN]:
            health = 3
            scores = 0
            return True

        if keys[pg.K_ESCAPE]:
            return False

        pg.display.update()
        clock.tick(15)






######### параметры героя
jump_counter = 30
hero_width = 60
hero_height = 111
hero_x = okno_widht // 3
hero_y = okno_height - hero_height - 100


def rpg_game():
    while game_cycle():
        scores = 0
        jump_counter = 30
        make_jump = False
        health = 3
        hero_y = okno_height - hero_height - 100




class Button:
    def __init__(self, width, height, color, active_color):
        self.width = width
        self.height = height
        self.color = color
        self.active_color = active_color

    def draw(self, x, y, message, action=None, font_size=30):
        mouse = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()
        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            pg.draw.rect(okno, self.active_color, (x, y, self.width, self.height))
            if click[0] == 1 and action is not None:
                pg.mixer.Sound.play(button_sound)
                pg.time.delay(300)
                action()
        else:
            pg.draw.rect(okno, self.color, (x, y, self.width, self.height))

        print_text(message, x + 10, y + 10, font_size=font_size)

def print_text(message, x, y, font_color = (0, 0, 0), font_type = "source/starmap.ttf", font_size=30):
    font_text = pg.font.Font(font_type, font_size)
    text = font_text.render(message, True, font_color)
    okno.blit(text, (x, y))
def show_menu():
    start_btn = Button(288, 70, (8, 198, 212), (5, 169, 181))
    tic_tac_btn = Button(288, 70, (8, 198, 212), (5, 169, 181))
    jump_btn = Button(288, 70, (8, 198, 212), (5, 169, 181))
    show = True

    while show:
        if okno.get_size() == (300, 300):
            okno1 = pg.display.set_mode((800, 600))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
        okno.blit(land, (-900, -750))
        start_btn.draw(270, 100, 'RPG', rpg_game, 50)
        tic_tac_btn.draw(270, 200, 'TIC-TAC', tic_tac, 50)
        pg.display.update()
        clock.tick(60)


if __name__ == '__main__':
    show_menu()
