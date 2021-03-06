#!/gnuplot

nuclide = 'u235'
nuclide_title = '{}^{235}U'

set title "N time dependence"
set key left top
set xlabel "t, c"
set term png linewidth 2
set output "../output/".nuclide."_number_time_dependence.png"
set logscale x
#set format y "10^{%L}"

plot '../output/'.nuclide.'/'.nuclide.'_neutrino_number.dat' using 1:2 title "u235" with lines
