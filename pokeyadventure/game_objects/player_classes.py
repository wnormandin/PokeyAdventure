
from .core import CHA_ATTRIBUTES
from .core import CHA_FACTIONS
from .core import CHA_STATUS_EFFECTS
from .core import CHA_SKILLS
from .core import CHA_SIZES
from .core import CHA_LANGUAGES
from .weapons import Sword, Mace, Dagger, Staff
from .armor import ClothArmor, IronArmor, LeatherArmor

class PlayerClass:

    ''' Parent class for player class objects

        In addition to attributes, factions, skills, and languages,
        PlayerClass objects have:
            hp_mult - the base hp_multiplier for max_hp calculations

    '''

    def __init__(self):
        self.hp_mult = 5
        self.dmg_mult = 1
        self.advantages = []
        self.bonuses = {attr: 0 for attr in CHA_ATTRIBUTES}
        self.skills = {skill: False for skill in CHA_SKILLS}
        self.factions = {fact: 0 for fact in CHA_FACTIONS}
        self.languages = {lang: False for lang in CHA_LANGUAGES}
        self.inventory = {}
        self.sprite_path = 'resources/sprites/TestWarr.png'

class Warrior(PlayerClass):

    ''' Specialist in melee weapons '''

    def __init__(self):
        super().__init__()
        self.hp_mult = 7
        self.dmg_mult = 1.5

        # Default Warrior Skills
        self.skills['light_armor'] = True
        self.skills['heavy_armor'] = True
        self.skills['slashing'] = True
        self.skills['piercing'] = True
        self.skills['blunt'] = True

        # Default Warrior Factions
        self.factions['guards'] += 5

        # Default Warrior Bonuses/Advantages
        self.bonuses['strength'] += 1
        self.advantages.extend(['strength', 'stamina'])

        # Default Warrior Inventory
        self.inventory['Sword'] = Sword()
        self.inventory['Iron Armor'] = IronArmor()

class Rogue(PlayerClass):

    ''' Specialist in stealth '''

    def __init__(self):
        super().__init__()

        # Default Rogue Skills
        self.skills['sneak'] = True
        self.skills['piercing'] = True
        self.skills['light_armor'] = True

        # Default Rogue Factions
        self.factions['guards'] -= 5
        self.factions['thieves'] += 10

        # Default Rogue Bonuses/Advantages
        self.bonuses['dexterity'] += 1
        self.advantages.extend(['dexterity', 'charisma'])

        # Default Rogue Inventory
        self.inventory['Dagger'] = Dagger()
        self.inventory['Leather Armor'] = LeatherArmor()

class Wizard(PlayerClass):

    ''' Specialist in destruction magic '''

    def __init__(self):
        super().__init__()

        # Default Wizard Skills
        self.skills['spells'] = True
        self.skills['blunt'] = True

        # Default Wizard Factions
        self.factions['mages'] += 5
        self.factions['magical'] += 5

        # Default Wizard Languages
        self.languages['celestial'] = True

        # Default Wizard Bonuses/Advantages
        self.bonuses['stamina'] += 1
        self.bonuses['intelligence'] += 1
        self.advantages.extend(['stamina', 'intelligence'])

        # Default Wizard Inventory
        self.inventory['Staff'] = Staff()
        self.inventory['Cloth Armor'] = ClothArmor()

CLASS_LIST = [Warrior, Rogue, Wizard]
