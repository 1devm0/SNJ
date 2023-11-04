import pygame as pg
from framework import * 

pge_init_pg()

WINDOW_SIZE = (1280, 720) 
DISPLAY_SIZE = (640, 360)

PLAYER_IMG_FOLDER = "res/player/"
PLAYER_STATES = 3
PLAYER_STATE_LIST = [("idle", 2), ("run", 6), ("jump", 1)]
PLAYER_IMG_COLORKEY = (158, 158, 158, 255)
PLAYER_SIZE = (18, 32)
PLAYER_MOVE_SPEED = 200 * 1.25

PLAYER_KEYS = {
    str(pg.K_d) : "right",
    str(pg.K_a) : "left",
    str(pg.K_s) : "down",
    str(pg.K_RIGHT) : "right",
    str(pg.K_LEFT) : "left",
    str(pg.K_DOWN) : "down"
}

ENEMY_0_IMG_FOLDER = "res/enemy_0/"
ENEMY_0_STATES = 1
ENEMY_0_STATE_LIST = [("idle", 2)]
ENEMY_0_SIZE = (40, 40)
ENEMY_0_MOVE_SPEED = 50


