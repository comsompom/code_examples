import pyxel
import random

MAIN_TITLE = 'Smert Voragam! Zyve Belarus! Slava Ukraine!'
MAIN_WIDTH = 220
MAIN_HEIGHT = 110
MAIN_GAME_FRAME = 4

PLAYER_WIDTH = 12
PLAYER_HEIGHT = 10
PLAYER_SPEED = 1
MAX_PLAYER_SPEED = 10
INIT_ENEMY_NUMBER = 4
BULLET_SPEED = 3

TOTAL_SCORE = 0
NEXT_LEVEL_SCORE = 2_000

MENU_TEXT_LEVEL = 'Level: '
MENU_TEXT_SCORE = 'Score: '
MENU_TEXT_BULLETS = 'Bullets: '
MENU_TEXT_ENEMY = 'Govno: '
MENU_COLOR = 9

SCENE_NAME_START = 0
SCENE_NAME_MAIN_ZYVE = 1
SCENE_NAME_MAIN_SLAVA = 2
SCENE_NAME_GAMEOVER = 3
SCENE_MAIN_TEXT_ZYVE = '1 - ZYVE BELARUS'
SCENE_MAIN_TEXT_SLAVA = '2 - SLAVA UKRAINE'

START_POINT_X = 0 + MAIN_GAME_FRAME
START_POINT_Y = MAIN_HEIGHT - PLAYER_HEIGHT - MAIN_GAME_FRAME
ENEMY_START_X = MAIN_WIDTH - MAIN_GAME_FRAME - PLAYER_HEIGHT - 2

bullets = []
enemies = []


class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.bl_speed = BULLET_SPEED
        self.is_alive = True
        bullets.append(self)

    def update(self):
        self.x += self.bl_speed
        if self.x + self.bl_speed >= MAIN_WIDTH:
            self.is_alive = False

    def draw(self):
        pyxel.line(self.x + PLAYER_WIDTH, self.y + PLAYER_HEIGHT - 3,
                   self.x + PLAYER_WIDTH + 2, self.y + PLAYER_HEIGHT - 3, 10)


class PlayerShoot:
    def __init__(self):
        self.x_bul = 0

    def update(self):
        while self.x_bul <= MAIN_WIDTH:
            self.x_bul += 1

    def draw(self, x, y):
        pyxel.line(x + PLAYER_WIDTH, y + PLAYER_HEIGHT - 3,
                   x + PLAYER_WIDTH + 2, y + PLAYER_HEIGHT - 3, 10)


class Player:
    def __init__(self, x, y):
        self.pl_x = x
        self.pl_y = y
        self.pl_width = PLAYER_WIDTH
        self.pl_height = PLAYER_HEIGHT
        self.pl_speed = PLAYER_SPEED
        self.shoot = False
        self.bullet_counter = 0
        self.player_shoot = PlayerShoot()

    def update(self):
        # player key control movement arrow keys
        if pyxel.btn(pyxel.KEY_RIGHT) and self.pl_x <= MAIN_WIDTH - 12:
            self.pl_x += self.pl_speed
        if pyxel.btn(pyxel.KEY_LEFT) and self.pl_x >= 2:
            self.pl_x -= self.pl_speed
        if pyxel.btn(pyxel.KEY_UP) and self.pl_y >= MAIN_GAME_FRAME + self.pl_height + self.pl_speed:
            self.pl_y -= self.pl_speed
        if pyxel.btn(pyxel.KEY_DOWN) and self.pl_y <= MAIN_HEIGHT - 16:
            self.pl_y += self.pl_speed
        self.pl_x = max(self.pl_x, MAIN_GAME_FRAME)
        self.pl_x = min(self.pl_x, pyxel.width - self.pl_width - MAIN_GAME_FRAME)
        self.pl_y = max(self.pl_y, MAIN_GAME_FRAME)
        self.pl_y = min(self.pl_y, pyxel.height - self.pl_height - MAIN_GAME_FRAME)

        # player speed control A-Speed UP, Z-Speed Down
        if pyxel.btn(pyxel.KEY_A) and self.pl_speed <= MAX_PLAYER_SPEED:
            self.pl_speed += 1
            self.pl_speed = min(self.pl_speed, MAX_PLAYER_SPEED)
        if pyxel.btn(pyxel.KEY_Z) and self.pl_speed > 1:
            self.pl_speed -= 1
            self.pl_speed = min(self.pl_speed, 1)

        # player shoot bullet
        if pyxel.btn(pyxel.KEY_SPACE):
            self.shoot = True
            Bullet(self.pl_x, self.pl_y)

    def draw(self):
        pyxel.blt(self.pl_x, self.pl_y, 0, 0, 0, 10, 12)
        if self.shoot:
            self.bullet_counter += 1
            self.player_shoot.draw(self.pl_x, self.pl_y)
            self.shoot = False


