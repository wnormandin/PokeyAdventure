
import pygame
import random
import os

from .core import CHA_ATTRIBUTES
from .core import CHA_FACTIONS
from .core import CHA_STATUS_EFFECTS
from .core import CHA_SKILLS
from .core import CHA_SIZES
from .core import CHA_LANGUAGES
from .core import INITIAL_STAT_SUM
from .weapons import Weapon # Superclasses for type comparisons
from .armor import Armor    # ''    ''      ''      ''      ''
from .items import Item     # ''    ''      ''      ''      ''

# Player/NPC Classes

class Character:

    ''' Parent class for characters and NPCs '''

    def __init__(self, name):
        self.age = 20
        self.name = name
        self.level = 1
        self.race = None
        self.player_class = None
        self.background = None
        self.attributes = {attr: 0 for attr in CHA_ATTRIBUTES}
        self.factions = {fact: 0 for fact in CHA_FACTIONS}
        self.skills = {skill: False for skill in CHA_SKILLS}
        self.languages = {lang: False for lang in CHA_LANGUAGES}
        self.advantages = []
        self.inventory = {}
        self.x = 0
        self.y = 0
        self.sprite_path = 'resources/sprites/TestWarr.png'
        self.sprite = pygame.image.load(os.path.join(os.getcwd(), self.sprite_path))

    @property
    def position(self):
        return self.y, self.x

    @position.setter
    def position(self, pos):
        y, x = pos
        self.y = y
        self.x = x

    @property
    def max_hp(self):
        return (self.level * self.player_class.hp_mult) + self.attributes['stamina']

    @property
    def max_dmg(self):
        base = self.level * self.player_class.dmg_mult
        weapon = self.weapon
        modifier = 0 if weapon is None else weapon.dmg
        return base + self.attributes['strength'] + modifier

    @property
    def weapon(self):
        for weap in self.weapons:
            obj = self.inventory[weap]
            if obj.equipped:
                return obj

    @property
    def armor(self):
        for armor in self.armors:
            obj = self.inventory[armor]
            if obj.equipped:
                return obj

    @property
    def armors(self):
        inv = self.inventory
        return {key: inv[key] for key in inv if isinstance(inv[key], Armor)}

    @property
    def weapons(self):
        inv = self.inventory
        return {key: inv[key] for key in inv if isinstance(inv[key], Weapon)}

    def fill_stats(self):
        base_stats = {attr: 5 for attr in CHA_ATTRIBUTES}
        stat_sum = INITIAL_STAT_SUM
        while stat_sum > 0:
            pref_stat = random.choice([True, True, False])
            if pref_stat:
                stat = random.choice(self.advantages)
            else:
                stat = random.choice(CHA_ATTRIBUTES)
            base_stats[stat] += 1
            stat_sum -= 1
        for attr in CHA_ATTRIBUTES:
            self.attributes[attr] += base_stats[attr]

    def _mod_attribute(self, attr, val):
        self.attributes[attr] += val

    def _mod_faction(self, fact, val):
        self.factions[fact] += val

    def _mod_skill(self, skill, val):
        self.skills[skill] = val

    def _mod_lang(self, lang, val):
        self.languages[lang] = val

    def _apply_dict(self, dict_list, method):
        # Apply initial dictionary values

        def do_apply(val_dict):
            for val in val_dict:
                if val_dict[val]:
                    # Only apply when true
                    method(val, val_dict[val])

        for _dict in dict_list:
            do_apply(_dict)

    def _equip_item(self, item):
        assert item in self.inventory.values()
        required = item.skills
        if not all(skill in self.skills for skill in required):
            return False
        else:
            item.equip()
            return True

    def _initial_inventory(self):
        self.inventory.update(self.player_class.inventory)
        self.inventory.update(self.race.inventory)
        self.inventory.update(self.background.inventory)

        max_dmg = max([self.weapons[w].dmg for w in self.weapons])
        for weapon in self.weapons:
            obj = self.weapons[weapon]
            if obj == max_dmg or len(self.weapons) == 1:
                if self._equip_item(obj):
                    break
                else:
                    continue

        max_ac = max([self.armors[a].ac for a in self.armors])
        for armor in self.armors:
            obj = self.armors[armor]
            if obj.ac == max_ac or len(self.armors) == 1:
                if self._equip_item(obj):
                    break
                else:
                    continue

    def character_init(self):
        # Post race/class/background selection init
        assert self.race is not None
        assert self.player_class is not None
        assert self.background is not None
        self.sprite_path = self.player_class.sprite_path
        bonuses = (self.race.bonuses, self.player_class.bonuses,
                    self.background.bonuses)
        factions = (self.race.factions, self.player_class.factions,
                    self.background.factions)
        skills = (self.race.skills, self.player_class.skills,
                    self.background.skills)
        languages = (self.race.languages, self.player_class.languages,
                    self.background.languages)

        for pair in ((bonuses, self._mod_attribute),
                    (languages, self._mod_lang),
                    (skills, self._mod_skill),
                    (factions, self._mod_faction)):
            self._apply_dict(*pair)

        self.speed = self.race.speed
        self.vision = self.race.vision
        self.size = self.race.size
        self.advantages.extend(self.race.advantages)
        self.advantages.extend(self.player_class.advantages)
        self.advantages.extend(self.background.advantages)
        self.fill_stats()
        self._initial_inventory()

class NPCharacter(Character):

    def __init__(self, name, cls, race, bg):
        super().__init__(name)
        self.player_class = cls
        self.race = race
        self.background = bg
