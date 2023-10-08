import sys, math, random
import pygame as pg
from framework import *
from CONSTANTS import *

pge_init_pg()

window = pge_win(WINDOW_SIZE, "SNJ", pg.RESIZABLE) 
display = pg.Surface(DISPLAY_SIZE)
fader = pge_fader(DISPLAY_SIZE)
fader.set_val(40, 0)

tile_surf = pg.Surface((32, 32)).convert()
tile_surf.fill((180, 20, 230))
tile_images = { '1' : tile_surf, '2' : tile_surf, '3' : tile_surf, '4' : tile_surf }

true_scroll = [0, 0]
scroll = [0, 0]

running = 1

player_img = pge_anim_img(PLAYER_SIZE, PLAYER_IMG_FOLDER, PLAYER_IMG_COLORKEY, PLAYER_STATES, PLAYER_STATE_LIST, scale=1)
player_body = pge_rigidbody2d(PLAYER_SIZE, 100, 100)

player_afterimages_pos = []

lvl = pge_lvl("res/maps/0", tile_images, tile_size=32)
player_body_pos = lvl.get_player_pos(6)

player_body.rect.x = player_body_pos[0]
player_body.rect.y = player_body_pos[1]

mlbtn_down = 0

dash_multiplier = 1.5
dash_timer = 0

while running:
    ### game events
    for e in pg.event.get():
        if e.type == pg.QUIT:
            running = 0
        if e.type == pg.KEYDOWN:
            if str(e.key) in PLAYER_KEYS:
                player_body.movement[PLAYER_KEYS[str(e.key)]] = 1

            if e.key == pg.K_e and dash_timer == 0:
                dash_multiplier = 7
                player_afterimages_pos.clear()

        if e.type == pg.KEYUP:
            if str(e.key) in PLAYER_KEYS:
                player_body.movement[PLAYER_KEYS[str(e.key)]] = 0


        if e.type == pg.MOUSEBUTTONDOWN:
            if e.button == 1:
                mlbtn_down = 1
        if e.type == pg.MOUSEBUTTONUP:
            if e.button == 1:
                mlbtn_down = 0

    ### game update
    true_scroll[0] += (player_body.rect.x - true_scroll[0] - DISPLAY_SIZE[0] / 2 + player_body.rect.w / 2) / 10
    true_scroll[1] += (player_body.rect.y - true_scroll[1] - DISPLAY_SIZE[1] / 2 + player_body.rect.h / 2) / 10 
    scroll = [round(true_scroll[0]), round(true_scroll[1])]

    mpos = get_mouse_scaled_pos(window.get_current_size(), DISPLAY_SIZE)
    mrect = pg.Rect(mpos, (1, 1))

    if dash_multiplier > 1.5:
        dash_timer += 1 

    if dash_timer > 5:
        dash_multiplier = 1.5
        dash_timer = -60 * 4

    if dash_timer < 0:
        dash_timer += 1

    # uppdating the position but key remains the same
    if mlbtn_down:
        mpos = (mpos[0] + scroll[0], mpos[1] + scroll[1])
        pos = (int(mpos[0] // lvl.tile_size), int(mpos[1] // lvl.tile_size))
        strpos = str(pos[0]) + ';' + str(pos[1])
        if strpos in lvl.tilemap:
            try:
                lvl.tilemap.pop(strpos)
                # new_strpos = str(pos[0] + 1) + ';' + str(pos[1])
                # if new_strpos not in lvl.tilemap:
                    # tile = lvl.tilemap[strpos]
                    # lvl.tilemap.pop(strpos)
                    # tile['pos'] = [tile['pos'][0] + 1, tile['pos'][1]]
                    # lvl.tilemap[new_strpos] = tile
            except:
                pass

    player_body.update(PLAYER_MOVE_SPEED * dash_multiplier, window.dt, lvl.phys_rects_around((player_body.rect.x, player_body.rect.y)))

    player_img.update(window.dt, "idle", 0)

    if dash_timer != 0 and len(player_afterimages_pos) < 5:
        img_copies = player_img.current_img
        img_copies.set_alpha(60)
        player_afterimages_pos.append((img_copies, player_body.rect.x, player_body.rect.y))

    ### game display update
    display.fill((135, 206, 235))
        
    lvl.draw(display, scroll)

    for i in range(0, len(player_afterimages_pos) - 1):
        l = player_afterimages_pos[i]
        if dash_timer < 0:
            l[0].set_alpha(l[0].get_alpha() - 1)
        display.blit(l[0], (l[1] - scroll[0], l[2] - scroll[1]))

    player_body.dbg_draw(display, scroll)
    player_img.draw(display, (player_body.rect.x - scroll[0], player_body.rect.y - scroll[1]))

    mssrect = mrect
    mssrect.x -= scroll[0]
    mssrect.y -= scroll[1]
    pg.draw.rect(display, (255, 255, 255), mssrect, width=1)

    fader.draw(display, (0, 0), window.dt, 255)

    window.draw(display, (0, 0), 1)

pg.quit()
sys.exit()