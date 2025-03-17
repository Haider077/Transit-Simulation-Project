
import pygame as pg
from .utils import draw_text


class Hud:

    def __init__(self, width, height):

        self.width = width
        self.height = height

        self.hud_colour = (50, 50, 50, 255)
        pg.font.init() # you have to call this at the start, 
                        # if you want to use this module.
        my_font = pg.font.SysFont('monogram medium', 70)
        my_font1 = pg.font.Font('../monogram.ttf', 70) #Load font object.
        self.text_surface = my_font1.render('Building Menu', False, (255, 255, 255))
        text = "  MINI-MAP :"
        text.splitlines()
        self.text_surface1 = my_font1.render(text, False, (255, 255, 255))
        # resouces hud
        self.resouces_surface = pg.Surface((width, height * 0.02), pg.SRCALPHA)
        self.resources_rect = self.resouces_surface.get_rect(topleft=(0, 0))
        self.resouces_surface.fill(self.hud_colour)

        # building hud
        
        self.build_surface = pg.Surface((width * 0.15, height * 0.25), pg.SRCALPHA)
        self.build_rect = self.build_surface.get_rect(topleft=(self.width * 0.84, self.height * 0.74 + 1))
        self.build_surface.fill(self.hud_colour)

        # select hud
        self.select_surface = pg.Surface((width * 0.3, height * 0.2), pg.SRCALPHA)
        self.select_rect = self.select_surface.get_rect(topleft=(self.width * 0.35, self.height * 0.79))
        self.select_surface.fill(self.hud_colour)

        # instructions menu
        self.instructions = pg.Surface((width * 0.15, height * 0.25), pg.SRCALPHA)
        self.select_rect = self.select_surface.get_rect(topleft=(self.width * 0.35, self.height * 0.79))
        self.instructions.fill(self.hud_colour)


        self.images = self.load_images()
        self.tiles = self.create_build_hud()

        self.selected_tile = None

    def create_build_hud(self):

        render_pos = [self.width * 0.84 + 10, self.height * 0.74 + 10]
        object_width = self.build_surface.get_width() // 3

        tiles = []

        for image_name, image in self.images.items():

            pos = render_pos.copy()
            image_tmp = image.copy()
            image_scale = self.scale_image(image_tmp, w=object_width)
            rect = image_scale.get_rect(topleft=pos)

            tiles.append(
                {
                    "name": image_name,
                    "icon": image_scale,
                    "image": self.images[image_name],
                    "rect": rect
                }
            )

            render_pos[0] += image_scale.get_width() + 10

        return tiles

    def update(self):

        mouse_pos = pg.mouse.get_pos()
        mouse_action = pg.mouse.get_pressed()

        if mouse_action[2]:
            self.selected_tile = None

        for tile in self.tiles:
            if tile["rect"].collidepoint(mouse_pos):
                if mouse_action[0]:
                    self.selected_tile = tile

    def draw(self, screen):

        # resouce hud
        screen.blit(self.resouces_surface, (0, 0))
        # build hud
        screen.blit(self.build_surface, (self.width * 0.84, self.height * 0.74))
        screen.blit(self.instructions, (60, 60))

        screen.blit(self.text_surface, (self.width * 0.84, self.height * 0.74 - 60))
        screen.blit(self.text_surface1, (60, 60))

        for tile in self.tiles:
            screen.blit(tile["icon"], tile["rect"].topleft)


    def load_images(self):

        # read images
        building1 = pg.image.load("assets/graphics/building01.png")
        building2 = pg.image.load("assets/graphics/building02.png")
        tree = pg.image.load("assets/graphics/tree.png")
        rock = pg.image.load("assets/graphics/rock.png")
        ts = pg.image.load("assets/graphics/trainStation.png")

        images = {
            "train": ts,
        }

        return images

    def scale_image(self, image, w=None, h=None):

        if (w == None) and (h == None):
            pass
        elif h == None:
            scale = w / image.get_width()
            h = scale * image.get_height()
            image = pg.transform.scale(image, (int(w), int(h)))
        elif w == None:
            scale = h / image.get_height()
            w = scale * image.get_width()
            image = pg.transform.scale(image, (int(w), int(h)))
        else:
            image = pg.transform.scale(image, (int(w), int(h)))

        return image

