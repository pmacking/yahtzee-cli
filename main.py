#!python3

from roll import Roll
from player import Player
import pyinputplus as pyip
from pathlib import Path
from datetime import datetime
import os, time, docx

print('\nWELCOME TO YAHTZEE!')


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

    # GAME LOOP
    gameOver = False
    gameCounter = 0

    while gameOver is False:

        print(f"\nLET'S PLAY! GAME {gameCounter+1}")

        # ROUND LOOP
        for i, k in enumerate(playersList[0]._scoreDict):

            # PLAYER LOOP
            for j, player in enumerate(playersList):

                # skip final round if only yahtzee bonus and yahtzee != 50
                if i == 13 and playersList[j]._scoreDict['yahtzee bonus'] == False and playersList[j]._scoreDict['yahtzee'] != 50:
                    playersList[j]._scoreDict['yahtzee bonus'] = 0
                    print("\nAutomatically score 0 for 'yahtzee bonus'...")

                else:
                    # print current scores and totals before rolling
                    print(f'\n{playersList[j].name.upper()} YOUR TURN. ROUND: {i+1}')

                    print('-'*21)
                    print('ROLL SCORES'.rjust(16))
                    playersList[j].printStackedScoreDict()

                    print('-'*21)
                    print('TOP SCORE BONUS'.rjust(19))
                    print(playersList[j].getTopScore())
                    print(playersList[j].getTopBonusScore())

                    print('-'*21)
                    print('TOTAL SCORES'.rjust(19))
                    print(playersList[j].getTotalTopScore())
                    print(playersList[j].getTotalBottomScore())

                    print('-'*21)
                    print(f"{playersList[j].getGrandTotalScore()}\n")

                    # first roll
                    rollsList[j].rollDice()
                    print(f'{playersList[j].name.upper()}', end='')
                    keepFirstRoll = rollsList[j].keepDice()

                    # second roll
                    rollsList[j].reRollDice(keepFirstRoll)
                    print(f'{playersList[j].name.upper()}', end='')
                    keepSecondRoll = rollsList[j].keepDice()

                    # third roll
                    finalRoll = rollsList[j].finalRollDice(keepSecondRoll)

                    # select score to check final roll against
                    scoreSelected = playersList[j].selectScore()

                    # This section checks either TOP or BOTTOM score per selection
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

                    # else BOTTOM SCORE options and increment scores
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

                            # player cannot score yahztee bonus 50 if no yahtzee
                            if playersList[j]._scoreDict['yahtzee'] != 50:
                                score = 0

                        # increment round, total bottom, and grand total scores
                        playersList[j]._scoreDict[scoreSelected] += score
                        playersList[j]._totalBottomScore += score
                        playersList[j]._grandTotalScore += score

        # END OF ROUND ACTIONS

        # create rankingDict of player and grand total score
        rankingDict = {}
        for j, player in enumerate(playersList):
            rankingName, rankingScore = playersList[j].getNameAndGrandTotalScore()
            rankingDict[rankingName] = rankingScore

        # reverse sort rankingDict by grand total
        rankingDictSorted = sorted(rankingDict.items(), key=lambda x: x[1], reverse=True)

        # print rankings to CLI
        print('\nFINAL SCORES')
        print('-'*12)
        for k, v in enumerate(rankingDictSorted):
            print(f"{k}: {v[0]}: {v[1]}")
        print('\n')

        # END OF GAME ACTIONS

        # OUTPUT SCORES
        print("\nSaving .txt scores file in: 'YahtzeeScores/TextFiles/'...")
        print("\nSaving .docx scores file in: 'YahtzeeScores/DocxFiles/'...")

        # create YahtzeeScores directory
        os.makedirs(Path.cwd() / 'YahtzeeScores', exist_ok=True)

        # CREATE TEXT FILE

        # create TextFiles Directory
        os.makedirs(Path.cwd() / 'YahtzeeScores/TextFiles', exist_ok=True)
        textFileDirStr = str(Path.cwd() / 'YahtzeeScores/TextFiles')

        # create text file filename with datetime and game number
        dateToday = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
        textFilename = f"{dateToday}Game{gameCounter+1}.txt"

        # write scores to text file
        with open(f'{textFileDirStr}/{textFilename}', 'w') as f:
            f.write(f'YAHTZEE GAME {gameCounter+1}\n')
            f.write('FINAL RANKINGS\n')

            # write ranking of all players to file
            f.write(f"\n{'-'*21}")
            for k, v in enumerate(rankingDictSorted):
                f.write(f"\n{v[0]}: {v[1]}")

            # write each player score dict and total scores to file
            for j, player in enumerate(playersList):
                f.write(f"\n{'-'*21}")
                f.write(f"\n{'-'*21}")
                f.write(f"\n{' '*2}{playersList[j].name.upper()} FINAL SCORES\n")

                f.write(f"\n{'ROLL SCORES'.rjust(16)}")
                outputScoreDict = playersList[j].getScoreDict()
                for i, k in enumerate(outputScoreDict):
                    f.write(f"\n{k.rjust(15)}: {outputScoreDict[k]}")

                f.write(f"\n{'-'*21}")
                f.write(f"\n{'TOP SCORE BONUS'.rjust(19)}")
                f.write(f"\n{playersList[j].getTopScore()}".rjust(20))
                f.write(f"\n{playersList[j].getTopBonusScore()}\n".rjust(20))

                f.write(f"\n{'TOTAL SCORES'.rjust(19)}")
                f.write(f"\n{playersList[j].getTotalTopScore()}".rjust(20))
                f.write(f"\n{playersList[j].getTotalBottomScore()}".rjust(20))

                f.write(f"\n{'-'*21}")
                f.write(f"\n{playersList[j].getGrandTotalScore()}".rjust(20))
                f.write('\n')

        # CREATE WORD FILE

        # create Docx Directory
        os.makedirs(Path.cwd() / 'YahtzeeScores/DocxFiles', exist_ok=True)
        docxFileDirStr = str(Path.cwd() / 'YahtzeeScores/DocxFiles')

        # create docx file filename with datetime and game number
        docxFilename = f"{dateToday}Game{gameCounter+1}.docx"

        # change cwd to ./YahtzeeScores/DocxFiles/ for writing docx files
        os.chdir(docxFileDirStr)

        # open blank Document object
        doc = docx.Document()
        doc.add_paragraph(f'YAHTZEE GAME {gameCounter+1}', 'Title')
        doc.paragraphs[0].runs[0].add_break()

        doc.add_heading('FINAL RANKINGS', 1)
        for k, v in enumerate(rankingDictSorted):
            doc.add_paragraph(f"{v[0]}: {v[1]}")

        # add page break after rankings
        paraObjRankings = doc.add_paragraph('   ')
        paraObjRankings.runs[0].add_break(docx.enum.text.WD_BREAK.PAGE)

        # write each player score dict and total scores to file
        doc.add_heading('PLAYER SCORES AND TOTALS', 1)
        for j, player in enumerate(playersList):

            # write player name as header
            doc.add_heading(f"{playersList[j].name.upper()}", 2)

            # write player roll scores for each scoring option
            doc.add_heading('ROLL SCORES', 3)
            outputScoreDict = playersList[j].getScoreDict()
            for i, k in enumerate(outputScoreDict):
                doc.add_paragraph(f"{k}: {outputScoreDict[k]}")

            # write top score and bonus
            doc.add_heading('TOP SCORE BONUS', 3)
            doc.add_paragraph(f"{playersList[j].getTopScore()}")
            doc.add_paragraph(f"{playersList[j].getTopBonusScore()}")

            # write total scores and grand total
            doc.add_heading('TOTAL SCORES', 3)
            doc.add_paragraph(f"{playersList[j].getTotalTopScore()}")
            doc.add_paragraph(f"{playersList[j].getTotalBottomScore()}")
            paraObjGT = doc.add_paragraph(f"{playersList[j].getGrandTotalScore()}")

            # add pagebreak before writing next player scores to docx
            if j != (len(playersList)-1):
                paraObjGT.runs[0].add_break(docx.enum.text.WD_BREAK.PAGE)

        # save Document object as docxFilename
        doc.save(docxFilename)

        # clear each player _scoreDict and totals for next round
        print('\nResetting dice for next round...')
        time.sleep(1)
        for j, player in enumerate(playersList):
            playersList[j].resetAllScores()

        # increment game counter, if three games end match
        gameCounter += 1
        if gameCounter == 3:
            print('GAME OVER')
            gameOver = True


if __name__ == "__main__":
    main()
