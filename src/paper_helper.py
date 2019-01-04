from download_data import downloader_main, get_dest_path, get_pdf_path
from parse_latex import parser_main, get_summary_path
import subprocess


def paper_helper_main(pdf_url, dest, force_dl):
    downloader_main(pdf_url, dest, force_dl)
    dest_path = get_dest_path()
    parser_main(dest_path)
    subprocess.Popen(["evince", get_pdf_path()])
    subprocess.Popen(["subl", "-w", get_summary_path()]).wait()



if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("pdf_url", type=str, help="URL to PDF")
    parser.add_argument("dest", type=str, help="Destination folder")
    parser.add_argument("-force_dl", action="store_true", help="If file already exist, download again", default=False)

    args = parser.parse_args()
    paper_helper_main(**vars(args))

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