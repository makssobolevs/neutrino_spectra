#!/gnuplot

nuclide = 'u235'
nuclide_title = '{}^{235}U'

set term png linewidth 2
set output nuclide.".png"
set title nuclide_title
set xrange [1:12]
#set logscale y
#set format y "10^{%L}"
times = "CFY 1s 1minute 1hour 24hours 1week 1year"

plot for [t in times] '../plots/u235time'.t.'_gamma.dat' using 1:2 title t with lines
