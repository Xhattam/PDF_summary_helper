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

    :return : latex source file absolute path
    :rtype  : str
    """
    return TEX_FILE_PATH


def get_sections(text):
    """ Finds all section and subsections names in the latex file

    :param text : content of the latex file
    :type text  : str
    :return     : list of section/subsection/paragraph/input names, in latex format: `\section{section name}`
    :rtype      : list of str
    """
    tmp = re.finditer(r"^\\(s(?:ubs){0,2}ection|paragraph|input){.*?}", text, re.MULTILINE)
    return [(e.start(), e.end(), e.group()) for e in tmp]


def get_figure(text):
    """ Extracts specific latex elements (currently, figure, itemize, equation, table and enumerate sections)

    :param text : content of the latex file
    :type text  : str
    :return     : list with all specific latex elements and their content
    :rtype      : str
    """
    patt = "|".join(["figure", "itemize", "equation", "table", "enumerate", "problem", "align", "layer1"])
    tmp = re.finditer(r'((?<!\\begin{comment})\s\\begin{(?P<sec>(?:' +
                       '{}'.format(patt) +
                       r')\*{0,1})}(?:.*?)\\end{(?P=sec)})', text, re.S)

    return [(e.start(), e.end(), e.group().strip()) for e in tmp]


def remove_comments(text):
    """ Removes inline and general comments (indicated with %), while keeping literal %

    Also removes training whitespaces
    :param text : latex file content
    :type text  : str
    :return     : content without comments
    :rtype      : str
    """
    no_comments = []
    lines = [l.rstrip(" ") for l in text.split("\n")]
    for line in lines:
        if not "%" in line:
            no_comments.append(line)
        else:
            if not line.startswith("%"):
                if line == '':
                    no_comments.append(line)
                else:
                    line = line.replace('\%', 'TMP_PERCENT')
                    line = re.sub(" *%.*", '', line)
                    line = line.replace('TMP_PERCENT', r'\%')
                    if line != "":
                        no_comments.append(line)

    return "\n".join(no_comments)


def get_appendix(text):
    """ Extracts the appendix header (no content)

    :param text : latex file content
    :type text  : str
    """
    tmp = re.finditer(r'(^\\appendix$)', text, re.M)
    return [(e.start(), e.end(), e.group()) for e in tmp]


def get_all(text):
    """ Creates blueprint of original latex src
    Calls all extraction functions. Gets header, content, and references. Adds a `\end{document}` at the end

    :param text : latex file content
    :type text  : str
    :return     : 'blueprint' of latex source file, ready to be written to output and edited and/or compiled in latex
    :rtype      : str
    """
    text = remove_comments(text)
    sections = re.split(r'(\\section{.*})', text)
    header = sections[0].strip()
    result = [(0, 1, header)]
    result += get_figure(text)
    result += get_sections(text)
    result += get_references(text)
    result += get_appendix(text)
    result.sort()
    result = remove_overlaps(result)

    return "\n\n".join(e[2] for e in result).strip() + "\n\n\end{document}\n"


def remove_overlaps(results):
    """ Some matched macros might contain references to other in the case of input, and created overlapping matches
    Ex : a \table section is matched, containing a references to another file with \input.
    Then, we search for \input sections. This \input will be matched twice
    Use the start/end of each match to remove overlapping elements

    :param results  : list of all parsed latex macros (ordered by regex match start index)
    :type results   : list of str
    :return         : list of parsed latex macros, with overlaps removed
    :rtype          : list of str
    """
    i = 0
    for e in results:
        j = i + 1
        while j < len(results):
            if not is_contained(results[j], e):
                i += 1
                break
            else:
                del results[i+1]
    return results


def is_contained(e1, e2):
    """ Checks if regex match e2 is contained (overlapping) in regex match e1
    ex :
        e1 = (0, 10, "cde abc ghf") and e2 = (4, 6, "abc")

    e2 is contained in e1 (shown in the start/end indices of the match)
    Each tuple is (match_start_index, match_end_index, string_matched)
    :param e1   : regex-matched element
    :type e1    : str
    :param e2   : regex-matched element
    :type e2    : str
    :return     : True if e2 is contained in e1
    :rtype      : bool
    """
    return e1[0] < e2[1] and e1[1] < e2[1]


def get_references(content):
    """ Extracts bibliography.

    :param content  : last section of the extracted latex file
    :type content   : str
    :return         : list containing each line matching \bilbio.*{.*}
    :rtype          : list of str
    """
    tmp = re.finditer(r'\\biblio.*{.*}', content)
    return [(e.start(), e.end(), e.group()) for e in tmp]


def parser_main(dl_path, ret=False):
    """ Finds tex source file. Parses its content. Overwrites source with blueprint.

    :param dl_path  : PDF URL
    :type dl_path   : str
    :param ret      : if true, returns extracted content (for tests)
    :type ret       : bool
    """
    files_list = [e for e in os.listdir(dl_path) if e.endswith(".tex")]

    latex_content, tex_src_name = None, None
    multiple_inputs = {}

    for name in files_list:
        content_fh = open(os.path.join(dl_path, name), 'r')
        content = content_fh.read()
        if "\\begin{document}" in content:
            latex_content = remove_comments(content)
            tex_src_name = name
        else:
            name_no_ext = name.rsplit(".", 1)[0]
            multiple_inputs[name_no_ext] = content
        content_fh.close()

    latex_content = concatenate_multiple_sources_into_one(multiple_inputs, latex_content)

    if latex_content:
        global TEX_FILE_PATH
        TEX_FILE_PATH = os.path.join(dl_path, tex_src_name)
        extracted_content = get_all(latex_content)
        if ret:
            return extracted_content
        with open(TEX_FILE_PATH, 'w') as parsed_latex_output:
            parsed_latex_output.write(extracted_content)
    else:
        sys.exit("Cannot find .tex file in the specified folder: {}".format(dl_path))


def concatenate_multiple_sources_into_one(multiple_inputs, main_tex):
    """ Inserts content of \input element into the main latex content
    Ex : if the content is:

        some text
        \input{other_file}

        some more text

    And the content of 'other_file' is 'abcd'

    The the result will be:

        some text
        abcd

        some more text

    :param multiple_inputs  : dictionary mapping an input name to its file content
    :type multiple_inputs   : dict(str)
    :param main_tex         : current content of the main latex file
    :type main_tex          : str
    :return                 : main latex file with references to inputs replaced by inputs contents
    :rtype                  : str
    """

    def replace_input_ref_by_content(m):
        """ Returns content for a given input name

        :param m    : (implicit) matched group, name in \input macro
        :type m     : match object
        :return     : content of file referenced by \input{filename}
        :rtype      : str
        """
        return multiple_inputs[m.groups()[0]]

    return re.sub(r'\\input{(.*?)}', replace_input_ref_by_content, main_tex)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Small latex parser, to extract skeleton of a latex file.")
    parser.add_argument("dl_path", type=str, help="Path to downloaded sources")
    args = parser.parse_args()
    parser_main(**vars(args))
