import re
import os
import sys


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
    return "\n\n".join(e[1] for e in result) + "\n\n\end{document}"


def main(dl_path):
    files_list = os.listdir(dl_path)
    tex = None
    for name in files_list:
        match = re.match(r'.*\.tex', name)
        if match:
            tex = name
    if tex:
        latex_content = open(os.path.join(dl_path, tex), 'r').read()
        new_filename = re.sub(r'\.tex', '_summary.tex', tex)
        extracted = get_all(latex_content)
        with open(os.path.join(dl_path, new_filename), 'w') as parsed_latex_output:
            parsed_latex_output.write(latex_content)
    else:
        sys.exit("Cannot find .tex file in the specified folder: {}".format(dl_path))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("dl_path", type=str, help="Path to downloaded sources")
    args = parser.parse_args()
    main(**vars(args))
