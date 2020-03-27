#!python3

from roll import Roll
from player import Player
import pyinputplus as pyip

print('WELCOME TO YAHTZEE!')


def main():
    '''
    Main gameplay for playing yahtzee
    '''
    # scoring dictionaries
    _scoreDict = {
            'ones': 0, 'twos': 0, 'threes': 0, 'fours': 0, 'fives': 0,
            'sixes': 0, 'three of a kind': 0, 'four of a kind': 0,
            'full house': 0, 'small straight': 0, 'large straight': 0,
            'yahtzee': 0, 'chance': 0, 'yahtzee bonus': 0,
            }
    _scoreDictReferenceValues = {
            'ones': 1, 'twos': 2, 'threes': 3,
            'fours': 4, 'fives': 5, 'sixes': 6
            }
    # create Player and Roll instances for each player (1 to 4)
    playersList = []
    rollsList = []

    numberOfPlayers = pyip.inputInt(prompt='Enter number of players (1 to 4):\n', min=1, max=4)

    # create player and rolls instances in mirrored lists
    for player in range(numberOfPlayers):
        playerName = pyip.inputStr(prompt=f'\nEnter name of player{player+1}:\n')
        playersList.append(Player(playerName))
        rollsList.append(Roll(playerName))

    # rounds for each player based on scoreDict and number of players
    for i, k in enumerate(_scoreDict):
        for j, player in enumerate(playersList):
            print(f'\n{playersList[j].name.upper()} your turn.\n')

            # first roll
            rollsList[j].rollDice()
            keepFirstRoll = rollsList[j].keepDice()

            # second roll
            rollsList[j].reRollDice(keepFirstRoll)
            keepSecondRoll = rollsList[j].keepDice()

            #third roll
            rollsList[j].finalRollDice(keepSecondRoll)

            print(rollsList[j].getCurrentDice())


    # for player in playersList:

    # # loop through the top part and start rolling some dice!
    # for index,item in enumerate(game_list_top):

    #     #just one way to print info on the current rolling
    #     print ('-'*40)
    #     print (f'rolling for {item}')
    #     print ('-'*40)

    #     #first roll:
    #     dice1.roll_dice()
    #     keep1 = dice1.keep_dice()

    #     #second roll:
    #     dice1.reroll_dice(keep1)
    #     keep2 = dice1.keep_dice()

    #     #third roll:
    #     roll3 = dice1.reroll_dice(keep2)
    #     dice1.forced_keep(roll3)

    #     #the final roll collection of dice goes in for check:
    #     final_roll_collection = dice1.get_kept_dice()

    #     print (f'final roll collection: {final_roll_collection}')

    #     #check what the score is for this particular roll:
    #     check_score = dice1.single_values(final_roll_collection,game_list_top_values[index] )

    #     #create the key in the dictionary and add the score to the total top score.
    #     #this score will later determine if we get a bonus or not.
    #     player1.add_rolled(item , check_score)
    #     player1.add_top_score(check_score)

    # #let's hope we get a bonus?
    # player1.add_top_bonus()

    # #print current score:
    # player1.print_scoreboard()


if __name__ == "__main__":
    main()
