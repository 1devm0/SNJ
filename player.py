import sys, math, random
import pygame as pg
from framework import *
from CONSTANTS import *

class player:
    def __init__(self, pos):
        self.img = pge_anim_img(PLAYER_SIZE, PLAYER_IMG_FOLDER, PLAYER_IMG_COLORKEY, PLAYER_STATES, PLAYER_STATE_LIST, scale=0)
        self.body = pge_rigidbody2d(PLAYER_SIZE, pos[0], pos[1])
        self.after_images_pos = []
        self.true_scroll = [0, 0]
        self.scroll = [0, 0]
        self.lmbtn_down = 0
        self.dash_multiplier = 1
        self.dash_timer = 0
        self.jump_timer = 0
        self.jump_count = 0
        self.initial_lvl_pos = pos
        self.ability = pge_circle((128, 128, 255), [-10000, -1000], 0)    
        self.ability_direction = 0
        self.ability_counter = 0
        self.particles = []
        self.flip = 0
        self.state = "idle"

    def set_initial_lvl_pos(self, pos):
        self.initial_lvl_pos = pos

    def handle_events(self, events):
        for e in events:
            if e.type == pg.QUIT:
                return 0
            if e.type == pg.KEYDOWN:
                if str(e.key) in PLAYER_KEYS:
                    self.body.movement[PLAYER_KEYS[str(e.key)]] = 1
                if (e.key == pg.K_w or e.key == pg.K_UP) and self.jump_count < 2:
                    self.body.vel[1] = -9
                    self.state = "jump"
                    self.jump_count += 1
                if e.key == pg.K_SPACE and self.dash_timer == 0:
                    self.dash_multiplier = 7
                    self.after_images_pos.clear()
                if e.key == pg.K_r:
                    self.body.rect.x, self.body.rect.y = self.initial_lvl_pos
            if e.type == pg.KEYUP:
                if str(e.key) in PLAYER_KEYS:
                    self.body.movement[PLAYER_KEYS[str(e.key)]] = 0
            if e.type == pg.MOUSEBUTTONDOWN:
                if e.button == 1:
                    self.lmbtn_down = 1
            if e.type == pg.MOUSEBUTTONUP:
                if e.button == 1:
                    self.lmbtn_down = 0
        return 1

    def update(self, game_state):
        self.true_scroll[0] += (self.body.rect.x - self.true_scroll[0] - DISPLAY_SIZE[0] / 2 + self.body.rect.w / 2) / 10
        self.true_scroll[1] += (self.body.rect.y - self.true_scroll[1] - DISPLAY_SIZE[1] / 2 + self.body.rect.h / 2) / 10

        self.scroll = [round(self.true_scroll[0]), round(self.true_scroll[1])]

        if self.dash_multiplier > 1:
            self.dash_timer += 1
        
        if self.dash_timer > 6:
            self.dash_multiplier = 1
            self.dash_timer = -60 * 3

        if self.dash_timer < 0:
            self.dash_timer += 1

        mpos = get_mouse_scaled_pos(game_state.window.get_current_size(), DISPLAY_SIZE)
        mrect = pg.Rect(mpos, (1, 1)) 

        # updating position, key remains same
        if self.lmbtn_down: 
            mpos = (mpos[0] + self.scroll[0], mpos[1] + self.scroll[1])
            self.ability_direction = math.atan2(mpos[1] - self.body.rect.y, mpos[0] - self.body.rect.x)
            self.ability.pos = [self.body.rect.x + self.body.rect.w / 2, self.body.rect.y + self.body.rect.h / 2]
            self.ability.pos = [self.ability.pos[0] + math.cos(self.ability_direction) * 30, self.ability.pos[1] + math.sin(self.ability_direction) * 30]
            self.ability.color = (95 - random.randint(-10, 10), 0, 160 - random.randint(-10, 10))
            self.ability.radius += 0.1

        self.ability.pos = [self.ability.pos[0] + math.cos(self.ability_direction) * 5, self.ability.pos[1] + math.sin(self.ability_direction) * 5]
        if self.ability.radius > 15:
            self.ability.radius = 15

        # get physic reccts around and then get colliding tiles and then track down specific tile by storing respective ids and then pop
        if self.ability.radius > 6:
            rects_around = game_state.lvl.phys_rects_around(self.ability.pos)
            ability_rect = pg.Rect((self.ability.pos[0] - self.ability.radius, self.ability.pos[1] - self.ability.radius), [self.ability.radius * 2, self.ability.radius * 2])
            positions = []
            for i in rects_around:
                if i.colliderect(ability_rect):
                    for l in range(20, 30):
                        self.particles.append(pge_circle((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), [i.x + random.randint(-1, 1) * l, i.y  + random.randint(-1, 1) * l], random.randint(6, 12)))
                    positions.append(str(int(i.x // game_state.lvl.tile_size)) + ';' + str(int(i.y // game_state.lvl.tile_size)))
                    self.scroll[0] += random.randint(-8, 8)
                    self.scroll[1] += random.randint(-8, 8)
            for pos in positions:
                if pos in positions:
                    try:
                        game_state.lvl.tilemap.pop(pos)
                    except:
                        pass
            e = 0
            for i in game_state.enemies:
                if i[0].rect.colliderect(ability_rect):
                    game_state.enemies.pop(e)
                    for l in range(20, 30):
                        self.particles.append(pge_circle((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), [i[0].rect.x + random.randint(-1, 1) * l, i[0].rect.y  + random.randint(-1, 1) * l], random.randint(6, 12)))
                    self.scroll[0] += random.randint(-12, 12)
                    self.scroll[1] += random.randint(-12, 12)
                e += 1

        if self.ability.radius:
            self.ability_counter += 1
        
        if self.ability_counter > 60 * 8:
            self.ability = pge_circle((128, 128, 255), [0, 0], 0)
            self.ability_counter = 0
        
        if self.body.vel[1] < 0:
            self.jump_timer += 1
        
        self.body.update(PLAYER_MOVE_SPEED * self.dash_multiplier * game_state.window.dt, game_state.lvl.phys_rects_around((self.body.rect.x, self.body.rect.y)))

        if self.body.collision["down"]:
            self.jump_timer = 0
            self.jump_count = 0

        if self.body.movement["right"]:
            self.flip = 0

        if self.body.movement["left"]:
            self.flip = 1
        
        if (self.body.movement["right"] or self.body.movement["left"]) and self.body.collision["down"]:
            self.state = "run"
            self.img.framerate = 6
            self.body.rect.w = 28
        else:
            if self.body.collision["down"]:
                self.state = "idle"
                self.img.framerate = 14
                self.body.rect.w = 18
            
        if self.body.vel[1] < 0 and self.body.collision["down"] != True:
            self.state = "jump"
            self.img.framerate = 300

        self.img.update(game_state.window.dt, self.state, self.flip)

        if self.dash_timer != 0 and len(self.after_images_pos) < 5:
            img_copy = self.img.current_img
            img_copy.set_alpha(60)
            self.after_images_pos.append((img_copy, self.body.rect.x, self.body.rect.y))
            i_x = self.body.rect.x
            i_y = self.body.rect.y
            for l in range(10, 20):
                self.particles.append(pge_circle((81, 45, 168), [i_x + random.randint(-1, 1) * l, i_y  + random.randint(-1, 1) * l], random.randint(3, 6)))


    def render(self, game_state):
        for i in range(0, len(self.after_images_pos) - 1):
            l = self.after_images_pos[i]
            if self.dash_timer < 0:
                l[0].set_alpha(l[0].get_alpha() - 1)
            game_state.display.blit(l[0], (l[1] - self.scroll[0], l[2] - self.scroll[1]))


        for i in self.particles:
            i.draw(game_state.display, self.scroll)
            i.radius -= 0.25     

        self.img.draw(game_state.display, (self.body.rect.x - self.scroll[0], self.body.rect.y - self.scroll[1]))
        self.body.dbg_draw(game_state.display, self.scroll)
        self.ability.draw(game_state.display, self.scroll)




 