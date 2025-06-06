import pygame as pg
import sys
from .world import World
from .settings import TILE_SIZE
from .utils import draw_text
from .camera import Camera
from .hud import Hud


class Game:

    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.width, self.height = self.screen.get_size()
        self.zoom_factor = 3
        

        # hud
        self.hud = Hud(self.width, self.height)
        self.world = World(self.hud, 20, 20, self.width, self.height,"assets/graphics/map/sanJose.png")
        self.camera = Camera(self.width, self.height)

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(60)
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()

    def update(self):
        self.camera.update()
        self.hud.update()
        self.world.update(self.camera,self.zoom_factor)

    def draw(self):
        game_world_surface = pg.Surface((self.width, self.height)) 
        self.world.draw(game_world_surface, self.camera)
        scaled_world = pg.transform.scale(game_world_surface, (self.width * self.zoom_factor, self.height * self.zoom_factor)) #controls zoom level
        self.screen.blit(scaled_world, (0, 0)) 
        self.hud.draw(self.screen)


        draw_text(
            self.screen,
            'fps={}'.format(round(self.clock.get_fps())),
            25,
            (255, 255, 255),
            (10, 10)
        )

        
        pg.display.flip()

