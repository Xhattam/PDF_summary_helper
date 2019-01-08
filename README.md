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


Given an **arxiv** PDF link (e.g `https://arxiv.org/pdf/1901.01911.pdf`) and a destination folder, the script will try to download the PDF file, and search for latex sources.

Sources are found
=================
The latex file is parsed, and the following are extracted:
  - Begining of document until the Introduction section
  - All sections/subsections names
  - Specific latex parts (*itemize*, *enumerate*, *equation*, *table*, *figure*)
  - Bibliography declaration
 
The content of the original latex file is replaced with what was extracted, and formatted so that it can be built with
latex right away (`pdflatex` command). *However*, the purpose is to take notes in this file, and compile it after, so that the note will be clean, in latex, and with the original PDF structure preserved.

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
It is **strongly recommended** to install a full latex version (`sudo apt-get install texlive-full` in Linux), to make sure the user doesn't run into dependencies/missing libraries errors at compilation time.

Evince and Sublime text are the default applications to open the PDF and the `tex` file.

This is a python3 script.

This is a **WORK IN PROGRESS**, any suggestions/bug reports/PR welcome !

USAGE
=====

from the **/src** folder :

**Download, parse, and open documents:**

`python3 arxiv_paper_helper.py https://arxiv.org/pdf/1901.01911.pdf /home/my_dest_folder`

**Download only:**

`python3 download_arxiv_data.py https://arxiv.org/pdf/1901.01911.pdf /home/my_dest_folder`

**Parse and open files only (latex source folder required):**

`python3 parse_latex.py latex_source_folder`

