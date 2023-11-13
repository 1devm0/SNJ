import sys, math, random
import pygame as pg
from framework import *
from CONSTANTS import *
from player import player

pge_init_pg()

class Game:
    def __init__(self):
        self.window = pge_win(WINDOW_SIZE, "SNJ", pg.RESIZABLE) 
        self.display = pg.Surface(DISPLAY_SIZE)
        self.fader = pge_fader(DISPLAY_SIZE)
        self.fader.set_val(40, 0)

        self.tile_surf = pg.image.load("res/tile_two.png").convert()
        self.tile_images = { '1' : self.tile_surf, '2' : self.tile_surf, '3' : self.tile_surf, '4' : self.tile_surf }

        self.running = 1
        self.lvl = pge_lvl("res/maps/0", self.tile_images, tile_size=40)

        self.enemy_positions = self.lvl.get_enemy_pos(5)
        self.enemy_img = pge_anim_img(ENEMY_0_SIZE, ENEMY_0_IMG_FOLDER, (0, 0, 0), ENEMY_0_STATES, ENEMY_0_STATE_LIST) 
        self.enemies = []
        self.enemy_health = [] 
        for i in self.enemy_positions:
            self.enemies.append([pge_rigidbody2d((40, 40), i[0], i[1]), random.randint(10, 30)])

        self.squares_background = []
        for i in range(0, 50):
            self.size = random.randint(10, 30)
            self.surf = pg.Surface((self.size, self.size), pg.SRCALPHA)
            self.surf.fill((0, 100, 255, random.randint(30, 128)))
            pg.draw.rect(self.surf, (255, 255, 255, random.randint(0, 128)), pg.Rect(0, 0, self.size, self.size), width=1)
            self.surf = pg.transform.rotate(self.surf, random.randint(-90, -10))
            self.squares_background.append([self.surf, [random.randint(0, DISPLAY_SIZE[0]), random.randint(-DISPLAY_SIZE[1], DISPLAY_SIZE[1])], random.randint(5, 20)])

        self.player = player(self.lvl.get_player_pos(6))

    def handle_events(self):
        events = pg.event.get()
        self.running = self.player.handle_events(events)

    def update(self):
        self.player.update(self)
        for i in self.enemies:
            i[0].update(ENEMY_0_MOVE_SPEED * self.window.dt, self.lvl.phys_rects_around((i[0].rect.x, i[0].rect.y)))
        self.enemy_img.update(self.window.dt, "idle", 0)

    def render(self):
        self.display.fill((135, 206, 235))

        for i in range(0, len(self.squares_background) - 1):
            self.display.blit(self.squares_background[i][0], self.squares_background[i][1])
            self.squares_background[i][1][1] += 1
            if self.squares_background[i][1][1] > DISPLAY_SIZE[1]:
                self.squares_background[i][1][1] = -DISPLAY_SIZE[1] + 10

        self.lvl.draw(self.display, self.player.scroll)

        for i in self.enemies:
            self.enemy_img.draw(self.display, (i[0].rect.x - self.player.scroll[0], i[0].rect.y - self.player.scroll[1]))
            i[0].dbg_draw(self.display, self.player.scroll)
            pg.draw.rect(self.display, (255, 50, 50), pg.Rect(i[0].rect.x - self.player.scroll[0], i[0].rect.y - self.player.scroll[1] - 10, i[1], 5))

        self.player.render(self)


        self.fader.draw(self.display, (0, 0), self.window.dt, 255)
        self.window.draw(self.display, (0, 0), 1)
        pg.display.set_caption(str(int(self.window.fps.get_fps())))


game = Game()
while game.running:
    game.handle_events()
    game.update()
    game.render()


pg.quit()
sys.exit()

# implement red, blue with timer