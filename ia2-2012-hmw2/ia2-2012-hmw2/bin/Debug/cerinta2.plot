set terminal png
set output  "cerinta2.png"
#set title "Energy vs. Time for Sample Data"
#set xlabel "Time"
#set ylabel "Energy"
plot "cerinta2.dat" using 1:2 smooth csplines
