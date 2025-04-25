
import pygame as pg
import random
import noise
from .settings import TILE_SIZE
import time


class World:

    def __init__(self, hud, grid_length_x, grid_length_y, width, height,map_image=None):
        self.hud = hud
        self.grid_length_x = grid_length_x
        self.grid_length_y = grid_length_y
        self.width = width
        self.height = height
        world_width = self.grid_length_x * TILE_SIZE
        world_height = self.grid_length_y * TILE_SIZE
        self.map_center_x = world_width / 2
        self.map_center_y = world_height / 2
        self.perlin_scale = grid_length_x/2

        self.grass_tiles = pg.Surface((grid_length_x * TILE_SIZE * 2, grid_length_y * TILE_SIZE + 2 * TILE_SIZE)).convert_alpha()
        self.tiles = self.load_images()
        self.world = self.create_world()


        # Check if image not null, if null use procedural map
        if map_image:
            self.world = self.create_world_from_image(map_image)
        else:
            self.world = self.create_world()
            
        self.last_growth_time = time.time()
        self.temp_tile = None


        self.last_growth_time = time.time()
        self.temp_tile = None



    def is_neighbor_of_train_station(self, x, y):
            neighbors = self.get_neighbors(x, y)
            for nx, ny in neighbors:
                if self.world[nx][ny]["tile"] == "train":
                    return True
            return False

    def is_within_train_station_radius(self, x, y, radius):
        for tx in range(self.grid_length_x):
            for ty in range(self.grid_length_y):
                if self.world[tx][ty]["tile"] == "train":
                    distance = abs(x - tx) + abs(y - ty)
                    if distance <= radius:
                        return True
        return False
    
    def get_distance_to_nearest_train(self, x, y):
        min_distance = float('inf')
        for tx in range(self.grid_length_x):
            for ty in range(self.grid_length_y):
                if self.world[tx][ty]["tile"] == "train":
                    distance = abs(x - tx) + abs(y - ty) 
                    min_distance = min(min_distance, distance)
        
        return min_distance
       
    def simulation(self):
        new_tile = []
        for x in range(self.grid_length_x):
            for y in range(self.grid_length_y):
                if (
                    self.world[x][y]["tile"] == "building1"
                    or self.world[x][y]["tile"] == "building2"
                    or self.world[x][y]["tile"] == "building3"
                    or self.world[x][y]["tile"] == "building4"
                ):
                    neighbors = self.get_neighbors(x, y)
                    for nx, ny in neighbors:
                        localGrowthValue = 0
                        if self.is_within_train_station_radius(
                            nx, ny,3
                        ):  # Check if neighbor of train station
                            localGrowthValue = 0.1  # Increase growth probability

                        if (
                            self.world[nx][ny]["tile"] == ""
                            and random.random() < 0 + localGrowthValue
                        ):  
                            new_tile.append((nx, ny))
                        elif (
                            self.world[nx][ny]["tile"] == "farm"
                            and random.random() < 0.01 + localGrowthValue * 5
                        ):  
                            new_tile.append((nx, ny))

        for nx, ny in new_tile:

            #density determination
            if random.random() < 0.01 :
                self.world[nx][ny]["tile"] = "building1"
                self.world[nx][ny]["collision"] = True
            elif random.random() < 0.15 + localGrowthValue and self.get_distance_to_nearest_train(nx,ny) < 3:
                self.world[nx][ny]["tile"] = "building2"
                self.world[nx][ny]["collision"] = True
            elif random.random() < 0.05 + localGrowthValue and self.get_distance_to_nearest_train(nx,ny) < 2:
                self.world[nx][ny]["tile"] = "building3"
                self.world[nx][ny]["collision"] = True
            elif random.random() < 0.15 + localGrowthValue and self.get_distance_to_nearest_train(nx,ny) < 1:
                self.world[nx][ny]["tile"] = "building4"
                self.world[nx][ny]["collision"] = True
            elif random.random() < 0.9 - localGrowthValue * 5:
                self.world[nx][ny]["tile"] = "farm"
                self.world[nx][ny]["collision"] = True

    #used to get neighbours for cellular automata
    def get_neighbors(self, x, y):
        neighbors =  []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue  
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.grid_length_x and 0 <= ny < self.grid_length_y:
                    neighbors.append((nx, ny))
        return neighbors
    

    def update(self, camera, zoom_factor):
        mouse_pos = pg.mouse.get_pos()
        mouse_action = pg.mouse.get_pressed()

        self.temp_tile = None

        current_time = time.time()
        if current_time - self.last_growth_time >= 0.5:  # 60 seconds
            self.simulation()
            self.last_growth_time = current_time


        

        if self.hud.selected_tile is not None:

            grid_pos = self.mouse_to_grid(mouse_pos[0], mouse_pos[1], camera.scroll,zoom_factor)

            if self.can_place_tile(grid_pos):
                img = self.hud.selected_tile["image"].copy()
                img.set_alpha(100)

                try:
                    render_pos = self.world[grid_pos[0]][grid_pos[1]]["render_pos"]
                    iso_poly = self.world[grid_pos[0]][grid_pos[1]]["iso_poly"]
                    collision = self.world[grid_pos[0]][grid_pos[1]]["collision"]
                except:
                    print("stupid error due to mouse coordinates not on map")
                    render_pos = self.world[0][0]["render_pos"]
                    iso_poly = self.world[0][0]["iso_poly"]
                    collision = self.world[0][0]["collision"]


                self.temp_tile = {
                    "image": img,
                    "render_pos": render_pos,
                    "iso_poly": iso_poly,
                    "collision": collision
                }

                if mouse_action[0] and not collision:
                    self.world[grid_pos[0]][grid_pos[1]]["tile"] = self.hud.selected_tile["name"]
                    self.world[grid_pos[0]][grid_pos[1]]["collision"] = True
                    self.hud.selected_tile = None


    def draw(self, screen, camera):

        screen.blit(self.grass_tiles, (camera.scroll.x, camera.scroll.y))

        for x in range(self.grid_length_x):
            for y in range(self.grid_length_y):
                render_pos =  self.world[x][y]["render_pos"]
                tile = self.world[x][y]["tile"]
                if tile != "":
                    screen.blit(self.tiles[tile],
                                    (render_pos[0] + self.grass_tiles.get_width()/2 + camera.scroll.x,
                                     render_pos[1] - (self.tiles[tile].get_height() - TILE_SIZE) + camera.scroll.y))

        if self.temp_tile is not None:
            iso_poly = self.temp_tile["iso_poly"]
            iso_poly = [(x + self.grass_tiles.get_width()/2 + camera.scroll.x, y + camera.scroll.y) for x, y in iso_poly]
            if self.temp_tile["collision"]:
                pg.draw.polygon(screen, (255, 0, 0), iso_poly, 3)
            else:
                pg.draw.polygon(screen, (255, 255, 255), iso_poly, 3)
            render_pos = self.temp_tile["render_pos"]
            screen.blit(
                self.temp_tile["image"],
                (
                    render_pos[0] + self.grass_tiles.get_width()/2 + camera.scroll.x,
                    render_pos[1] - (self.temp_tile["image"].get_height() - TILE_SIZE) + camera.scroll.y
                )
            )

    def create_world(self):
        world = []
        for grid_x in range(self.grid_length_x):
            world.append([])
            for grid_y in range(self.grid_length_y):
                world_tile = self.grid_to_world(grid_x, grid_y)
                world[grid_x].append(world_tile)
                render_pos = world_tile["render_pos"]
                self.grass_tiles.blit(self.tiles["block"], (render_pos[0] + self.grass_tiles.get_width()/2, render_pos[1]))
        return world

    def grid_to_world(self, grid_x, grid_y):
        rect = [
            (grid_x * TILE_SIZE, grid_y * TILE_SIZE),
            (grid_x * TILE_SIZE + TILE_SIZE, grid_y * TILE_SIZE),
            (grid_x * TILE_SIZE + TILE_SIZE, grid_y * TILE_SIZE + TILE_SIZE),
            (grid_x * TILE_SIZE, grid_y * TILE_SIZE + TILE_SIZE)
        ]
        iso_poly = [self.cart_to_iso(x, y) for x, y in rect]
        minx = min([x for x, y in iso_poly])
        miny = min([y for x, y in iso_poly])
        r = random.randint(1, 100)
        perlin = 100 * noise.pnoise2(grid_x/self.perlin_scale, grid_y/self.perlin_scale)
        if (perlin >= 15) or (perlin <= -35):
            tile = "water"
        else:
            if r == 1:
                tile = "water"
            elif r >= 2 and r <= 10:
                tile = "rock"
            elif r > 10 and r < 16:
                tile = "building1"
            else:
                tile = ""

        out = {
            "grid": [grid_x, grid_y],
            "cart_rect": rect,
            "iso_poly": iso_poly,
            "render_pos": [minx, miny],
            "tile": tile,
            "collision": False if tile == "" else True
        }

        return out

    def cart_to_iso(self, x, y):
        iso_x = x - y
        iso_y = (x + y)/2
        return iso_x, iso_y

    def mouse_to_grid(self, x, y, scroll, zoom_factor):
        # Adjust for zoom
        world_x = x / zoom_factor
        world_y = y / zoom_factor

        # transform to world position (removing camera scroll and offset)
        world_x -= scroll.x + self.grass_tiles.get_width() / 2
        world_y -= scroll.y
        # transform to cart (inverse of cart_to_iso)
        cart_y = (2 * world_y - world_x) / 2
        cart_x = cart_y + world_x
        # transform to grid coordinates

        grid_x = int(cart_x // TILE_SIZE)
        grid_y = int(cart_y // TILE_SIZE)

        return grid_x, grid_y

    def load_images(self):

        block = pg.image.load("assets/graphics/block.png").convert_alpha()
        building1 = pg.image.load("assets/graphics/building01.png").convert_alpha()
        building2 = pg.image.load("assets/graphics/building02.png").convert_alpha()
        water = pg.image.load("assets/graphics/water.png").convert_alpha()
        rock = pg.image.load("assets/graphics/rock.png").convert_alpha()
        farm = pg.image.load("assets/graphics/farms.png").convert_alpha()
        building3 = pg.image.load("assets/graphics/building03.png").convert_alpha()
        building4 = pg.image.load("assets/graphics/building04.png").convert_alpha()
        ts = pg.image.load("assets/graphics/trainStation.png").convert_alpha()
        images = {
            "building1": building1,
            "building2": building2,
            "building3": building3,
            "building4": building4,
            "water": water,
            "rock": rock,
            "block": block,
            "farm" : farm,
            "train" : ts
        }

        return images
    def create_world_from_image(self, image_path):
        
        # Attempt to load the image and create the world, if null, use procedural map
        try:
            map_image = pg.image.load(image_path).convert()
        except:
            print(f"Failed to load image: {image_path}")
            return self.create_world() 
        
        map_image = pg.transform.scale(map_image, (self.grid_length_x, self.grid_length_y))
        
        world = []
        
        #color coded from png
        color_map = {
            (0, 0, 255): "water",      
            (255, 255, 0): "farm",     
            (100, 50, 0): "rock",      
            (255, 0, 0): "building1",  
            (200, 0, 0): "building2",  
            (150, 0, 0): "building3",  
            (100, 0, 0): "building4",  
            (0, 0, 0): "train"  
        }
        
        for grid_x in range(self.grid_length_x):
            world.append([])
            for grid_y in range(self.grid_length_y):

                rect = [
                    (grid_x * TILE_SIZE, grid_y * TILE_SIZE),
                    (grid_x * TILE_SIZE + TILE_SIZE, grid_y * TILE_SIZE),
                    (grid_x * TILE_SIZE + TILE_SIZE, grid_y * TILE_SIZE + TILE_SIZE),
                    (grid_x * TILE_SIZE, grid_y * TILE_SIZE + TILE_SIZE)
                ]

                iso_poly = [self.cart_to_iso(x, y) for x, y in rect]
                minx = min([x for x, y in iso_poly])
                miny = min([y for x, y in iso_poly])

                world_tile = {
                    "grid": [grid_x, grid_y],
                    "cart_rect": rect,
                    "iso_poly": iso_poly,
                    "render_pos": [minx, miny],
                    "tile": "", 
                    "collision": False 
                }
                
                # Get pixel color
                try:
                    pixel_color = map_image.get_at((grid_x, grid_y))[:3]
                except IndexError:
                    pixel_color = (255, 255, 255)  # Default white
                
                #algorithm to get closests color from png
                min_distance = float('inf')
                matching_tile = ""
                for color, tile in color_map.items():
                    distance = sum((a - b) ** 2 for a, b in zip(color, pixel_color))
                    if distance < min_distance:
                        min_distance = distance
                        matching_tile = tile
                if min_distance < 10000: 
                    world_tile["tile"] = matching_tile
                    world_tile["collision"] = matching_tile != ""
                
                world[grid_x].append(world_tile)
                
                #default
                render_pos = world_tile["render_pos"]
                self.grass_tiles.blit(self.tiles["block"], 
                                    (render_pos[0] + self.grass_tiles.get_width()/2, render_pos[1]))
        
        return world
    
    
    def can_place_tile(self, grid_pos):
        mouse_on_panel = False
        for rect in [self.hud.resources_rect, self.hud.build_rect, self.hud.select_rect]:
            if rect.collidepoint(pg.mouse.get_pos()):
                mouse_on_panel = True
        world_bounds = (0 <= grid_pos[0] <= self.grid_length_x) and (0 <= grid_pos[1] <= self.grid_length_x)
        if world_bounds and not mouse_on_panel:
            return True
        else:
            return False

