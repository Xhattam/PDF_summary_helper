""" Script to parse a latex file and extract main info (title, authors, abstract...), section names, and specific latex
elements such as formulas or tables.

@author Jessica Tanon

JAN 2019
"""


import re
import os
import sys

TEX_FILE_PATH = ""


def get_tex_path():
    """ Gets latex file abs path

    :return: latex source file absolute path
    """
    return TEX_FILE_PATH


def get_sections(text):
    """ Finds all section and subsections names in the latex file

    :param text: content of the latex file
    :return: iterator with section/subsection names, in latex format: `\section{section name}`
    """
    tmp = re.finditer(r"^(?!%)\\(s(?:ubs)?ection|paragraph){.*}( |$)", text, re.MULTILINE)
    # Removing elements with multiple }
    """ Ex: \paragraph{Multi-source abstractive summarization based RC.} The first idea is to use a pointer-generator 
    mechanism for multi-passage RC, which was originally proposed for text summarization~\citep{SeeLM17}. 
    \citet{HasselqvistHK17} and \citet{McCannKXS18} 
    This is matched instead of just paragraph{.*} because of the following \cite{} elements
    """
    return [(e.start(), e.group().strip().split("}")[0] + "}") for e in tmp]


def get_figure(text):
    """ Extracts specific latex elements (currently, figure, itemize, equation, table and enumerate sections)

    :param text: content of the latex file
    :return: iterator with all specific elements and their content, in latex format
    """

    return re.finditer(r'((?<!\\begin{comment})\s\\begin{(?P<sec>(?:figure\*{0,1}|itemize|equation|table|enumerate))}(?:.*?)\\end{(?P=sec)})', text, re.S)


def get_all(text):
    """ Creates blueprint of original latex src
    Calls all extraction functions. Gets header, content, and references. Adds a `\end{document}` at the end

    :param text: latex file content
    :return: blueprint of latex source file, ready to be written to output and edited and/or compiled in latex
    """
    sections = re.split(r'(\\section{.*})', text)
    header = sections[0].strip()
    result = [(0, header)]
    for e in get_figure(text):
        result.append((e.start(), e.group().strip()))
    for e in get_sections(text):
        result.append(e)
    result.sort()

    # extraction on a small part of the latex source restarts the regex matches position numbering.
    # this is a trick to make sure the bibliography lines are at the end of the document.
    fake_start = result[-1][0] + 1
    for e in get_references(sections[-1]):
        result.append((fake_start, e.group()))
        fake_start += 1
    return "\n\n".join(e[1] for e in result).strip() + "\n\n\end{document}\n"


def get_references(content):
    """ Extracts bibliography. Assumption : it's in the last element of `sections`

    :param content: last section of the extracted latex file
    :return: iterator containing each line matching \bilbio.*{.*}
    """
    return re.finditer(r'\\biblio.*{.*}', content)


def parser_main(dl_path):
    """ Finds tex source file. Parses its content. Overwrites source with blueprint.

    :param dl_path: PDF URL
    """
    files_list = [e for e in os.listdir(dl_path) if e.endswith(".tex")]
    latex_content, tex_src_name = None, None

    for name in files_list:
        content = open(os.path.join(dl_path, name), 'r').read()
        if "\\begin{document}" in content:
            latex_content = content
            tex_src_name = name

    if latex_content:
        global TEX_FILE_PATH
        TEX_FILE_PATH = os.path.join(dl_path, tex_src_name)
        extracted_content = get_all(latex_content)
        with open(TEX_FILE_PATH, 'w') as parsed_latex_output:
            parsed_latex_output.write(extracted_content)
    else:
        sys.exit("Cannot find .tex file in the specified folder: {}".format(dl_path))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Small latex parser, to extract skeleton of a latex file.")
    parser.add_argument("dl_path", type=str, help="Path to downloaded sources")
    args = parser.parse_args()
    parser_main(**vars(args))
