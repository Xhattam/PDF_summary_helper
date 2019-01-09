""" Script to test download_archive data
@author Jessica Tanon

JAN 2019
"""

import unittest
from os.path import join, exists
from shutil import rmtree
import parse_latex as pl
import logging
import sys
from os import listdir

logging.basicConfig(level="INFO")

try:
    ORIG1 = open("../resources/ex1_original.tex", 'r').read()
    EXP1 = open("../resources/ex1_expected.tex", 'r').read()
    ORIG2 = open("../resources/ex2_original.tex", 'r').read()
    EXP2 = open("../resources/ex2_expected.tex", 'r').read()
except IOError as e:
    sys.exit("Missing test files, cannot run tests: {}".format(e))


class TestParser(unittest.TestCase):

    def test(self):
        self.assertTrue(True)

    def test_sections_extractor(self):
        expected_sections = [
            "\section{Introduction}",
            "\section{Related Work}",
            "\section{Model}",
            "\subsection{Input and Embedding Layers}",
            "\subsection{LSTM Layer}",
            "\section{Experiments}",
            "\subsection{Datasets}",
            "\subsection{Comparison Methods}",
            "\subsection{Results}",
            "\section{Conclusion}"
        ]

        extracted_sections = [e[0] for e in pl.get_sections(ORIG1)]
        self.assertListEqual(expected_sections, extracted_sections)
