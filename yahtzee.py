#!python3

# this is a multiplayer yahtzee game
# instructions: https://www.hasbro.com/common/instruct/Yahtzee.pdf

from random import randint

# game and player attributes
round=0
player={'1':'False','2':'False','3':'False','4':'False'}
# or implement dictionary for each player (active, total score, best score)

# score keeping
scoreCardTop={'Ones':'0','Twos':'0','Threes':'0','Fours':'0','Fives':'0','Sixes':'0'}
scoreCardBottom={'Three of a kind':'0','Four of a kind':'0','Full house':'0','Small straight':'0','Large straight':'0','Yahtzee':'0','Chance':'0','Yahtzee bonus':'0'}
totalScoreCard={'Sum of upper':'0','Bonus':'0','Total upper':'0','Total bottom':'0','Grand total':'0'}

# dice attributes
dice={'1':'0','2':'0','3':'0','4':'0','5':'0'}
# TODO: should we have selected/unselected dice?
diceActive={'1':'False','2':'False','3':'False','4':'False','5':'False'}