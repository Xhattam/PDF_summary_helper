### doc classification 
set ytics 94,0.5  
set y2tics 55,5   

set grid
set ylabel "Score"

pl[][] 'C:\Users\Steffen\Desktop\projects\ActFunc\scores_norm.dat' i 0 u 1:xtic(2) w lp t "Best" axis x1y1 lw 5, "" i 0 u 3:xtic(2) w lp t "Avg" axis x1y2 lw 5 lc 3

set terminal epslatex color lw 2 size 15cm,12cm "" 8
set output "doc.tex"
replot
unset output

### sent classification
set ytics 97,0.5
set y2tics 64,5
set xtics rotate

pl[][] 'C:\Users\Steffen\Desktop\projects\ActFunc\scores_norm.dat' i 1 u 1:xtic(2) w lp t "Best" axis x1y1 lw 5, "" i 1 u 3:xtic(2) w lp t "Avg" axis x1y2 lw 5 lc 3

set terminal epslatex color lw 2 size 15cm,12cm "" 8
set output "sent.tex"
replot
unset output

### seq tagging 
set ytics 74,3
set y2tics 30,10

pl[][] 'C:\Users\Steffen\Desktop\projects\ActFunc\scores_norm.dat' i 2 u 1:xtic(2) w lp t "Best" axis x1y1 lw 5, "" i 2 u 3:xtic(2) w lp t "Avg" axis x1y2 lw 5 lc 3

set terminal epslatex color lw 2 size 15cm,12cm "" 8
set output "seq.tex"
replot
unset output