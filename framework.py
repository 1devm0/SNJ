import pygame as pg
import math, sys, os
# Using Python 3.9.+ and Pygame == 2.1.2

def pge_init_pg():
    pg.init()
    pg.font.init()
    pg.mixer.init()
    pg.display.init()

class pge_win:
    def __init__(self, size, caption = "pg game", flags = 0, icon = None):
        self.size = size 
        self.caption = caption
        self.flags = flags
        self.icon = icon
        self.screen = pg.display.set_mode(self.size, self.flags)

        pg.display.set_caption(caption)

        self.fps = pg.time.Clock()

        if icon is not None:
            pg.display.set_icon(pg.image.load(self.icon).convert())
    
        self.display_size = pg.display.get_surface().get_size()
        self.dt = 0

    def cls(self, color = (0, 0, 0)):
        self.screen.fill(color)

    def get_current_size(self):
        self.display_size = pg.display.get_surface().get_size()
        return self.display_size


    def draw(self, main_surf=None, pos=[0, 0], scale=0, fps=60):
        self.screen.fill((0, 0, 255))

        self.display_size = pg.display.get_surface().get_size()
        if main_surf is not None and scale:
            pg.transform.scale(main_surf, self.get_current_size(), dest_surface=self.screen)

        if main_surf is not None and not scale:
            self.screen.blit(main_surf, pos)

        pg.display.update()
        self.dt = self.fps.tick(fps) / 1000

    def close(self):
        pg.quit()
        sys.exit()


class pge_mouse:
    def __init__(self, img = None, surf = None, visible = True):
        self.visible = visible

        self.img = img 
        self.surf = surf 

        pg.mouse.set_visible(self.visible)
        self.pos = pg.mouse.get_pos()

    def get_scaled_pos(self, win_size, surf_size):
        self.pos = pg.mouse.get_pos()
        return (self.pos[0] / (win_size[0] / surf_size[0]), self.pos[1] / (win_size[1] / surf_size[1]))

def get_mouse_scaled_pos(win_size, surf_size):
    pos = pg.mouse.get_pos()
    return (pos[0] / (win_size[0] / surf_size[0]), pos[1] / (win_size[1] / surf_size[1]))



class pge_circle:
    def __init__(self, surface, color, pos, radius):
        self.surface = surface
        self.color = color
        self.pos = pos
        self.radius = radius

    def draw(self):
        pg.draw.circle(self.surface, (255, 255, 255), self.pos, self.radius + 1)
        pg.draw.circle(self.surface, self.color, self.pos, self.radius)  

    def collision(self, otherCircle):
        xDif = self.pos[0] - otherCircle.pos[0]
        yDif = self.pos[1] - otherCircle.pos[1]

        distance = math.sqrt((xDif ** 2) + (yDif ** 2))

        if distance < self.radius:
            return True

class pge_fader:
    def __init__(self, size):
        self.fade = 0
        self.surf = pg.Surface(size)
        self.surf.fill((0, 0, 0))
        self.fade = int 
        self.alpha = int
        self.delta = int
        self.desired = int
    
    def set_val(self, delta, fade=0):
        self.fade = fade
        # fade in
        if self.fade == 0:
            self.alpha = 255
            self.delta = -delta 
            self.desired = 0
            self.surf.set_alpha(self.alpha)
        # fade out
        if self.fade == 1:
            self.alpha = 0
            self.delta = delta
            self.desired = 255
            self.surf.set_alpha(self.alpha)


    def draw(self, screen, pos, dt, start_fade=0):
        if start_fade:
            if self.alpha != self.desired:
                self.alpha += self.delta * dt
                self.surf.set_alpha(self.alpha)
                screen.blit(self.surf, pos)
            else:
                start_fade = 0

"""

PLAYER_IMG_FOLDER = "res/player/"
PLAYER_STATES = 3
PLAYER_STATE_LIST = [("idle", 1), ("run", 2), ("jump", 1)]
PLAYER_IMG_COLORKEY = (128, 128, 128, 255)
PLAYER_SIZE = (16, 16)
PLAYER_SPAWN_POS = (130, 656)
"""

class pge_anim_img:
    def __init__(self, size : tuple, img_folder, colorkey, number_of_states, states_list, framerate=30, scale=0):
        self.animated_imgs = {}
        for i in range(0, number_of_states):
            # adding the key into the dictionary
            self.animated_imgs[states_list[i][0]] = []
            # adding all the images 
            for n in range(0, states_list[i][1]):
                # load from folder, i.e res/player/idle/0.png
                img = pg.image.load(img_folder + states_list[i][0] + "/" + str(n) + ".png").convert_alpha()
                img.set_colorkey(colorkey)
                if scale:
                    img = pg.transform.scale(img, size)
                ## adding final modified image to the hash table
                self.animated_imgs[states_list[i][0]].append(img)
        self.current_img = None
        self.state = None 
        self.frames_passed = 0
        self.current_frame = 0
        self.flipped = 0
        # how many frames 1 image has to be displayed for
        self.framerate = framerate 

    def set_state(self, new_state):
        if self.state != new_state:
            self.state = new_state
            self.current_frame = 0

    def update(self, dt, state, flipped):
        self.set_state(state)
        self.flipped = flipped

        self.frames_passed += 1    

        if self.frames_passed > self.framerate:
            self.frames_passed = 0
            if self.current_frame < len(self.animated_imgs[self.state]) - 1:
                self.current_frame += 1
            else:
                self.current_frame = 0
        
        self.current_img = (self.animated_imgs[self.state][self.current_frame])
        self.current_img = pg.transform.flip(self.current_img, self.flipped, 0)

    def draw_rotated(self, display, topleft_pos, angle, colorkey):
        rotated_image = pg.transform.rotate(self.current_img, angle)
        rotated_image.set_colorkey(colorkey)
        new_rect = rotated_image.get_rect(center = self.current_img.get_rect(topleft = topleft_pos).center)

        display.blit(rotated_image, new_rect.topleft)

    def draw(self, display, pos):
        display.blit(self.current_img, pos)


