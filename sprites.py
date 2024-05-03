# This file was created by: Rameil Khoshaba

# import modules
import pygame as pg
from pygame.sprite import Sprite
from settings import *
from os import path # create a player class
class Player(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(SKYBLUE)
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.hitpoints = 100
        self.last_dash_time = 0
        self.dash_cooldown = 1000  # Cooldown time
        self.dash_distance = 128  # distance 
        self.speed = 8
        self.coin = 0

    # def move(self, dx=0, dy=0):
    #     self.x += dx
    #     self.y += dy
        
    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -PLAYER_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = PLAYER_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -PLAYER_SPEED
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = PLAYER_SPEED
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071

    def collide_with_obj(self, group, kill, desc):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits and desc == "food":
            print("I collided with food")
            # self.image.fill(GREEN)
        if hits and desc == "powerup":
            print("I collided with powerup")
            self.coin += 1
        if hits and desc == "markiplier":
            print("I collided with markiplier")
            # self.image.fill(GREEN)
            markiplier = True

    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y
    def dash(self):
        self.last_dash_time = pg.time.get_ticks()
        if self.vx >= 0:
            self.x += self.dash_distance

        if self.vy >= 0:
            self.y += self.dash_distance

        if self.vx <= 0:
            self.x -= self.dash_distance
            
        if self.vy <= 0:
            self.y -= self.dash_distance

    def update(self):
        # self.rect.x = self.x * TILESIZE
        # self.rect.y = self.y * TILESIZE
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        # add x collision later
        self.collide_with_walls('x')
        self.rect.y = self.y
        # add y collision later
        self.collide_with_walls('y')
        self.collide_with_obj(self.game.power_ups, True, "powerup")
        self.collide_with_obj(self.game.foods, True, "food")
        self.collide_with_obj(self.game.mobs, True, "mob")
        self.collide_with_obj(self.game.portals, True, "markiplier")
        self.rect.width = self.rect.width
        self.rect.height = self.rect.height
          # Dash when 'e' is pressed and moving in a certain direction
        keys = pg.key.get_pressed()
        if keys[pg.K_e] and (self.vx != 0 or self.vy != 0):
            now = pg.time.get_ticks()
            if now - self.last_dash_time > self.dash_cooldown:
                self.dash()
        
# creating wall class
class Wall(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(DARKGREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Coin(Sprite):
    def __init__(self, game, x, y):
        # add powerup groups later....
        self.groups = game.all_sprites, game.power_ups
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Food(Sprite):
    def __init__(self, game, x, y):
        # add powerup groups later....
        self.groups = game.all_sprites, game.foods
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(LIGHTGREY)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Markiplier(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.portals
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

    