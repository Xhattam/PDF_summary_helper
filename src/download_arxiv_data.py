""" Script to download PDF and tex sources for a given PDF.
@author Jessica Tanon

JAN 2019
"""

import os
import requests
import sys
import wget
import tarfile
import logging
import subprocess
from os.path import exists, join, isabs, abspath
from arxiv_downloader_helper import get_download_folder

LOCAL_LATEX_SRC_PATH = ""
LOCAL_PDF_PATH = ""
DEST_PATH = ""
logging.basicConfig(level=logging.INFO)


def arxiv_downloader_main(pdf_url):
    """ Calls download functions with correct arguments depending on the download type (pdf, latex sources)

    :param pdf_url: URL to pdf file on arxiv
    :param dest_folder: name of folder that will be created as a download destination
    """

    if is_valid_link(pdf_url):
        logging.info("PDF link: {}".format(pdf_url))
    else:
        sys.exit("Link to {} doesn't work, please check your link".format(pdf_url))

    build_paths(pdf_url)

    download(pdf_url)
    download(pdf_url, extract=True)


def build_paths(pdf_url):
    """ if isabs and exists : write files inside of it
    if isabs and doesn't exist : create folder and write inside of it
    if not is abs: create folder in Downloads, define absath
    :param dest_path:
    :return:
    """

    # Extracting names for folders to be created
    dl_folder_path      = get_download_folder()                         # Getting local Download folder
    pdf_name            = pdf_url.rsplit("/")[-1]                       # 1987.1234.pdf
    dest_folder_name    = pdf_name.rsplit(".", 1)[0].replace(".", "_")  # 1987_1234
    src_folder_path     = dest_folder_name + "_tex_src"                 # 1987_1234_tex_src

    # Setting global variables
    set_dest_path(join(dl_folder_path, dest_folder_name))   # .../Downloads/1987_1234
    set_src_path(src_folder_path)                           # .../Downloads/1987_1234/1987_1234_tex_src
    set_pdf_path(pdf_name)                                  # .../Downloads/1987_1234/1987.1234.pdf

    logging.info("Trying to build destination folder...")
    try:
        os.mkdir(DEST_PATH)
    except OSError as err:
        logging.error("Cannot create destination folder : {}".format(err))
        sys.exit(0)
    logging.info("OK --- Created destination folder at {}".format(DEST_PATH))

    logging.info("Creating latex source folder...")
    os.mkdir(LOCAL_LATEX_SRC_PATH)
    logging.info("OK --- Latex source folder created at {}".format(LOCAL_LATEX_SRC_PATH))


def set_dest_path(dest_path):
    global DEST_PATH
    DEST_PATH = dest_path


def set_pdf_path(pdf_name):
    global LOCAL_PDF_PATH
    LOCAL_PDF_PATH = join(DEST_PATH, pdf_name)


def set_src_path(tex_src_name):
    global LOCAL_LATEX_SRC_PATH
    LOCAL_LATEX_SRC_PATH = join(DEST_PATH, tex_src_name)



def get_dest_path():
    """ Returns destination folder absolute path

    :return: Destination folder absolute path
    """
    return DEST_PATH


def get_pdf_path():
    """ Returns the PDF abs path

    :return: PDF absolute file path
    """
    return LOCAL_PDF_PATH


def get_latex_src_path():
    return LOCAL_LATEX_SRC_PATH


def is_valid_link(link, check_src=False):
    """ Checks if the URL provided to the PDF file is valid

    :param link: link to the PDF file, e.g. `https://arxiv.org/pdf/1812.11928.pdf` """
    logging.info("Checking link validity...")
    request = requests.get(link)
    if request.status_code == 200:
        if check_src:
            headers = request.headers
            # Seems to indicate an attempt to download non-existent sources redirected to the PDF
            if headers['Content-Type'] == 'application/pdf' and headers['Content-Encoding'] == 'gzip':
                return False
        return True
    return False


def build_tex_source_link_name(pdf_dl_link):
    """ Builds tex source folder download link from the pdf link

    :param pdf_dl_link: pdf download link
    :return: tex src folder download link
    """
    base = "https://arxiv.org/e-print/"
    pdf_no_ext = pdf_dl_link.rsplit("/")[-1].rsplit(".", 1)[0]
    return base + pdf_no_ext


def download_pdf(pdf_url):
    try:
        wget.download(pdf_url, out=DEST_PATH)
    except Exception as e:
        logging.error("Cannot download PDF file !")
        sys.exit(e)


def download(link, dest_folder, extract=False):
    """ Downloads PDF or tex source gzip folder with wget

    :param link: link to download
    :param dest_folder: destination of download
    :param extract: option for the tex src case, which is an gzip archive file
    """

    if os.path.exists(LOCAL_PDF_PATH):
        logging.info("File {} already exists, won't download again".format(LOCAL_PDF_PATH))
    else:
        try:
            if extract:
                msg = "Downloading latex sources..."
                out = LOCAL_LATEX_SRC_PATH
            else:
                msg = "Downloading PDF..."
                out = DEST_PATH

            logging.info(msg)
            wget.download(link, out=out)
            logging.info("OK --- Downloaded {} to {}".format(link, out))
        except Exception as e:
            logging.error("Download failed: {}".format(e))

    if extract:
        if not os.path.exists(LOCAL_PDF_PATH + "_tex_src"):
            try:
                extract_src(LOCAL_PDF_PATH + "_tex_src")
            except tarfile.ReadError:
                logging.info("No sources could be found for this article")
                try:
                    subprocess.Popen(["evince", get_pdf_path()])
                except subprocess.CalledProcessError as e:
                    try:
                        subprocess.Popen(["open", get_pdf_path()]) # Mac OS (NOT TESTED)
                    except subprocess.CalledProcessError:
                        sys.exit("Cannot find PDF application, please open {} manually.".format(get_pdf_path()))
                sys.exit(0) # Opening PDF then exiting
    #
    # global DEST_PATH
    # DEST_PATH = os.path.join(PDF_PATH + "_tex_src")


def extract_src(archive_name, dest_path):
    """ Extract downloaded tex src archive

    :param archive_name: name of archive file
    :param dest_path: destination folder
    """
    logging.info("Extracting {}...".format(archive_name))
    tar = tarfile.open(archive_name)
    tar.extractall(path=dest_path)
    tar.close()


if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser(description="Downloader for arxiv PDF and latex source files")
    parser.add_argument("link2pdf", type=str, help="Link to PRD arxiv file")
    parser.add_argument("dest_folder", type=str, help="Destination folder")
    args = parser.parse_args()
    arxiv_downloader_main(**(vars(args)))
