'''
import re

def base_roll(roll):
    dice = re.search(r'\d ',roll)
    if if_dice:
        sComment = roll[dice.end():]
        roll = roll[:if_dice.end()-1]
'''

from dice import DiceRoller

dicer = DiceRoller()

print dicer.base_roll('1d20')