class Enemy:
    def __init__(self):
        self.en_x = ENEMY_START_X
        self.en_y = random.randint(MAIN_GAME_FRAME, MAIN_HEIGHT)
        self.move_x = 0
        self.move_y = 0
        self.is_alive = True
        self.is_killed = False
        self.is_gone = False
        enemies.append(self)

    def enemy_restart(self):
        self.is_alive = False
        self.en_x = ENEMY_START_X
        self.en_y = random.randint(MAIN_GAME_FRAME, MAIN_HEIGHT)

    def update(self):
        if self.en_x == ENEMY_START_X:
            self.is_killed = False
            self.is_gone = False
        self.move_x = random.randint(1, 2)
        self.move_y = 1 - random.randint(0, 2)
        self.en_x -= self.move_x
        self.en_y -= self.move_y
        self.en_y = max(self.en_y, (MAIN_GAME_FRAME + PLAYER_HEIGHT + 2))
        self.en_y = min(self.en_y, MAIN_HEIGHT - 8)
        # check the enemy killed
        for check in range(8):
            if pyxel.pget(self.en_x - 1, self.en_y + check) == 10:
                self.is_killed = True
                self.enemy_restart()
        # restart enemy because go to the end
        if self.en_x <= MAIN_GAME_FRAME:
            self.is_gone = True
            self.enemy_restart()

    def draw(self, g=1):
        pyxel.blt(self.en_x, self.en_y, 0, 16 + 8 * g, 0, 8, 8)

class Background:
    def __init__(self):
        self.menu_line_y = PLAYER_HEIGHT + MAIN_GAME_FRAME - 2
        self.level_end_tab = len(MENU_TEXT_LEVEL) * 6
        self.bullets_tab = self.level_end_tab + len(MENU_TEXT_BULLETS) * 7
        self.enemy_score = self.bullets_tab + len(MENU_TEXT_ENEMY) * 8

    def draw(self):
        pyxel.line(0, self.menu_line_y, MAIN_WIDTH, self.menu_line_y, 10)
        pyxel.line(self.level_end_tab, self.menu_line_y, self.level_end_tab, 0, 10)
        pyxel.line(self.bullets_tab, self.menu_line_y, self.bullets_tab, 0, 10)
        pyxel.line(self.enemy_score, self.menu_line_y, self.enemy_score, 0, 10)


