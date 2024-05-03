# Importing other files
import pygame as pg
import sys
import settings as s
from sprites import *
from random import randint
from os import path
from math import floor
# Creating game behavior

LEVEL1 = "map.txt"
LEVEL2 = "robbie.txt"
LEVEL3 = "tyler.txt"

class Game:
    def __init__(self):
        # Initializing Pyegame
        pg.init()
        # game window
        self.screen = pg.display.set_mode((s.WIDTH, s.HEIGHT))
        pg.display.set_caption(s.TITLE)
        # frame rate
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        # time variables
        self.dt = self.clock.tick(s.FPS) / 1000
        self.load_data()
        self.start_time = pg.time.get_ticks() 
        # Start time for the countdown
        # Countdown duration in seconds
        self.countdown_duration = 20 
        self.running = True
        self.paused = False
        self.on_start_screen = True  # Flag to indicate if on the start screen
        self.level = 1

    def load_data(self):
        game_folder = path.dirname(__file__)
        self.map_data = []
        with open(path.join(game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                self.map_data.append(line)
# adding sprites 
    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.power_ups = pg.sprite.Group()
        self.foods = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.portals = pg.sprite.Group()
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'U':
                    Coin(self, col, row)
                if tile == 'F':
                    Food(self, col, row)
                # if tile == 'M':
                #     Mob(self, col, row)

    def run(self):
        while self.running:
            self.show_start_screen()
            self.new()  # This line should only be called after the start screen is displayed
            self.run_game()

    def run_game(self):
        self.playing = True
        self.on_start_screen = False  # No longer on start screen
        while self.playing:
            if self.paused:
                self.paused_screen()
            else:
                self.dt = self.clock.tick(s.FPS) / 1000
                self.events()
                self.update()
                self.draw()
                if not self.on_start_screen:  # Only check countdown if not on start screen
                    self.check_countdown()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        self.all_sprites.update()
        self.portal_spawn()

    def draw_grid(self):
        for x in range(0, s.WIDTH, s.TILESIZE):
            pg.draw.line(self.screen, s.LIGHTGREY, (x, 0), (x, s.HEIGHT))
        for y in range(0, s.WIDTH, s.TILESIZE):
            pg.draw.line(self.screen, s.LIGHTGREY, (0, y), (s.WIDTH, y))

    def draw(self):
        self.screen.fill(s.BLACK)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        self.draw_text(self.screen, "Hello world...", 42, s.BLACK, 1, 1)

        # adding countdown timer, but only if not on start screen
        if not self.on_start_screen:
            time_remaining = max(0, self.countdown_duration - (pg.time.get_ticks() - self.start_time) // 1000)
            self.draw_text(self.screen, f"Time Remaining: {time_remaining}", 24, WHITE, WIDTH // 2, HEIGHT - 30)

        pg.display.flip()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.paused = not self.paused  # Toggle pause state

    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        surface.blit(text_surface, text_rect)

    def check_countdown(self):
        time_remaining = max(0, self.countdown_duration - (pg.time.get_ticks() - self.start_time) // 1000)
        if time_remaining == 0:
            self.quit()

    def show_start_screen(self):
        self.screen.fill(BLACK)
        self.draw_text(self.screen,"Press Any Button To Start", 36, WHITE, WIDTH // 2, HEIGHT // 2 - 50)
        self.draw_text(self.screen, "Press Any Key To Start", 24, WHITE, WIDTH // 2, HEIGHT // 2)
        pg.display.flip()
        waiting = True
        while waiting:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False

    def paused_screen(self):
        self.screen.fill(BLACK)
        self.draw_text(self.screen, "Paused", 48, WHITE, WIDTH // 2, HEIGHT // 2)
        pg.display.flip()
        waiting = True
        while waiting:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE: 
                        self.paused = not self.paused  # Resume the game
                        waiting = False
    def portal_spawn(self):
        if self.level == 1 and self.player.coin == 5:
            Markiplier(self,30,16)
            print("Hello everybody")
        if self.level == 2 and self.player.coin == 11:
            Markiplier(self,30,16)
            print("Hello everybody")
        if s.markiplier == True:
            self.level += 1
            self.change_level(self.level)
            s.markiplier = False

    def change_level(self,lvl): #level changing function
        current_coin_count = self.player.coin
        current_hp = self.player.hitpoints
        if lvl == 2:
            self.lvl = LEVEL2
        elif lvl == 3:
            self.lvl = LEVEL3
        

        for sprite in self.all_sprites:
            sprite.kill() #Killing sprites
        self.map_data = [] #Reset map data
        # Load new level
        with open(path.join(self.game_folder, self.lvl), 'rt') as f:
            for line in f:
                print(line)
                self.map_data.append(line) #Creating new map data from the new map.txt file

        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'U':
                    Coin(self, col, row)
                if tile == 'F':
                    Food(self, col, row)
                # if tile == 'M':
                #     Mob(self, col, row)

        self.player.coin = current_coin_count
        self.player.hitpoints = current_hp
            
        


g = Game()
g.new()
g.run()
