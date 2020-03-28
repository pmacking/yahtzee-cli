#!python3

from roll import Roll
from player import Player
import pyinputplus as pyip

print('WELCOME TO YAHTZEE!')


def main():
    '''
    Main gameplay for playing yahtzee
    '''

    # reference dicts and lists for calculating scores
    _scoreDictReferenceValues = {
            'ones': 1, 'twos': 2, 'threes': 3,
            'fours': 4, 'fives': 5, 'sixes': 6,
            'full house': 25, 'small straight': 30, 'large straight': 35,
            'yahtzee': 50, 'yahtzee bonus': 50,
            }
    singlesOptions = [
                'ones', 'twos', 'threes', 'fours', 'fives', 'sixes'
                ]

    # create Player and Roll instances for each player (1 to 4)
    playersList = []
    rollsList = []

    numberOfPlayers = pyip.inputInt(prompt='\nEnter number of players (1 to 4):\n', min=1, max=4)

    # create Player and Roll instances per player in mirrored lists
    for player in range(numberOfPlayers):
        playerName = pyip.inputStr(prompt=f'\nEnter name of player{player+1}:\n')
        playersList.append(Player(playerName))
        rollsList.append(Roll(playerName))

    # rounds for each player based on scoreDict and number of players
    for i, k in enumerate(playersList[0]._scoreDict):
        for j, player in enumerate(playersList):

            # printing player and scores for each round
            print(f'\n{playersList[j].name.upper()} YOUR TURN. ROUND: {i+1}')

            print('-'*21)
            print('ROLL SCORES'.rjust(16))
            playersList[j].printScoreDict()

            print('-'*21)
            print('TOP SCORE BONUS'.rjust(19))
            playersList[j].printTopScore()
            playersList[j].printTopBonusScore()

            print('-'*21)
            print('TOTAL SCORES'.rjust(19))
            playersList[j].printTotalTopScore()
            playersList[j].printTotalBottomScore()

            print('-'*21)
            playersList[j].printGrandTotalScore()

            # first roll
            rollsList[j].rollDice()
            print(f'{playersList[j].name.upper()}', end='')
            keepFirstRoll = rollsList[j].keepDice()

            # second roll
            rollsList[j].reRollDice(keepFirstRoll)
            keepSecondRoll = rollsList[j].keepDice()

            # third roll
            finalRoll = rollsList[j].finalRollDice(keepSecondRoll)

            # select score from existing options to check dice against
            scoreSelected = playersList[j].selectScore()

            # this section checks TOP and BOTTOM scores based on score selected
            # TOP SCORE options and increment scores
            if scoreSelected in singlesOptions:
                score = rollsList[j].checkSingles(finalRoll, _scoreDictReferenceValues[scoreSelected])

                # incremenet score option, top score, top total, grand total
                playersList[j]._scoreDict[scoreSelected] += score
                playersList[j]._topScore += score
                playersList[j]._totalTopScore += score
                playersList[j]._grandTotalScore += score

                # check top bonus, increment top total and grand total
                playersList[j].addTopBonusScore()
                playersList[j]._totalTopScore += playersList[j]._topBonusScore
                playersList[j]._grandTotalScore += playersList[j]._topBonusScore

            # BOTTOM SCORE options and increment scores
            else:
                if scoreSelected == 'three of a kind':
                    score = rollsList[j].checkThreeOfAKind(finalRoll)

                elif scoreSelected == 'four of a kind':
                    score = rollsList[j].checkFourOfAKind(finalRoll)

                elif scoreSelected == 'full house':
                    score = rollsList[j].checkFullHouse(finalRoll)

                elif scoreSelected == 'small straight':
                    score = rollsList[j].checkSmallStraight(finalRoll)

                elif scoreSelected == 'large straight':
                    score = rollsList[j].checkLargeStraight(finalRoll)

                elif scoreSelected == 'yahtzee':
                    score = rollsList[j].checkYahtzee(finalRoll)

                elif scoreSelected == 'chance':
                    score = rollsList[j].addChance(finalRoll)

                elif scoreSelected == 'yahtzee bonus':
                    score = rollsList[j].checkYahtzeeBonus(finalRoll)

                # increment score option, total bottom score, grand total score
                playersList[j]._scoreDict[scoreSelected] += score
                playersList[j]._totalBottomScore += score
                playersList[j]._grandTotalScore += score


if __name__ == "__main__":
    main()
