#!/bin/bash

INFILE=$1
VIEWPG=$2
echo $INFILE

#set DVIFILE='echo $INFILE:t | sed s:.tex:."$DVIEXT":g'
BIBFILE=`echo $INFILE | sed 's/\(.*\)\.tex/\1/'`
DVIFILE=`echo $INFILE | sed 's/\(.*\)\.tex/\1\.dvi/'`
PDFFILE=`echo $INFILE | sed 's/\(.*\)\.tex/\1\.pdf/'`
PSFILE=`echo $INFILE | sed 's/\(.*\)\.tex/\1\.ps/'`
LOGFILE=`echo $INFILE | sed 's/\(.*\)\.tex/\1\.log/'`
BIBLOGFILE=`echo $INFILE | sed 's/\(.*\)\.tex/\1\.blg/'`
AUXFILE=`echo $INFILE | sed 's/\(.*\)\.tex/\1\.aux/'`

#					  i/p				o/p 	
latex $INFILE		# tex				aux
bibtex $BIBFILE		# aux, bib, bst		blg, bbl
latex $INFILE		# tex, aux, bbl		aux
latex $INFILE		# tex, aux			dvi
echo
echo
echo "Generating dvi->ps->pdf file for $DVIFILE ... "
dvips  $DVIFILE
ps2pdf $PSFILE
#dvipdf $DVIFILE 

# do not delete aux and bbl files. Otherwise you'll get 
# errors like: "LaTeX Warning: Citation `Lamp86' on page 2 undefined on input line 165."
rm $LOGFILE $PSFILE $DVIFILE $BIBLOGFILE
echo "Opening page $VIEWPG in pdf file $PDFFILE using evince ... "
evince --page-label=$VIEWPG   $PDFFILE &

#gv $PDFFILE & # <- This opens the dvi file even though pdf file is given as
#input

#xdvi $DVIFILE
exit 0
