''' Script to download PDF and tex sources for a given PDF.
@author Jessica Tanon

JAN 2019
'''

import os
import requests
import sys
import wget
import tarfile
import logging

DEST_PATH = ""
PDF_PATH = ""
logging.basicConfig(level=logging.WARN)


def downloader_main(link2pdf, dest_folder, force_dl):
    if is_valid_link(link2pdf):
        logging.info("PDF link: {}".format(link2pdf))
    else:
        sys.exit("Link to {} doesn't work, please check your link".format(link2pdf))
    logging.info("Destination folder: {}".format(dest_folder))

    link2src = build_tex_source_link_name(link2pdf)
    if os.path.exists(dest_folder):
        logging.error("Provided folder name already exists. Please delete it, or provide another name.")
        sys.exit()
    else:
        os.mkdir(dest_folder.strip())

    download(link2pdf, dest_folder, force_dl)
    download(link2src, dest_folder, force_dl, extract=True)


def get_dest_path():
    return DEST_PATH


def get_pdf_path():
    return PDF_PATH + ".pdf"


def is_valid_link(link):
    """ Checks if the URL provided to the PDF file is valid

    :param link: link to the PDF file, e.g. `https://arxiv.org/pdf/1812.11928` """
    request = requests.get(link)
    if request.status_code == 200:
        return True
    return False


def build_tex_source_link_name(pdf_dl_link):
    """ Extracts tex src folder download link from the pdf link

    :param pdf_dl_link: pdf download link
    :return: tex src folder download link
    """
    base = "https://arxiv.org/e-print/"
    pdf_no_ext = pdf_dl_link.rsplit("/")[-1].rsplit(".", 1)[0]
    return base + pdf_no_ext


def download(link, dest_folder, force_dl, extract=False):
    """ Downloads PDF or tex source gzip folder with wget

    :param link: link to download
    :param dest_folder: destination of download
    :param force_dl: if True, will download again if the file already exists
    :param extract: option for the tex src case, which is an gzip archive file
    """
    name = link.rsplit("/")[-1]
    global PDF_PATH
    PDF_PATH = os.path.join(dest_folder, name)
    if os.path.exists(PDF_PATH) and not force_dl:
        logging.info("File {} already exists, won't download again".format(PDF_PATH))
    else:
        try:
            wget.download(link, out=dest_folder)
        except Exception as e:
            logging.error("Download failed: {}".format(e))
    if extract:
        if not os.path.exists(PDF_PATH + "_tex_src"):
            extract_src(PDF_PATH, PDF_PATH + "_tex_src")
    global DEST_PATH
    DEST_PATH = os.path.join(PDF_PATH + "_tex_src")


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
    parser = argparse.ArgumentParser()
    parser.add_argument("link2pdf", type=str, help="Link to PRD arxiv file")
    parser.add_argument("dest_folder", type=str, help="Destination folder")
    parser.add_argument("-force_dl", action="store_true", help="If file already exist, download again", default=False)
    args = parser.parse_args()
    downloader_main(**(vars(args)))


