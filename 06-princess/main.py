"""
ISPPV1-I2026
Study Case: The Legend of the Princess (ARPG)

Author: Brian Marquez
brnmarq@gmail.com

This file contains the main program to run the game.
"""

from src.TheLegendOfThePrincess import TheLegendOfThePrincess
from src import states

if __name__ == "__main__":
    game = TheLegendOfThePrincess()
    game.exec()
