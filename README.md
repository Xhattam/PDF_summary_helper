# PDF_summary_helper
To help you take clean notes !
------------------------------

This small project aims to facilitate note taking for **arxiv** PDF articles

Keywords
========
- arxiv
- latex
- evince
- sublime
- python3


Given an **arxiv** PDF link (e.g `https://arxiv.org/pdf/arxiv_article.pdf`) and a destination folder (e.g *my_new_dest_folder*), the script will try to download the PDF file *arxiv_article.pdf* , and search for latex sources (*arxiv_article_tex_src* will be created).

Sources are found
=================
The `arxiv_article_tex_src/arxiv_article.tex` file is parsed, and the following is extracted:
  - Begining of document until the Introduction section
  - All sections/subsections names
  - Specific latex parts (*itemize*, *enumerate*, *equation*, *table*, *figure*)
  - Bibliography declaration
 
The content of the original `arxiv_article.tex` latex file **is replaced** with what was extracted, and formatted so that it can be built with `latex` right away (`pdflatex` command). *However*, the purpose is to take notes in this file, and compile it after, so that the notes are clean, in latex, and with the original PDF structure preserved.

Once the extraction is done, two subprocesses are called:
- `evince`, to open the original PDF
- `subl*`, to edit the extracted latex sources
An alternative for Mac OS has been added, but not tested.

*`subl` for `Sublime Text`

No sources are found
=====================
`evince` is called to open the PDF.

NOTES
=====
It is **strongly recommended** to install a **full** latex version (`sudo apt-get install texlive-full` in Linux), to make sure the user doesn't run into dependencies/missing libraries errors at compilation time.

`evince` and `Sublime text` are the default applications to open `arxiv-article.pdf` and the `arxiv_article.tex` file.

This is a `python3` script.

This is a **WORK IN PROGRESS**, any suggestions/bug reports/PR welcome !

Work in progress - planned modifications
----------------

- option to select specific latex sections to extract (*itemize*, *equation*...)
- Mac OS compatibility
- make `bibliography`/`abstract` extraction optional
- better paths (abs or not) handling
- thorough error handling and fallback when possible

USAGE
=====

from the **/src** folder :

**Download, parse, and open documents:**

`python3 arxiv_paper_helper.py https://arxiv.org/pdf/arxiv_article.pdf /home/my_new_dest_folder`

**Download only:**

`python3 download_arxiv_data.py https://arxiv.org/pdf/arxiv_article.pdf /home/my_new_dest_folder`

**Parse and open files only (latex source folder required):**

`python3 parse_latex.py arxiv_article_tex_src`

Once you've been through the article and took the notes you wanted in the new (overwritten) `arvice_article.tex` file, provided there are no syntax errors, you can create a PDF of your notes with

`pdflatex arxiv_article.tex`

This file will read the bibliography/images files from the `arxiv_article_tex_src` folder, and build a clean PDF.

**Do NOT: move/rename files.**
If you want to rename your PDF notes, please do so directly on the PDF file ***after*** it's been created.
