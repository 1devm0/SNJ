import pygame as pg
from framework import * 

pge_init_pg()

WINDOW_SIZE = (1280, 720) 
DISPLAY_SIZE = (640, 360)

PLAYER_IMG_FOLDER = "res/player/"
PLAYER_STATES = 3
PLAYER_STATE_LIST = [("idle", 2), ("run", 2), ("jump", 1)]
PLAYER_IMG_COLORKEY = (128, 128, 128, 255)
PLAYER_SIZE = (16, 16)
PLAYER_MOVE_SPEED = 200

PLAYER_KEYS = {
    str(pg.K_d) : "right",
    str(pg.K_a) : "left",
    str(pg.K_s) : "down",
    str(pg.K_w) : "up"
}

