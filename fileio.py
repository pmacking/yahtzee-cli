#!python3

from pathlib import Path
import os


def createFileioDirectory():
    '''
    Creates YahtzeeScores/ folder in cwd
    '''
    os.makedirs(Path.cwd() / 'YahtzeeScores', exist_ok=True)


def printFileioConfirmation(fileDirStr, fileName):
    '''
    Prints confirmation message when file creation completed
    '''
    print(f"\nSaved scores file: '{fileDirStr}/{fileName}'")


class TextFile:
    '''
    Creates text file of players and scores
    '''
    def __init__(self, gameCounter, playersList, rankingDict, dateTimeToday):
        self._gameCounter = gameCounter
        self._playersList = playersList
        self._rankingDict = rankingDict
        self._dateTimeToday = dateTimeToday

        # instance method objects
        self._textFileDirStr = ''
        self._textFilename = ''

    def createTextFileDir(self):
        '''
        Create TextFiles folder.
        '''
        os.makedirs(Path.cwd() / 'YahtzeeScores/TextFiles', exist_ok=True)
        self._textFileDirStr = str(Path.cwd() / 'YahtzeeScores/TextFiles')

    def createTextFilename(self):
        '''
        Create text file filename with datetime and game number
        '''
        self._textFilename = f"{self._dateTimeToday}Game{self._gameCounter+1}.txt"

    def writeTextFile(self):
        '''
        Writes players scores to text file
        '''
        with open(f'{self._textFileDirStr}/{self._textFilename}', 'w') as f:
            f.write(f'YAHTZEE GAME {self._gameCounter+1}\n')
            f.write('FINAL RANKINGS\n')

            # write ranking of all players to file
            f.write(f"{'-'*21}")
            for k, v in enumerate(self._rankingDict):
                f.write(f"\n{v[0]}: {v[1]}")
            f.write(f"\n{'-'*21}\n")

            # write each player score dict and total scores to file
            for j, player in enumerate(self._playersList):
                f.write(f"\n{'-'*21}")
                f.write(f"\n{'-'*21}")
                f.write(f"\n{' '*2}{self._playersList[j].name.upper()} FINAL SCORES\n")

                f.write(f"\n{'ROLL SCORES'.rjust(16)}")
                outputScoreDict = self._playersList[j].getScoreDict()
                for i, k in enumerate(outputScoreDict):
                    f.write(f"\n{k.rjust(15)}: {outputScoreDict[k]}")

                f.write(f"\n{'-'*21}\n")
                f.write(f"{'TOP SCORE BONUS'.rjust(19)}\n")
                f.write(f"{self._playersList[j].getTopScore()}\n".rjust(20))
                f.write(f"{self._playersList[j].getTopBonusScore()}\n".rjust(20))

                f.write(f"\n{'TOTAL SCORES'.rjust(19)}\n")
                f.write(f"{self._playersList[j].getTotalTopScore()}\n".rjust(20))
                f.write(f"{self._playersList[j].getTotalBottomScore()}\n".rjust(20))

                f.write(f"\n{'-'*21}\n")
                f.write(f"{self._playersList[j].getGrandTotalScore()}\n".rjust(20))
                f.write('\n')

            # print file creation confirmation
            printFileioConfirmation(self._textFileDirStr, self._textFilename)

# # CREATE WORD FILE

# # create Docx Directory
# os.makedirs(Path.cwd() / 'YahtzeeScores/DocxFiles/', exist_ok=True)
# docxFileDirStr = str(Path.cwd() / 'YahtzeeScores/DocxFiles/')

# # create docx file filename with datetime and game number
# docxFilename = f"{dateToday}Game{self._gameCounter+1}.docx"

# # open blank Document object
# doc = docx.Document()
# doc.add_paragraph(f'YAHTZEE GAME {self._gameCounter+1}', 'Title')
# doc.paragraphs[0].runs[0].add_break()

# # add picture of yahtzee game to document
# doc.add_picture(str(Path.cwd() / 'yahtzeePicture.jpg'))

# doc.add_heading('FINAL RANKINGS', 1)
# for k, v in enumerate(self._rankingDict):
#     doc.add_paragraph(f"{v[0]}: {v[1]}")

# # add page break after rankings
# paraObjRankings = doc.add_paragraph('   ')
# paraObjRankings.runs[0].add_break(docx.enum.text.WD_BREAK.PAGE)

# # write each player score dict and total scores to file
# doc.add_heading('PLAYER SCORES AND TOTALS', 1)
# for j, player in enumerate(self._playersList):

#     # write player name as header
#     doc.add_heading(f"{self._playersList[j].name.upper()}", 2)

#     # write player roll scores for each scoring option
#     doc.add_heading('ROLL SCORES', 3)
#     outputScoreDict = self._playersList[j].getScoreDict()
#     for i, k in enumerate(outputScoreDict):
#         doc.add_paragraph(f"{k}: {outputScoreDict[k]}")

#     # write top score and bonus
#     doc.add_heading('TOP SCORE BONUS', 3)
#     doc.add_paragraph(f"{self._playersList[j].getTopScore()}")
#     doc.add_paragraph(f"{self._playersList[j].getTopBonusScore()}")

#     # write total scores and grand total
#     doc.add_heading('TOTAL SCORES', 3)
#     doc.add_paragraph(f"{self._playersList[j].getTotalTopScore()}")
#     doc.add_paragraph(f"{self._playersList[j].getTotalBottomScore()}")
#     paraObjGT = doc.add_paragraph(f"{self._playersList[j].getGrandTotalScore()}")

#     # add pagebreak before writing next player scores to docx
#     if j != (len(self._playersList)-1):
#         paraObjGT.runs[0].add_break(docx.enum.text.WD_BREAK.PAGE)

# # save Document object as docxFilename
# doc.save(f"{docxFileDirStr}/{docxFilename}")
# print("\nSaved .docx scores file in: 'YahtzeeScores/DocxFiles/'...")

# # CONVERT TO PDF

# # create PDF Directory
# os.makedirs(Path.cwd() / 'YahtzeeScores/pdfFiles/', exist_ok=True)
# pdfFileDirStr = str(Path.cwd() / 'YahtzeeScores/pdfFiles/')

# # convert docx to pdf
# convert(f"{docxFileDirStr}/{docxFilename}", f"{pdfFileDirStr}/{docxFilename[:-5]}.pdf")
# print("\nSaved pdf scores file in: 'YahtzeeScores/pdfFiles/'...")
