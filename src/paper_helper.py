from tex2py import tex2py
import re

def run(tex_file):
    with open(tex_file) as tex:
        data = tex.read()
        section_names = find_sections(data)
        beginning = extract_beginning(data)


def find_sections(data):
    sections = re.findall(r"\\s*u*b*section{.*}|\\paragraph", data)
    return sections


def extract_beginning(data):
    d = re.findall(r'(.*?)\\section{Introduction}', data, re.S)
    return d[0]

def extract_other(data, patt="figure"):
    d = re.findall(r'(\\begin{%s}.*?\\end{%s}'.format(patt))


'''
1. Download src when available in latex (will contain .tex file and other files referenced in the tex source)
    - name.tex : tex source
    - name.bst : bibliography style file, references in name.tex WITHOUT the extension
    - name.bbl : bibliography, NOT mentioned in the main,tex file, passed to latex at compilation (??)
    - image files (extension varies), mentioned in the main.tex
    - other ??
    
2. Copy the folder content, and start reading the main.tex file. Should extract:
    - everything from the beginning to the end of the abstract 
    - all section/subsections/paragraph names
    - all images sections (should include a ref to an image in the source folder)
    - all formulas/tables... (any data that cannot explicitely be summarised)
    
    
    Process for extraction:
        - Extract everything until \end{abstract} is found. Add it to summary file
        - Split the original text on \section and \(sub)*section and paragraph, respecting order
        - For each section type, copy potential image/table, etc sections
        - Copy the Bibliography section
        
    Write the extracted content to a new .tex file, in the same source folder
    
3. Once the new tex file has been created, execute a latex2pdf command on it, make sure it doesn't fail, or fix issues 
manually

4. Once the compilation is successful, run a command to open the original PDF, or a latex viewer online ? and open the 
new .tex file in sublime for editing.


'''