#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse

from game_objects import player_classes
from game_objects import players
from game_objects import races
from game_objects import backgrounds
from game_objects import core

def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--pclass',
            choices=[cls.__name__ for cls in player_classes.CLASS_LIST],
            help="Specify a player class")
    parser.add_argument('-r', '--race',
            choices=[rc.__name__ for rc in races.RACE_LIST],
            help="Specify a race for your character")
    parser.add_argument('-b', '--background',
            choices=[bg.__name__ for bg in backgrounds.BG_LIST],
            help="Specify a background for your character")
    parser.add_argument('-n', '--name',
            help="Your hero's name")
    return parser.parse_args()

def print_equipped(inventory):
    print('[*] Equipped')
    for item in inventory:
        if inventory[item].equipped:
            print('\t{:<20}{:<20}'.format(item, str(inventory[item])))

def print_inventory(inventory):
    print('[*] Inventory')
    for item in inventory:
        print('\t{:<20}{:<20}'.format(item, str(inventory[item])))

def print_char_stats(player):

    def print_dict(_dict, msg):
        print(msg)
        for key in _dict:
            print('\t{:<20}{:<20}'.format(key, str(_dict[key])))

    print('[*] Player Stats for {}'.format(player.name))
    for val in ['level', 'speed', 'age']:
        print('\t{:<20}{:<20}'.format(val, getattr(player, val)))
    for val in ['background', 'player_class', 'race']:
        print('\t{:<20}{:<20}'.format(val, getattr(player, val).__class__.__name__))
    for val in ['max_hp', 'max_dmg']:
        print('\t{:<20}{:<20}'.format(val, getattr(player, val)))
    print('[*] Advantages: {}'.format(', '.join(player.advantages)))
    print_dict(player.attributes, '[*] Attributes')
    print_dict(player.factions, '[*] Factions')
    print_dict(player.skills, '[*] Skills')
    print_dict(player.languages, '[*] Languages')
    print_inventory(player.inventory)
    print_equipped(player.inventory)

if __name__ == '__main__':
    args = cli()
    player = players.Character(args.name)
    player.race = getattr(races, args.race)()
    player.player_class = getattr(player_classes, args.pclass)()
    player.background = getattr(backgrounds, args.background)()
    player.character_init()
    print_char_stats(player)