class pge_static_img:
    def __init__(self, size : tuple, img_folder, colorkey, current_img_num, scale=0):
        self.size = size
        self.flipped = 0
        self.imgs = []
        for img in sorted(os.listdir(img_folder)):
            i = pg.image.load(img).convert()
            if scale:
                i = pg.transform.scale(i, size)
            self.imgs.append(i)
        self.current_img = self.imgs[current_img_num] 

    def draw_rotated(self, display, topleft_pos, angle, colorkey):
        rotated_image = pg.transform.rotate(self.current_img, angle)
        rotated_image.set_colorkey(colorkey)
        new_rect = rotated_image.get_rect(center = self.current_img.get_rect(topleft = topleft_pos).center)

        display.blit(rotated_image, new_rect.topleft)

    def draw(self, display, pos):
        display.blit(self.current_img, pos)

class pge_rigidbody2d:
    def __init__(self, size, x, y):
        self.rect = pg.Rect((x, y), size)
        self.movement = {
            "right" : 0,
            "left" : 0,
            "down" : 0,
            "up" : 0
        }
        self.collision = {
            "right" : 0,
            "left" : 0,
            "up" : 0,
            "down" : 0
        }
        self.vel = [0, 0]

    def update(self, move_speed, dt, tiles=None):
        self.vel = [0, 0]

        self.vel[0] += move_speed * dt * (self.movement["right"] - self.movement["left"]) 
        self.vel[1] += move_speed * dt * (self.movement["down"] - self.movement["up"]) 

        collision_types = {
            "top"     : False,
            "bottom"  : False,
            "right"   : False,
            "left"    : False
        }

        self.rect.x += self.vel[0]
        if tiles != None:
            hit_list = [tile for tile in tiles if self.rect.colliderect(tile)]
            for tile in hit_list:
                if self.vel[0] > 0:
                    self.rect.right = tile.left 
                    collision_types["right"] = True

                elif self.vel[0] < 0:
                    self.rect.left = tile.right
                    collision_types["left"] = True

        self.rect.y += self.vel[1]
        if tiles != None:
            hit_list = [tile for tile in tiles if self.rect.colliderect(tile)]
            for tile in hit_list:
                if self.vel[1] > 0:
                    self.rect.bottom = tile.top
                    collision_types["bottom"] = True

                if self.vel[1] < 0:
                    self.rect.top = tile.bottom 
                    collision_types["top"] = True
            
        self.collision = collision_types

    def dbg_draw(self, display, offset):
        new_rect = pg.Rect(self.rect.x - offset[0], self.rect.y - offset[1], self.rect.w, self.rect.h)
        pg.draw.rect(display, (255, 255, 255), new_rect, width=1)


NEIGHBORING_TILES = [
    (-1, 1), (0, 1),  (1, 1),
    (-1, 0), (0, 0),  (1, 0),
    (-1,-1), (0,-1),  (1,-1)
]
PHYSICS_TILES = {'1', '2', '3', '4'}

class pge_lvl:
    def __init__(self, filename, tile_images : dict, tile_size=8):
        self.lvl = load_map(filename)
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []
        self.tile_images = tile_images

        y_pos = 0
        for y in self.lvl:
            x_pos = 0
            for x in y:
                if x in PHYSICS_TILES:
                    self.tilemap[str(x_pos) + ';' + str(y_pos)] = {'type' : x, 'pos' : [x_pos, y_pos]}
                x_pos += 1
            y_pos += 1

    def get_player_pos(self, player_tile_num):
        y_pos = 0
        for y in self.lvl:
            x_pos = 0
            for x in y:
                if x == str(player_tile_num):
                    return (x_pos * self.tile_size, y_pos * self.tile_size) 
                x_pos += 1
            y_pos += 1

    def get_tiles_around(self, pos):
        tiles = []
        n_pos = [int(pos[0] // self.tile_size), int(pos[1] // self.tile_size)]
        for offset in NEIGHBORING_TILES:
            check_loc = str(n_pos[0] + offset[0]) + ';' + str(n_pos[1] + offset[1])
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles
    
    def phys_rects_around(self, pos):
        rects = []
        for t in self.get_tiles_around(pos):
            if t['type'] in PHYSICS_TILES:
                rects.append(pg.Rect(t['pos'][0] * self.tile_size, t['pos'][1] * self.tile_size, self.tile_size, self.tile_size))
        return rects

    def draw(self, display, scroll):
        for t in self.offgrid_tiles:
            display.blit(self.tile_images[t['type']], (t['pos'][0] - scroll[0], t['pos'][1] - scroll[1])) 

        for x in range(scroll[0] // self.tile_size, (scroll[0] + display.get_width()) // self.tile_size + 1):
            for y in range(scroll[1] // self.tile_size, (scroll[1] + display.get_height()) // self.tile_size + 1):
                loc = str(x) + ";" + str(y) 
                if loc in self.tilemap:
                    t = self.tilemap[loc]
                    display.blit(self.tile_images[t['type']], (t['pos'][0] * self.tile_size - scroll[0], t['pos'][1] * self.tile_size - scroll[1])) 

def load_map(path):
    return [list(row) for row in open(path + ".txt", "r").read().split("\n")]

fonts = {}
def text(text, color, size, x, y, font, surface):
    if size not in fonts:
        fonts[size] = pg.font.Font(font, size)

    surface.blit(fonts[size].render(text, False, color), (x, y))

