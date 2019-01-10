""" Script to test download_archive data
@author Jessica Tanon

JAN 2019
"""

import unittest
import parse_latex as pl
import logging
import sys
import re

logging.basicConfig(level="INFO")

try:
    ORIG1 = open("../resources/ex1_original.tex", 'r').read()
    EXP1 = open("../resources/ex1_expected.tex", 'r').read()
    ORIG2 = open("../resources/ex2_original.tex", 'r').read()
    EXP2 = open("../resources/ex2_expected.tex", 'r').read()
    COMM = open("../resources/with_comments_orig.tex", 'r').read()
    NO_COMM = open("../resources/commentes_removed_expected.tex", 'r').read()
except IOError as e:
    sys.exit("Missing test files, cannot run tests: {}".format(e))


class TestParser(unittest.TestCase):

    def test_sections_extractor_ex1(self):
        expected_sections = [
            "\section{Introduction}",
            "\section{Related Work}",
            "\section{Model}",
            "\subsection{Input and Embedding Layers}",
            "\subsection{LSTM Layer}",
            "\subsection{Task-Specific Attention Layer}",
            "\subsection{Regularization Layer}",
            "\section{Experiments}",
            "\subsection{Datasets}",
            "\subsection{Comparison Methods}",
            "\subsection{Results}",
            "\section{Conclusion}"
        ]

        extracted_sections = [e[1] for e in pl.get_sections(ORIG1)]
        self.assertListEqual(expected_sections, extracted_sections)

    def test_sections_extractor_ex2(self):
        self.maxDiff = None
        expected = [
            "\section{Introduction}",
            "\section{Problem Formulation}",
            "\section{Proposed Model}",
            "\subsection{Question-Passages Reader}",
            "\subsubsection{Word Embedding Layer}",
            "\subsubsection{Dual Attention Layer}",
            "\subsubsection{Modeling Encoder Layer}",
            "\paragraph{Copy distribution.}",
            "\section{Experiments}",
            "\subsection{Setup}",
            "\paragraph{Datasets and styles.}",
            "\paragraph{Does our multi-style learning improve NLG performance?}",
            "\section{Conclusion}",
            "\section{Reading Comprehension Examples generated by Masque from MS MARCO 2.1}"
        ]

        extracted = [e[1] for e in pl.get_sections(ORIG2)]
        self.assertListEqual(expected, extracted)

    def test_extract_all_ex1(self):
        extracted_content = pl.get_all(ORIG1)
        self.assertEqual(extracted_content, EXP1)

    def test_extract_all_ex2(self):
        self.maxDiff = None
        extracted_content = pl.get_all(ORIG2)
        self.assertEqual(extracted_content, EXP2)
