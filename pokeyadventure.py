#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import time
import random
import argparse
import os

from game_objects import core
from game_objects import player_classes
from game_objects import players
from game_objects import backgrounds
from game_objects import races
from game_objects import core
from game_objects import tiles

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
    brown = (153, 76, 0)
    purple = (102, 0, 204)
    yellow = (255, 255, 100)
    dk_blue = (0, 0, 102)
    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (255, 0, 0)
    blue = (0, 255, 0)
    green = (0, 0, 255)

    def color_shift(color, vals=tiles.stuple((0, 0, 0)), double=False):
        if hard:
            modifier = 40
        else:
            modifier = 20
        return color[val] + modifier

class GameRunner:

    CELL_SIZE = 25


    def __init__(self, args, player):
        pygame.init()
        self.cwd = os.getcwd()
        self.grid = tiles.MapGrid((args.height, args.width), PyPokey.CELL_SIZE)
        self.grid.fill_matrix(args.test)
        self.args = args
        self.gameDisplay = pygame.display.set_mode((args.width, args.height))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('PyPokey - A Test Game')
        self.player = player
        self.player.position = self.grid.random()

    def hero(self):
        y, x = self.player.position
        y_min = y * PyPokey.CELL_SIZE
        x_min = x * PyPokey.CELL_SIZE
        self.gameDisplay.blit(self.player.sprite, (x_min, y_min))

    def text_objects(self, text, font):
        textSurface = font.render(text, True, PyPokey.black)
        return textSurface, textSurface.get_rect()

    def message_display(self, text, pos=None):
        normal_text = pygame.font.Font('freesansbold.ttf', 40)
        TextSurf, TextRect = self.text_objects(text, normal_text)
        if pos is not None:
            width, height = pos
        else:
            width = self.args.width / 2
            height = self.args.height / 2
        TextRect.center = (width, height)
        self.gameDisplay.blit(TextSurf, TextRect)
        pygame.display.update()
        time.sleep(1)

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
        viewable = self.grid.viewable
        for key in viewable:
            tile = viewable[key]
            self.gameDisplay.blit(tile['tile'].image, (tile['x_min'], tile['y_min']))

    def game_loop(self):
        x = (self.args.width * 0.45)
        y = (self.args.height * 0.8)
        x_change = 0
        y_change = 0
        move_speed = 0
        gameExit = False

        while not gameExit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        x_change = -1
                    elif event.key == pygame.K_RIGHT:
                        x_change = 1
                    elif event.key == pygame.K_UP:
                        y_change = -1
                    elif event.key == pygame.K_DOWN:
                        y_change = 1
                if event.type == pygame.KEYUP:
                    if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                        x_change = 0
                    elif event.key in [pygame.K_UP, pygame.K_DOWN]:
                        y_change = 0

                # Set player position before calling hero()
                self.player.x += x_change
                self.player.y += y_change
                self.draw_map()
                self.draw_stats()
                self.draw_inventory()
                self.draw_info()
                self.hero()

                if x > self.args.width - PyPokey.CELL_SIZE:
                    x = self.args.width - PyPokey.CELL_SIZE
                if x < 0:
                    x = 0
                if y < 0:
                    y = 0
                if y > self.args.height - PyPokey.CELL_SIZE:
                    y = self.args.height - PyPokey.CELL_SIZE

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
    game.execute()
