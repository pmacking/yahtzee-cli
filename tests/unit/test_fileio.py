"""Unit test for fileio.py"""

import unittest
from pathlib import Path
import os
import shutil

from yahtzee.fileio import FileWriter, TextFile, DocxFile
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
        pass

    @classmethod
    def tearDownClass(cls):
        """
        Using tearDownClass class method for visibility and practice utility.
        No real purpose beyond creating namespace and viewing print output.
        """
        pass

    def setUp(self):
        """
        Sets up class instances required for all testing methods.
        """
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
        try:
            os.remove(
                Path.cwd() / 'data/TextFiles/2020-04-20-04:20:00Game1.txt')
            os.remove(
                Path.cwd() / 'data/DocxFiles/2020-04-20-04:20:00Game1.docx')
        except FileNotFoundError:
            pass

    def test_writeFile_txt(self):
        """
        Tests FileWriter for file format 'txt'
        """
        fileFormats = ['txt']

        filewriter = FileWriter()
        filewriter.write_file(self.dateTimeToday, self.gameCounter,
                              self.playersList, self.rankingDict, fileFormats)

        self.assertTrue(
            os.path.exists(
                Path.cwd() / 'data/TextFiles/2020-04-20-04:20:00Game1.txt')
            )

    def test_writeFile_docx(self):
        """
        Tests FileWriter for file format 'docx'
        """
        fileFormats = ['docx']

        filewriter = FileWriter()
        filewriter.write_file(self.dateTimeToday, self.gameCounter,
                              self.playersList, self.rankingDict, fileFormats)

        self.assertTrue(
            os.path.exists(
                Path.cwd() / 'data/DocxFiles/2020-04-20-04:20:00Game1.docx')
            )


class TestTextFile(unittest.TestCase):
    """
    Unit tests for the :class: `TextFile <TextFile>`.
    """
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        """
        Sets up instances and test attributes for testing TextFile methods.
        """
        # create instance of TextFile for testing instance methods
        self.textfile = TextFile()

        # setup attributes
        self.textfile.relativePath = 'data/test_data/TextFile'
        self.textfile.dateTimeToday = '2020-04-20-04:20:00'
        self.textfile.gameCounter = 0
        self.textfile.rankingDict = [('Joanna Smith', 101),
                                     ('John Smith', 100)]
        self.textfile.player1 = Player('John Smith')
        self.textfile.player2 = Player('Joanna Smith')
        self.textfile.playersList = [self.textfile.player1,
                                     self.textfile.player2]

        # setup scores on player instance for file write testing
        self.textfile.player1.scoreDict = {
            'ones': 25, 'twos': 25, 'threes': 25,
            'fours': 25, 'fives': 25, 'sixes': 25,
            'three of a kind': 25, 'four of a kind': 25,
            'full house': 25, 'small straight': 25,
            'large straight': 25, 'yahtzee': 25,
            'chance': 25, 'yahtzee bonus': 25
            }
        self.textfile.player1.topScore = 101
        self.textfile.player1.topBonusScore = 101
        self.textfile.player1.totalTopScore = 101
        self.textfile.player1.totalBottomScore = 101
        self.textfile.player1.grandTotalScore = 101

        self.textfile.player2.scoreDict = {
            'ones': 26, 'twos': 26, 'threes': 26,
            'fours': 26, 'fives': 26, 'sixes': 26,
            'three of a kind': 26, 'four of a kind': 26,
            'full house': 26, 'small straight': 26,
            'large straight': 26, 'yahtzee': 26,
            'chance': 26, 'yahtzee bonus': 26
            }
        self.textfile.player2.topScore = 102
        self.textfile.player2.topBonusScore = 102
        self.textfile.player2.totalTopScore = 102
        self.textfile.player2.totalBottomScore = 102
        self.textfile.player2.grandTotalScore = 102

    def tearDown(self):
        """
        Tears down class artifacts created during testing.
        """
        try:
            shutil.rmtree(Path.cwd() / 'data/test_data')
        except FileNotFoundError:
            pass

    def test_create_textfile_dir(self):
        """
        Tests creating directory for textfile output.
        """
        self.textfile.create_textfile_dir()

        self.assertTrue(
            os.path.exists(
                Path.cwd() / self.textfile.relativePath)
            )

    def test_create_textfile_name(self):
        """
        Tests creating textfile filename for textfile output.
        """
        self.textfile.create_textfile_name(self.textfile.gameCounter,
                                           self.textfile.dateTimeToday)

        self.assertEqual(self.textfile.textFilename,
                         '2020-04-20-04:20:00Game1.txt')

    def test_writeTextFile(self):
        """
        Tests writing textfile.
        """
        # create directory and filename
        self.textfile.create_textfile_dir()
        print()
        self.textfile.create_textfile_name(self.textfile.gameCounter,
                                           self.textfile.dateTimeToday)

        # act on file write test
        self.textfile.write_text_file(self.textfile.gameCounter,
                                      self.textfile.playersList,
                                      self.textfile.rankingDict)

        self.assertTrue(os.path.exists(
            Path.cwd() / f'data/test_data/TextFile/'
                         f'2020-04-20-04:20:00Game1.txt'))


