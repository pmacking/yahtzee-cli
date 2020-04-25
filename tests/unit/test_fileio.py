"""Unit test for fileio.py"""

import unittest
from unittest.mock import patch

from yahtzee.fileio import FileWriter, TextFile, DocxFile, PdfFile
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
        self.rankingDict = [('John Smith', 100)]
        player = Player('John Smith')
        self.playersList = [player]

    def tearDown(self):
        """
        Using tearDown instance method here for visibility on utility.
        No real purpose beyond creating namespace and viewing print output.
        """
        print('tearDown')

    # test FileWriter for file format 'txt'
    @patch('yahtzee.fileio.TextFile', spec=True)
    def test_writeFile_txt(self, mock_textFileClass):
        fileFormats = ['txt']

        # mock instance of TextFile and set path attributes
        mockTextFile = mock_textFileClass()
        mockTextFile.textFileDirStr = 'testTextFileDirStr'
        mockTextFile.textFilename = 'testTextFilename.txt'

        filewriter = FileWriter()
        filewriter.writeFile(self.dateTimeToday, self.gameCounter,
                             self.playersList, self.rankingDict, fileFormats)

        self.assertTrue(True)

    # test FileWriter for file format 'docx'
    @patch('yahtzee.fileio.DocxFile', spec=True)
    def test_writeFile_docx(self, mock_docxFileClass):
        fileFormats = ['docx']

        # mock instance of DocxFile and set path attributes
        mockDocxFile = mock_docxFileClass()
        mockDocxFile.docxFileDirStr = 'testDocxFileDirStr'
        mockDocxFile.docxFilename = 'testDocxFilename.docx'

        filewriter = FileWriter()
        filewriter.writeFile(self.dateTimeToday, self.gameCounter,
                             self.playersList, self.rankingDict, fileFormats)

        self.assertTrue(True)

    # test FileWriter for file format 'pdf'
    @patch('yahtzee.fileio.PdfFile', spec=True)
    def test_writeFile_pdf(self, mock_pdfFileClass):
        fileFormats = ['pdf']

        # mock instance of PdfFile and set path attributes
        mockPdfFile = mock_pdfFileClass()
        mockPdfFile.pdfFileDirStr = 'testPdfFileDirStr'
        mockPdfFile.pdfFilename = 'testPdfFilename.pdf'

        filewriter = FileWriter()
        # docx dir and filename to test as convertDocxToPdf args
        filewriter.docxFileDirStr = 'testDocxFileDir'
        filewriter.docxFilename = 'testDocxFilename.docx'
        filewriter.writeFile(self.dateTimeToday, self.gameCounter,
                             self.playersList, self.rankingDict, fileFormats)

        self.assertTrue(True)
