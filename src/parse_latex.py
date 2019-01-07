import re
import os
import sys


SUMMARY_PATH = ""

def get_sections(text):
    return re.finditer(r"\\(?:sub)*section{.*}", text)


def get_figure(text):
    return re.finditer(r'((?<!\\begin{comment})\s\\begin{(?P<sec>(?:figure\*{0,1}|itemize|equation|table|enumerate))}(?:.*?)\\end{(?P=sec)})', text, re.S)


def get_all(text):
    sections = re.split(r'(\\section{.*})', text)
    header = sections[0]
    extract_bibliography(sections[-1])
    result = [(0, header)]
    for e in get_figure(text):
        result.append((e.start(), e.group()))
    for e in get_sections(text):
        result.append((e.start(), e.group()))
    for e in get_references(sections[-1]):
        result.append((e.start(), e.group()))
    result.sort()
    return "\n\n".join(e[1] for e in result) + "\n\n\end{document}"


def get_summary_path():
    return SUMMARY_PATH


def get_references(content):
    return re.finditer(r'\\biblio.*{.*}', content)


def parser_main(dl_path):
    files_list = [e for e in os.listdir(dl_path) if e.endswith(".tex") and not e.endswith("_summary.tex")]
    latex_content, summary_filename = None, None

    for name in files_list:
        content = open(os.path.join(dl_path, name), 'r').read()
        if "\\begin{document}" in content:
            latex_content = content
            summary_filename = re.sub(r'\.tex', '_summary.tex', name)

    if latex_content:
        extracted_content = get_all(latex_content)
        summary_path = os.path.join(dl_path, summary_filename)
        global SUMMARY_PATH
        SUMMARY_PATH = summary_path
        with open(summary_path, 'w') as parsed_latex_output:
            parsed_latex_output.write(extracted_content)
    else:
        sys.exit("Cannot find .tex file in the specified folder: {}".format(dl_path))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("dl_path", type=str, help="Path to downloaded sources")
    args = parser.parse_args()
    parser_main(**vars(args))
