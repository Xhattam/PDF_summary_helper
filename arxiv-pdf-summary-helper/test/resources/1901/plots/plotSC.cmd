set ytics 75,0.1
set y2tics 45,5

set ylabel "Score"
set xtics rotate

set grid

pl[][] 'sentenceClassification.dat' u 1:xtic(2) w lp t "Best" axis x1y1 lw 3, "" i 2 u 3:xtic(2) w lp t "Avg" axis x1y2 lw 3 lc 3
 
 set terminal epslatex color lw 2 size 15cm,12cm "" 8
 set output "sent.tex"
 replot
 unset output
 