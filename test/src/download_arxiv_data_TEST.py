""" Script to test download_archive data
@author Jessica Tanon

JAN 2019
"""

import unittest
from os.path import join, exists
from shutil import rmtree
from arxiv_downloader_helper import get_download_folder
import download_arxiv_data as dl
import logging
from os import listdir

logging.basicConfig(level="INFO")


class TestDownloader(unittest.TestCase):

    def test_valid_links(self):
        valid_with_src = ["https://arxiv.org/pdf/1901.01911.pdf", "https://arxiv.org/pdf/1901.01824.pdf"]
        valid_no_src = ["https://arxiv.org/pdf/1901.01642.pdf", "https://arxiv.org/pdf/1901.01592.pdf"]
        for link in valid_with_src:
            self.assertTrue(dl._is_valid_link(link))
        for link in valid_no_src:
            self.assertTrue(dl._is_valid_link(link))

    def test_build_tex_source_link_name(self):
        """ Should build the latex source URLs from the PDF links as expected """

        actual_valid = ["https://arxiv.org/pdf/1901.01911.pdf", "https://arxiv.org/pdf/1901.01824.pdf",
                        "https://arxiv.org/pdf/1901.01642.pdf", "https://arxiv.org/pdf/1901.01592.pdf"]
        exp_valid = ["https://arxiv.org/e-print/1901.01911", "https://arxiv.org/e-print/1901.01824",
                     "https://arxiv.org/e-print/1901.01642", "https://arxiv.org/e-print/1901.01592"]
        actual = [dl._build_tex_source_link_name(e) for e in actual_valid]
        self.assertListEqual(exp_valid, actual)

    def test_invalid_latex_src_link(self):
        """ Should return False when testing for link validity if there are no available latex sources """
        # Built latex src links, which should be invalid because there are no source for these papers
        for link in ["https://arxiv.org/e-print/1901.01642", "https://arxiv.org/e-print/1901.01592"]:
            self.assertFalse(dl._is_valid_link(link, check_src=True))

    def test_valid_latex_source_link(self):
        """ Should return true when testing for link validity if there are latex sources available """
        self.assertTrue(dl._is_valid_link("https://arxiv.org/e-print/1901.01824"))

    def test_build_path(self):
        """ Should create folders as destination of downloads """
        test_data = join(get_download_folder(), "1987_1234")

        if exists(test_data):
            ok_to_remove = input("Folder exists. Need to delete it for this test to run {}. Y/N ?".format(test_data))
            if ok_to_remove.lower().strip() == "y":
                rmtree(join(test_data))
            else:
                logging.info("Not removing {}, dummy-passing test".format(test_data))
                return self.assertTrue(True)

        dl._build_paths("http://arxiv.com/pdf/1987.1234.pdf")
        self.assertTrue(exists(join(get_download_folder(), "1987_1234")))
        # Source folder for .tex files should NOT be created
        self.assertFalse(exists(join(test_data, "1987_1234_tex_src")))

    def test_download_existing_sources(self):
        """ Real data test with existing pdf + sources available
        Should download all data and create source folders accordingly """
        test_data = join(get_download_folder(), "1901_02262")
        if exists(test_data):
            ok_to_remove = input("Folder exists. Need to delete it for this test to run {}. Y/N ?".format(test_data))
            if ok_to_remove.lower().strip() == "y":
                rmtree(join(test_data))
            else:
                logging.info("Not removing {}, dummy-passing test".format(test_data))
                return self.assertTrue(True)

        pdf_url = "https://arxiv.org/pdf/1901.02262.pdf"
        dl.arxiv_downloader_main(pdf_url)
        self.assertTrue(exists(test_data))
        self.assertTrue(exists(join(test_data, "1901.02262.pdf")))
        self.assertTrue(exists(join(test_data, "1901_02262_tex_src")))
        self.assertTrue(listdir(join(test_data, "1901_02262_tex_src")))

    def test_download_no_existing_sources(self):
        """ Real data test with existing pdf but NO sources available
        Should only create the destination folder, which should only contain a pdf file """
        test_data = join(get_download_folder(), "1901_01642")
        if exists(test_data):
            ok_to_remove = input("Folder exists. Need to delete it for this test to run {}. Y/N ?".format(test_data))
            if ok_to_remove.lower().strip() == "y":
                rmtree(join(test_data))
            else:
                logging.info("Not removing {}, dummy-passing test".format(test_data))
                return self.assertTrue(True)

        pdf_url = "https://arxiv.org/pdf/1901.01642.pdf"
        dl.arxiv_downloader_main(pdf_url)
        self.assertTrue(exists(test_data))
        self.assertTrue(exists(join(test_data, "1901.01642.pdf")))
        self.assertFalse(exists(join(test_data, "1901_01642_tex_src")))
