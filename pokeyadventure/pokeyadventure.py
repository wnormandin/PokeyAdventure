#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import time
import random
import argparse
import os
import sys

from game_objects import core
from game_objects import player_classes
from game_objects import players
from game_objects import backgrounds
from game_objects import races
from game_objects import tiles
from game_objects.world_gen import LevelGenerator

import pdb

this = sys.modules[__name__]
this.GameObject = core.GameObject

def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--pclass',
        choices=[cls.__name__ for cls in player_classes.CLASS_LIST],
        help='Specify a player class')
    parser.add_argument('-r', '--race',
        choices=[rc.__name__ for rc in races.RACE_LIST],
        help='Choose a race')
    parser.add_argument('-b', '--background',
        choices=[bg.__name__ for bg in backgrounds.BG_LIST],
        help='Choose a background')
    parser.add_argument('-n', '--name',
        help='Name your hero')
    parser.add_argument('-w', '--width',
        default=800, type=int,
        help='Screen width (default=800px)')
    parser.add_argument('-v', '--height',
        default=600, type=int,
        help='Screen height (default=600px)')
    parser.add_argument('-t', '--test',
        action='store_true',
        help='Test world generation and mechanics')
    return parser.parse_args()

class RBGColor:
    brown = core.stuple((153, 76, 0))
    purple = core.stuple((102, 0, 204))
    yellow = core.stuple((255, 255, 100))
    dk_blue = core.stuple((0, 0, 102))
    black = core.stuple((0, 0, 0))
    white = core.stuple((255, 255, 255))
    red = core.stuple((255, 0, 0))
    blue = core.stuple((0, 255, 0))
    green = core.stuple((0, 0, 255))

    def color_shift(color, vals=core.stuple((0, 0, 0))):
        return color + vals

class GameRunner:

    CELL_SIZE = core.GameObject.CELL_SIZE

    def __init__(self, args, player):
        pygame.init()
        self.cwd = os.getcwd()
        self.grid = core.MapGrid((100, 100), (args.width, args.height))
        self.lvl_gen = LevelGenerator
        self.grid.fill_matrix(self.lvl_gen, args.test)
        self.args = args
        self.gameDisplay = pygame.display.set_mode((args.width, args.height))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('PyPokey - A Test Game')
        self.player = player
        self.player.position = self.grid.random()

    def hero(self):
        y, x = self.player.position
        y0, x0 = self.grid.view_origin
        print('player_pos: {}'.format(self.player.position))
        y_min = (y - y0) * self.CELL_SIZE
        x_min = (x - x0) * self.CELL_SIZE
        self.gameDisplay.blit(self.player.sprite, (x_min, y_min))

    def text_objects(self, text, font):
        textSurface = font.render(text, True, RBGColor.black)
        return textSurface, textSurface.get_rect()

    def message_display(self, text, pos=None, size=40):
        normal_text = pygame.font.Font('freesansbold.ttf', size)
        TextSurf, TextRect = self.text_objects(text, normal_text)
        if pos is not None:
            width, height = pos
        else:
            width = self.args.width / 2
            height = self.args.height / 2
        TextRect.center = (width, height)
        self.gameDisplay.blit(TextSurf, TextRect)
        pygame.display.update()

    def debug_info(self):
        # Debug information, dimensions, etc
        pass

    def draw_stats(self):
        # Player stats, status effects, and etc
        pass

    def draw_inventory(self):
        # Player inventory area
        pass

    def draw_info(self):
        # Scrolling info message area
        pass

    def draw_map(self):
        # Draw visible portion of the map
        visible, (y0, x0) = self.grid.visible_cells(self.player.position)
        for key in visible:
            y, x = key
            # Calculate the tile origin in pixels
            y_min = (y - y0) * GameObject.CELL_SIZE
            x_min = (x - x0) * GameObject.CELL_SIZE

            tile = self.grid.get(key, 'tile')
            if tile.fog is None:
                tile.fog = tile._get_fog()

            self.grid.map_s.blit(tile.image, (x_min, y_min))
            #self.gameDisplay.blit(tile.image, (x_min, y_min))

            # Set tile explored
            if self.player.position == (y, x):
                tile.explore()

            # Update visible / fog alpha level
            tile.visible(self.player)
            self.grid.map_s.blit(tile.fog, (x_min, y_min))
            #self.gameDisplay.blit(tile.fog, (x_min, y_min))

    def move_player(self, direction):
        y_, x_ = self.player.position + direction
        valid_pt = self.grid.valid(y_, True), self.grid.valid(x_)
        # Flip y/x here for pygame
        dest_tile = self.grid.get((valid_pt[1], valid_pt[0]), 'tile')
        if dest_tile.passable and not dest_tile.locked:
            self.player.position = dest_tile.position

    def game_loop(self):
        x = (self.args.width * 0.45)
        y = (self.args.height * 0.8)
        x_change = 0
        y_change = 0
        move_speed = 0
        gameExit = False

        self.player.position = self.grid.start_point

        while not gameExit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True

                direction = None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        direction = self.player.LEFT
                    elif event.key == pygame.K_RIGHT:
                        direction = self.player.RIGHT
                    elif event.key == pygame.K_UP:
                        direction = self.player.UP
                    elif event.key == pygame.K_DOWN:
                        direction = self.player.DOWN
                    elif event.key == pygame.K_q:
                        gameExit = True

                if event.type == pygame.KEYUP:
                    if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                        pass
                    elif event.key in [pygame.K_UP, pygame.K_DOWN]:
                        pass

                # Set player position before calling hero()
                if direction is not None:
                    self.move_player(direction)

                self.draw_map()
                # self.draw_stats()
                # self.draw_inventory()
                # self.draw_info()
                # pdb.set_trace()
                self.hero()
                self.debug_info()

            pygame.display.update()
            self.clock.tick(60)

class PokeyAdventure:

    def __init__(self, args):
        self.args = args
        self.player = players.Character(args.name)
        self.player.race = getattr(races, args.race)()
        self.player.player_class = getattr(player_classes, args.pclass)()
        self.player.background = getattr(backgrounds, args.background)()
        self.app_class = GameRunner

    def game_options(self):
        # Keep the queue clear of mouse events
        allowed = [pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP]
        pygame.event.set_allowed(allowed)
        blocked = [pygame.MOUSEMOTION]
        pygame.event.set_blocked(blocked)

    def character_init(self):
        self.player.character_init()
        self.app = self.app_class(self.args, self.player)

    def execute(self):
        try:
            self.app.game_loop()
        except:
            raise

if __name__ == '__main__':
    args = cli()
    game = PokeyAdventure(args)
    game.character_init()
    game.game_options()
    game.execute()