class Defender:
    def __init__(self):
        pyxel.init(MAIN_WIDTH, MAIN_HEIGHT, title=MAIN_TITLE)
        pyxel.load("defender.pyxres")
        self.score = 0
        self.enemy_score = 0
        self.current_scene = SCENE_NAME_START
        self.level = self.score // NEXT_LEVEL_SCORE + 1
        self.enemy_number = INIT_ENEMY_NUMBER + self.level
        self.player = Player(START_POINT_X, START_POINT_Y)
        self.background = Background()
        self.bchb_y_up = MAIN_HEIGHT / 2 - 5
        self.bchb_y_dn = MAIN_HEIGHT / 2 + 5
        self.flag_x_end = MAIN_GAME_FRAME + 20
        self.ukr_y_up = MAIN_HEIGHT / 2 - 3
        self.ukr_y_dn = MAIN_HEIGHT / 2 + 4

        pyxel.run(self.update, self.draw)

    def check_enemies(self):
        if len(enemies) < self.enemy_number:
            Enemy()

    def update_enemies(self):
        for enemy in enemies:
            enemy.update()
            if self.current_scene == SCENE_NAME_MAIN_ZYVE:
                if enemy.en_x <= self.flag_x_end:
                    for check in range(8):
                        if self.bchb_y_up <= enemy.en_y + check <= self.bchb_y_dn + 5:
                            self.current_scene = SCENE_NAME_GAMEOVER
            if self.current_scene == SCENE_NAME_MAIN_SLAVA:
                if enemy.en_x <= self.flag_x_end:
                    for check in range(8):
                        if self.ukr_y_up <= enemy.en_y + check <= self.ukr_y_dn + 7:
                            self.current_scene = SCENE_NAME_GAMEOVER
            if enemy.is_gone:
                self.enemy_score += 1
            if enemy.is_killed:
                self.score += 10
            self.level = self.score // NEXT_LEVEL_SCORE + 1
            self.enemy_number = INIT_ENEMY_NUMBER + self.level

    def draw_enemies(self):
        for enemy in enemies:
            enemy.draw(self.current_scene - 1)

    def update_bullets(self):
        for idx, bullet in enumerate(bullets):
            bullet.update()
            if bullet.is_alive == False:
                del bullets[idx]

    def draw_bullets(self):
        for bullet in bullets:
            bullet.draw()

    def draw_menu_items(self):
        pyxel.text(MAIN_GAME_FRAME, MAIN_GAME_FRAME,
                   f'{MENU_TEXT_LEVEL}{self.level}', MENU_COLOR)
        pyxel.text(MAIN_GAME_FRAME + 42, MAIN_GAME_FRAME,
                   f'{MENU_TEXT_SCORE}{self.score}', MENU_COLOR)
        pyxel.text(MAIN_GAME_FRAME + 105, MAIN_GAME_FRAME,
                   f'{MENU_TEXT_BULLETS}{self.player.bullet_counter}', MENU_COLOR)
        pyxel.text(MAIN_GAME_FRAME + 170, MAIN_GAME_FRAME,
                   f'{MENU_TEXT_ENEMY}{self.enemy_score}', MENU_COLOR)

    def draw_movements(self):
        pyxel.cls(0)
        self.player.draw()
        self.background.draw()
        self.draw_enemies()
        self.draw_bullets()

    def draw_main_scene_zyve(self):
        self.draw_movements()
        # flag drawing
        pyxel.rect(MAIN_GAME_FRAME, self.bchb_y_up, 20, 5, 7)
        pyxel.rect(MAIN_GAME_FRAME, MAIN_HEIGHT / 2, 20, 5, 8)
        pyxel.rect(MAIN_GAME_FRAME, self.bchb_y_dn, 20, 5, 7)
        # draw menu items
        self.draw_menu_items()

    def draw_main_scene_slava(self):
        self.draw_movements()
        # flag drawing
        pyxel.rect(MAIN_GAME_FRAME, self.ukr_y_up, 20, 7, 12)
        pyxel.rect(MAIN_GAME_FRAME, self.ukr_y_dn, 20, 7, 10)
        # draw menu items
        self.draw_menu_items()

    def update_main_scene_zyve(self):
        self.check_enemies()
        self.player.update()
        self.update_enemies()
        self.update_bullets()
        if pyxel.btnp(pyxel.KEY_Q):
            self.current_scene = SCENE_NAME_GAMEOVER

    def draw_start_scene(self):
        pyxel.cls(0)
        pyxel.text(5, 5, "Game Control keys:", 9)
        pyxel.text(10, 15, " - Arrow keys for player movement", 9)
        pyxel.text(10, 25, " - Space for shoot", 9)
        pyxel.text(10, 35, " - A - Player speed UP", 9)
        pyxel.text(10, 45, " - Z - Player speed DOWN", 9)
        pyxel.text(5, 55, "Your goal is protect the Flag from enemy", 8)
        pyxel.text(5, 65, "For start Game choose option and press 1 or 2", 8)
        pyxel.text(MAIN_WIDTH / 2 - len(SCENE_MAIN_TEXT_ZYVE) * 2, MAIN_HEIGHT / 2 + 20,
                   SCENE_MAIN_TEXT_ZYVE, pyxel.frame_count % 16)
        pyxel.text(MAIN_WIDTH / 2 - len(SCENE_MAIN_TEXT_ZYVE) * 2, MAIN_HEIGHT / 2 + 30,
                   SCENE_MAIN_TEXT_SLAVA, pyxel.frame_count % 16)

    def update_start_scene(self):
        if pyxel.btnp(pyxel.KEY_1) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_X):
            self.current_scene = SCENE_NAME_MAIN_ZYVE
        if pyxel.btnp(pyxel.KEY_2) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_X):
            self.current_scene = SCENE_NAME_MAIN_SLAVA

    def draw_gameover_scene(self):
        pyxel.cls(0)
        pyxel.text(90, 5, "GAME OVER!", 9)
        pyxel.text(10, 15, f" - You finished with level: {self.level}", 9)
        pyxel.text(10, 25, f" - You Score: {self.score}", 9)
        pyxel.text(10, 35, f" - You spend: {self.player.bullet_counter} bullets", 9)
        pyxel.text(10, 45, f" - Enemies alive: {self.enemy_score}", 9)
        efficiency_b = round((self.score / (self.player.bullet_counter + 1)), 3)
        efficiency_k = (self.score / 10) * (self.score / 10 + self.enemy_score) / 100
        pyxel.text(10, 55, f" - Your Efficiency as Shooter: {efficiency_b}", 10)
        pyxel.text(10, 65, f" - Your Efficiency as Defender: {efficiency_k}", 10)
        pyxel.text(MAIN_WIDTH / 2 - len(SCENE_MAIN_TEXT_ZYVE) * 2, MAIN_HEIGHT / 2 + 20,
                   SCENE_MAIN_TEXT_ZYVE, pyxel.frame_count % 16)
        pyxel.text(MAIN_WIDTH / 2 - len(SCENE_MAIN_TEXT_ZYVE) * 2, MAIN_HEIGHT / 2 + 30,
                   SCENE_MAIN_TEXT_SLAVA, pyxel.frame_count % 16)

    def reset_lists(self):
        bullets.clear()
        enemies.clear()

    def update_gameover_scene(self):
        if pyxel.btnp(pyxel.KEY_1) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_X):
            self.reset_lists()
            self.current_scene = SCENE_NAME_MAIN_ZYVE
        if pyxel.btnp(pyxel.KEY_2) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_X):
            self.reset_lists()
            self.current_scene = SCENE_NAME_MAIN_SLAVA

    def update(self):
        if self.current_scene == SCENE_NAME_START:
            self.update_start_scene()
        if self.current_scene == SCENE_NAME_MAIN_ZYVE:
            self.update_main_scene_zyve()
        if self.current_scene == SCENE_NAME_MAIN_SLAVA:
            self.update_main_scene_zyve()
        if self.current_scene == SCENE_NAME_GAMEOVER:
            self.update_gameover_scene()

    def draw(self):
        if self.current_scene == SCENE_NAME_START:
            self.draw_start_scene()
        if self.current_scene == SCENE_NAME_MAIN_ZYVE:
            self.draw_main_scene_zyve()
        if self.current_scene == SCENE_NAME_MAIN_SLAVA:
            self.draw_main_scene_slava()
        if self.current_scene == SCENE_NAME_GAMEOVER:
            self.draw_gameover_scene()


Defender()
