#!python3

"""
This module initiates a yahtzee game.

github.com/pmacking/main.py
"""

from .yahtzee import Yahtzee


def main():
    yahtzee_game = Yahtzee()
    yahtzee_game.play()


if __name__ == "__main__":
    main()
