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
import os
import re

logging.basicConfig(level="INFO")

class TestMultipleLatexIputs(unittest.TestCase):

    def test_files_search(self):
        p = "../resources/1901_recursion"
        a = [os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.expanduser(p)) for f in fn if f.endswith(".tex")]
        for e in a:
            print(e)

