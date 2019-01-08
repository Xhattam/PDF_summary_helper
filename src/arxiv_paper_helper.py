""" Wrapper script calling `download_arxiv_data` and `parse_latex` scripts.

@author Jessica Tanon

JAN 2019
"""

from download_arxiv_data import arxiv_downloader_main, get_dest_path, get_pdf_path
from parse_latex import parser_main, get_tex_path
import subprocess
import sys


def paper_helper_main(pdf_url, dest):
    """ Calls download and parsing functions.

    :param pdf_url: URL if PDF to download sources from, when possible
    :param dest: name of folder to save download/results/PDF to
    :return:
    """
    arxiv_downloader_main(pdf_url, dest)
    dest_path = get_dest_path()
    parser_main(dest_path)

    try:
        subprocess.Popen(["evince", get_pdf_path()])
    except subprocess.CalledProcessError as e:
        try:
            subprocess.Popen(["open", get_pdf_path()]) # Mac OS (NOT TESTED)
        except subprocess.CalledProcessError:
            sys.exit("Cannot find PDF application, please open {} manually.".format(get_pdf_path()))

    try:
        subprocess.Popen(["subl", "-w", get_tex_path()])
    except subprocess.CalledProcessError:  # Mac OS
        try:
            subprocess.Popen(["open", '-a', 'TextEdit', get_tex_path])  # Mac OS (NOT TESTED)
        except subprocess.CalledProcessError:
            sys.exit("Cannot find text editor application, please open {} manually.".format(get_tex_path()))


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(description="Downloads an arxiv PDF file, searches for latex sources when \
                                                 available, downloads sources, and extract skeleton from the \
                                                 text file, ready to be annotated. Opens a pdf reader and a text editor\
                                                 so that the user can start reading the paper and taking notes ready\
                                                 to be compiled to pdf from latex.")
    parser.add_argument("pdf_url", type=str, help="URL to PDF")
    parser.add_argument("dest", type=str, help="Name of folder to save data to (will be created if it doesn't exist)")

    args = parser.parse_args()
    paper_helper_main(**vars(args))
