""" Script to test multiple inputs replacements
@author Jessica Tanon

JAN 2019
"""

import unittest
from os.path import join, exists
from shutil import rmtree
from arxiv_downloader_helper import get_download_folder
import parse_latex as pl
import logging
from os import listdir
import re

logging.basicConfig(level="INFO")

ORIG1 = open("../resources/1901/appendix.tex").read()
EXP1 = open("../resources/multiple_inputs_ex1_expected.tex").read()

e = {r'introduction' : "WOW MUCH INTRO",
     r'theory' : r'SUCH THEORY'
     }


class TestMultipleInputs(unittest.TestCase):

    def test_this(self):
        #self.maxDiff = None
        replaced = pl.parser_main("/home/jessica/Python_Code/arxiv-pdf-summary-helper/test/resources/multiple_inputs_src")
        #print(replaced)
        self.assertEqual(EXP1, replaced)