class TestDocxFile(unittest.TestCase):
    """
    Unit tests for the :class: `DocxFile <DocxFile>`.
    """
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        """
        Sets up instances and test attributes for testing DocxFile methods.
        """
        # create instance of DocxFile for testing instance methods
        self.docxfile = DocxFile()

        # setup attributes
        self.docxfile.relativePath = 'data/test_data/DocxFile'
        self.docxfile.dateTimeToday = '2020-04-20-04:20:00'
        self.docxfile.gameCounter = 0
        self.docxfile.rankingDict = [('Joanna Smith', 101),
                                     ('John Smith', 100)]
        self.docxfile.player1 = Player('John Smith')
        self.docxfile.player2 = Player('Joanna Smith')
        self.docxfile.playersList = [self.docxfile.player1,
                                     self.docxfile.player2]

        # setup scores on player instance for file write testing
        self.docxfile.player1.scoreDict = {
            'ones': 25, 'twos': 25, 'threes': 25,
            'fours': 25, 'fives': 25, 'sixes': 25,
            'three of a kind': 25, 'four of a kind': 25,
            'full house': 25, 'small straight': 25,
            'large straight': 25, 'yahtzee': 25,
            'chance': 25, 'yahtzee bonus': 25
            }
        self.docxfile.player1.topScore = 101
        self.docxfile.player1.topBonusScore = 101
        self.docxfile.player1.totalTopScore = 101
        self.docxfile.player1.totalBottomScore = 101
        self.docxfile.player1.grandTotalScore = 101

        self.docxfile.player2.scoreDict = {
            'ones': 26, 'twos': 26, 'threes': 26,
            'fours': 26, 'fives': 26, 'sixes': 26,
            'three of a kind': 26, 'four of a kind': 26,
            'full house': 26, 'small straight': 26,
            'large straight': 26, 'yahtzee': 26,
            'chance': 26, 'yahtzee bonus': 26
            }
        self.docxfile.player2.topScore = 102
        self.docxfile.player2.topBonusScore = 102
        self.docxfile.player2.totalTopScore = 102
        self.docxfile.player2.totalBottomScore = 102
        self.docxfile.player2.grandTotalScore = 102

    def tearDown(self):
        """
        Tears down class artifacts created during testing.
        """
        try:
            shutil.rmtree(Path.cwd() / 'data/test_data')
        except FileNotFoundError:
            pass

    def test_create_docxfile_dir(self):
        """
        Tests creating directory for docx file output.
        """
        self.docxfile.create_docxfile_dir()

        self.assertTrue(
            os.path.exists(
                Path.cwd() / self.docxfile.relativePath)
            )

    def test_create_docx_filename(self):
        """
        Tests creating docx filename for docx file output.
        """
        self.docxfile.create_docx_filename(self.docxfile.gameCounter,
                                           self.docxfile.dateTimeToday)

        self.assertEqual(self.docxfile.docxFilename,
                         '2020-04-20-04:20:00Game1.docx')

    def test_write_docxfile(self):
        """
        Tests writing docx file.
        """
        # create directory and filename
        self.docxfile.create_docxfile_dir()
        print()
        self.docxfile.create_docx_filename(self.docxfile.gameCounter,
                                           self.docxfile.dateTimeToday)

        # act on file write test
        self.docxfile.write_docxfile(self.docxfile.gameCounter,
                                     self.docxfile.playersList,
                                     self.docxfile.rankingDict)

        self.assertTrue(os.path.exists(
            Path.cwd() / f'data/test_data/DocxFile/'
                         f'2020-04-20-04:20:00Game1.docx'))
