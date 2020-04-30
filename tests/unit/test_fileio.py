"""Unit test for fileio.py"""

import unittest
from unittest.mock import patch
from pathlib import Path
import os

from yahtzee.fileio import FileWriter
from yahtzee.player import Player


class TestFileWriter(unittest.TestCase):
    """
    Unit tests for the :class: `FileWriter <FileWriter>`.
    """
    @classmethod
    def setUpClass(cls):
        """
        Using setUpClass class method for visibility and practice utility.
        No real purpose beyond creating namespace and viewing print output.
        """
        print('setUpClass class method')

    @classmethod
    def tearDownClass(cls):
        """
        Using tearDownClass class method for visibility and practice utility.
        No real purpose beyond creating namespace and viewing print output.
        """
        print('tearDownClass class method')

    def setUp(self):
        """
        Sets up class instances required for all testing methods.
        """
        print('setUp')

        # setup attributes
        self.dateTimeToday = '2020-04-20-04:20:00'
        self.gameCounter = 0
        self.rankingDict = [('Joanna Smith', 101), ('John Smith', 100)]
        self.player1 = Player('John Smith')
        self.player2 = Player('Joanna Smith')
        self.playersList = [self.player1, self.player2]

        # setup scores on player instance for file write testing
        self.player1.scoreDict = {
            'ones': 25, 'twos': 25, 'threes': 25,
            'fours': 25, 'fives': 25, 'sixes': 25,
            'three of a kind': 25, 'four of a kind': 25,
            'full house': 25, 'small straight': 25,
            'large straight': 25, 'yahtzee': 25,
            'chance': 25, 'yahtzee bonus': 25
            }
        self.player1.topScore = 101
        self.player1.topBonusScore = 101
        self.player1.totalTopScore = 101
        self.player1.totalBottomScore = 101
        self.player1.grandTotalScore = 101

        self.player2.scoreDict = {
            'ones': 26, 'twos': 26, 'threes': 26,
            'fours': 26, 'fives': 26, 'sixes': 26,
            'three of a kind': 26, 'four of a kind': 26,
            'full house': 26, 'small straight': 26,
            'large straight': 26, 'yahtzee': 26,
            'chance': 26, 'yahtzee bonus': 26
            }
        self.player2.topScore = 102
        self.player2.topBonusScore = 102
        self.player2.totalTopScore = 102
        self.player2.totalBottomScore = 102
        self.player2.grandTotalScore = 102

    def tearDown(self):
        """
        Using tearDown instance method here for visibility on utility.
        No real purpose beyond creating namespace and viewing print output.
        """
        print('tearDown')

    # test FileWriter for file format 'txt'
    def test_writeFile_txt(self):
        fileFormats = ['txt']

        filewriter = FileWriter()
        filewriter.writeFile(self.dateTimeToday, self.gameCounter,
                             self.playersList, self.rankingDict, fileFormats)

        self.assertTrue(Path.cwd() / 'data/2020-04-20-04:20:00.txt')

    # test FileWriter for file format 'docx'
    def test_writeFile_docx(self):
        fileFormats = ['docx']

        filewriter = FileWriter()
        filewriter.writeFile(self.dateTimeToday, self.gameCounter,
                             self.playersList, self.rankingDict, fileFormats)

        self.assertTrue(Path.cwd() / 'data/2020-04-20-04:20:00.docx')

    # # test FileWriter for file format 'pdf'
    # def test_writeFile_pdf(self):
    #     fileFormats = ['pdf']

    #     filewriter = FileWriter()
    #     # docx dir and filename to test as convertDocxToPdf args
    #     filewriter.docxFileDirStr = 'testDocxFileDir'
    #     filewriter.docxFilename = 'testDocxFilename.docx'
    #     filewriter.writeFile(self.dateTimeToday, self.gameCounter,
    #                          self.playersList, self.rankingDict, fileFormats)

    #     self.assertTrue(Path.cwd() / 'data/2020-04-20-04:20:00.pdf')
