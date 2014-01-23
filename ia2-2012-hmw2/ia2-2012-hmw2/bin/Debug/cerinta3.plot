set terminal png
set output  "cerinta3.png"
#set title "Energy vs. Time for Sample Data"
#set xlabel "Time"
#set ylabel "Energy"
plot "cerinta3.dat" using 1:2 smooth csplines
