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
        self.datetime_today = '2020-04-20-04:20:00'
        self.game_counter = 0
        self.ranking_dict = [('Joanna Smith', 101), ('John Smith', 100)]
        self.player1 = Player('John Smith')
        self.player2 = Player('Joanna Smith')
        self.players_list = [self.player1, self.player2]

        # setup scores on player instance for file write testing
        self.player1.score_dict = {
            'ones': 25, 'twos': 25, 'threes': 25,
            'fours': 25, 'fives': 25, 'sixes': 25,
            'three of a kind': 25, 'four of a kind': 25,
            'full house': 25, 'small straight': 25,
            'large straight': 25, 'yahtzee': 25,
            'chance': 25, 'yahtzee bonus': 25
            }
        self.player1.top_score = 101
        self.player1.top_bonus_score = 101
        self.player1.total_top_score = 101
        self.player1.total_bottom_score = 101
        self.player1.grand_total_score = 101

        self.player2.score_dict = {
            'ones': 26, 'twos': 26, 'threes': 26,
            'fours': 26, 'fives': 26, 'sixes': 26,
            'three of a kind': 26, 'four of a kind': 26,
            'full house': 26, 'small straight': 26,
            'large straight': 26, 'yahtzee': 26,
            'chance': 26, 'yahtzee bonus': 26
            }
        self.player2.top_score = 102
        self.player2.top_bonus_score = 102
        self.player2.total_top_score = 102
        self.player2.total_bottom_score = 102
        self.player2.grand_total_score = 102

    def tearDown(self):
        """
        Using tearDown instance method here for visibility on utility.
        No real purpose beyond creating namespace and viewing print output.
        """
        try:
            os.remove(
                Path.cwd() / 'data/Textfiles/2020-04-20-04:20:00Game1.txt')
            os.remove(
                Path.cwd() / 'data/Docxfiles/2020-04-20-04:20:00Game1.docx')
        except FileNotFoundError:
            pass

    def test_write_file_txt(self):
        """
        Tests FileWriter for file format 'txt'
        """
        file_formats = ['txt']

        filewriter = FileWriter()
        filewriter.write_file(self.datetime_today, self.game_counter,
                              self.players_list, self.ranking_dict,
                              file_formats)

        self.assertTrue(
            os.path.exists(
                Path.cwd() / 'data/Textfiles/2020-04-20-04:20:00Game1.txt')
            )

    def test_write_file_docx(self):
        """
        Tests FileWriter for file format 'docx'
        """
        file_formats = ['docx']

        filewriter = FileWriter()
        filewriter.write_file(self.datetime_today, self.game_counter,
                              self.players_list, self.ranking_dict,
                              file_formats)

        self.assertTrue(
            os.path.exists(
                Path.cwd() / 'data/Docxfiles/2020-04-20-04:20:00Game1.docx')
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
        self.textfile.relative_path = 'data/test_data/Textfiles'
        self.textfile.datetime_today = '2020-04-20-04:20:00'
        self.textfile.game_counter = 0
        self.textfile.ranking_dict = [('Joanna Smith', 101),
                                      ('John Smith', 100)]
        self.textfile.player1 = Player('John Smith')
        self.textfile.player2 = Player('Joanna Smith')
        self.textfile.players_list = [self.textfile.player1,
                                      self.textfile.player2]

        # setup scores on player instance for file write testing
        self.textfile.player1.score_dict = {
            'ones': 25, 'twos': 25, 'threes': 25,
            'fours': 25, 'fives': 25, 'sixes': 25,
            'three of a kind': 25, 'four of a kind': 25,
            'full house': 25, 'small straight': 25,
            'large straight': 25, 'yahtzee': 25,
            'chance': 25, 'yahtzee bonus': 25
            }
        self.textfile.player1.top_score = 101
        self.textfile.player1.top_bonus_score = 101
        self.textfile.player1.total_top_score = 101
        self.textfile.player1.total_bottom_score = 101
        self.textfile.player1.grand_total_score = 101

        self.textfile.player2.score_dict = {
            'ones': 26, 'twos': 26, 'threes': 26,
            'fours': 26, 'fives': 26, 'sixes': 26,
            'three of a kind': 26, 'four of a kind': 26,
            'full house': 26, 'small straight': 26,
            'large straight': 26, 'yahtzee': 26,
            'chance': 26, 'yahtzee bonus': 26
            }
        self.textfile.player2.top_score = 102
        self.textfile.player2.top_bonus_score = 102
        self.textfile.player2.total_top_score = 102
        self.textfile.player2.total_bottom_score = 102
        self.textfile.player2.grand_total_score = 102

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
                Path.cwd() / self.textfile.relative_path)
            )

    def test_create_textfile_name(self):
        """
        Tests creating textfile filename for textfile output.
        """
        self.textfile.create_textfile_name(self.textfile.game_counter,
                                           self.textfile.datetime_today)

        self.assertEqual(self.textfile.textfile_name,
                         '2020-04-20-04:20:00Game1.txt')

    def test_write_textfile(self):
        """
        Tests writing textfile.
        """
        # create directory and filename
        self.textfile.create_textfile_dir()
        print()
        self.textfile.create_textfile_name(self.textfile.game_counter,
                                           self.textfile.datetime_today)

        # act on file write test
        self.textfile.write_textfile(self.textfile.game_counter,
                                     self.textfile.players_list,
                                     self.textfile.ranking_dict)

        self.assertTrue(os.path.exists(
            Path.cwd() / f'data/test_data/Textfiles/'
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
        self.docxfile.relative_path = 'data/test_data/Docxfiles'
        self.docxfile.datetime_today = '2020-04-20-04:20:00'
        self.docxfile.game_counter = 0
        self.docxfile.ranking_dict = [('Joanna Smith', 101),
                                      ('John Smith', 100)]
        self.docxfile.player1 = Player('John Smith')
        self.docxfile.player2 = Player('Joanna Smith')
        self.docxfile.players_list = [self.docxfile.player1,
                                      self.docxfile.player2]

        # setup scores on player instance for file write testing
        self.docxfile.player1.score_dict = {
            'ones': 25, 'twos': 25, 'threes': 25,
            'fours': 25, 'fives': 25, 'sixes': 25,
            'three of a kind': 25, 'four of a kind': 25,
            'full house': 25, 'small straight': 25,
            'large straight': 25, 'yahtzee': 25,
            'chance': 25, 'yahtzee bonus': 25
            }
        self.docxfile.player1.top_score = 101
        self.docxfile.player1.top_bonus_score = 101
        self.docxfile.player1.total_top_score = 101
        self.docxfile.player1.total_bottom_score = 101
        self.docxfile.player1.grand_total_score = 101

        self.docxfile.player2.score_dict = {
            'ones': 26, 'twos': 26, 'threes': 26,
            'fours': 26, 'fives': 26, 'sixes': 26,
            'three of a kind': 26, 'four of a kind': 26,
            'full house': 26, 'small straight': 26,
            'large straight': 26, 'yahtzee': 26,
            'chance': 26, 'yahtzee bonus': 26
            }
        self.docxfile.player2.top_score = 102
        self.docxfile.player2.top_bonus_score = 102
        self.docxfile.player2.total_top_score = 102
        self.docxfile.player2.total_bottom_score = 102
        self.docxfile.player2.grand_total_score = 102

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
                Path.cwd() / self.docxfile.relative_path)
            )

    def test_create_docx_filename(self):
        """
        Tests creating docx filename for docx file output.
        """
        self.docxfile.create_docx_filename(self.docxfile.game_counter,
                                           self.docxfile.datetime_today)

        self.assertEqual(self.docxfile.docx_filename,
                         '2020-04-20-04:20:00Game1.docx')

    def test_write_docxfile(self):
        """
        Tests writing docx file.
        """
        # create directory and filename
        self.docxfile.create_docxfile_dir()
        print()
        self.docxfile.create_docx_filename(self.docxfile.game_counter,
                                           self.docxfile.datetime_today)

        # act on file write test
        self.docxfile.write_docxfile(self.docxfile.game_counter,
                                     self.docxfile.players_list,
                                     self.docxfile.ranking_dict)

        self.assertTrue(os.path.exists(
            Path.cwd() / f'data/test_data/Docxfiles/'
                         f'2020-04-20-04:20:00Game1.docx'))
