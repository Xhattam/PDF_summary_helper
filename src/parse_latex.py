import re
import os
import sys

TEX_FILE_PATH = ""


def get_tex_path():
    return TEX_FILE_PATH


def get_sections(text):
    return re.finditer(r"\\(?:sub)*section{.*}", text)


def get_figure(text):
    return re.finditer(r'((?<!\\begin{comment})\s\\begin{(?P<sec>(?:figure\*{0,1}|itemize|equation|table|enumerate))}(?:.*?)\\end{(?P=sec)})', text, re.S)


def get_all(text):
    sections = re.split(r'(\\section{.*})', text)
    header = sections[0]
    result = [(0, header)]
    for e in get_figure(text):
        result.append((e.start(), e.group()))
    for e in get_sections(text):
        result.append((e.start(), e.group()))
    result.sort()
    fake_start = result[-1][0] + 1
    for e in get_references(sections[-1]):
        result.append((fake_start, e.group()))
        fake_start += 1
    return "\n\n".join(e[1] for e in result) + "\n\n\end{document}"


def get_references(content):
    """ Extracts bibliography. Assumption : it's in the last element of `sections`

    :param content: last section of the extracted latex file
    :return: iterator containing each line matching \bilbio.*{.*}
    """
    return re.finditer(r'\\biblio.*{.*}', content)


def parser_main(dl_path):
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

    parser = argparse.ArgumentParser()
    parser.add_argument("dl_path", type=str, help="Path to downloaded sources")
    args = parser.parse_args()
    parser_main(**vars(args))
