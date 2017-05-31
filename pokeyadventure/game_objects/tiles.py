import pygame
import os
import random
import sys

import pdb

from .core import GameObject


class Tile(GameObject):

    def __init__(self, pos):
        super().__init__(pos)
        self.passable = True    # Determines whether char can pass through tile
        self.locked = False
        self.image_base_path = 'resources/textures'
        self.image_filename = 'black_wood_wall_25px.png'
        self.traps = []
        self.metachar = '#'
        self.explored = False # Changes to true when the player has visited this tile
        self.max_alpha = 255
        self.fog = None

    def visible(self, p):
        if min(self._pt_distance(p.position)) < 5:
            self.fog.set_alpha(0)
            return True
        else:
            self.fog.set_alpha(self.max_alpha)
            return False

    def explore(self):
        self.max_alpha = 120
        self.fog.set_alpha(120)

    def _get_fog(self):
        # Creates the fog layer for this particular cell
        y, x = self.position
        fog = pygame.Surface((x * self.CELL_SIZE, y * self.CELL_SIZE))
        fog.set_alpha(self.max_alpha)
        fog.fill((0, 0, 0))
        return fog

    def _load_image(self):
        file_path = os.path.join(os.getcwd(), self.image_base_path)
        file_path = os.path.join(file_path, self.image_filename)
        self.image = pygame.image.load(file_path)

class Floor(GameObject):

    def __init__(self, pos):
        super().__init__(pos)
        self.damage = 0 # Assign for DPS
        self.false = False # Indicate whether this is a false door
        self.false_image = ''


class Door(GameObject):

    def _toggle_lock(self):
        # Using MI, ensures 2nd parent __init__ is called
        self.locked = not self.locked
        self.passable = not self.locked


class Wall(GameObject):

    def __init__(self, pos):
        super().__init__(pos)
        self.passable = False


class MossyFloor(Tile, Floor):

    def __init__(self, pos):
        super().__init__(pos)
        self.image_filename = 'mossy_floor_25px.png'
        self._load_image()
        self.metachar = 'm'


class BarnDoor(Tile, Door):

    def __init__(self, pos):
        super().__init__(pos)
        self.image_filename = 'barn_door_25px.png'
        self._load_image()
        self.metachar = 'D'


class LavaFloor(Tile, Floor):

    def __init__(self, pos):
        super().__init__(pos)
        self.image_filename = 'fire_ground_25px.png'
        self._load_image()
        self.metachar = 'L'
        self.damage = 1


class WoodWall(Tile, Wall):

    def __init__(self, pos):
        super().__init__(pos)
        self.image_filename = 'black_wood_wall_25px.png'
        self._load_image()
        self.metachar = 'W'


class ScreenFloor(Tile, Floor):

    def __init__(self, pos):
        super().__init__(pos)
        self.image_filename = 'dark_screen_25px.png'
        self._load_image()
        self.metachar = 's'


class SnowFloor(Tile, Floor):

    def __init__(self, pos):
        super().__init__(pos)
        self.image_filename = 'snowy_path_25px.png'
        self._load_image()
        self.metachar = 'S'


class BrickWall(Tile, Wall):

    def __init__(self, pos):
        super().__init__(pos)
        self.image_filename = 'red_brick_25px.png'
        self._load_image()
        self.metachar = 'w'


class WoodDoor(Tile, Door):

    def __init__(self, pos):
        super().__init__(pos)
        self.image_filename = 'wooden_door_25px.png'
        self._load_image()
        self._toggle_lock() # Start locked
        self.metachar = 'd'


class Curtain(Tile):

    RED = 0
    BLUE = 1

    def __init__(self, color=0):
        super().__init__()
        template = 'curtain_{}_25px.png'
        if color == Curtain.RED:
            template.format('red')
        elif color == Curtain.BLUE:
            template.format('blue')
        else:
            raise ValueError("Color {} not found".format(color))
        self._load_image()
        self.metachar = 'C'


class TudorWall(Tile, Wall):

    def __init__(self, pos):
        super().__init__(pos)
        self.image_filename = 'interior_wood_wall_25px.png'
        self._load_image()
        self.metachar = 'T'


class BrickFloor(Tile):

    def __init__(self, pos):
        super().__init__(pos)
        self.image_filename = 'gray_brick_25px.png'
        self._load_image()
        self.metachar = 'B'
