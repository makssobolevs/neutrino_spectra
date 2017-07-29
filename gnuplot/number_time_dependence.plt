#!/gnuplot

nuclide = 'u235'
nuclide_title = '{}^{235}U'

set title "N time dependence"
set key left top
set xlabel "t, c"
set term png linewidth 2
set output "number_time_dependence.png"
set logscale x
#set format y "10^{%L}"
nuclides = "u235"

plot '../plots/u235_neutrino_number.dat' using 1:2 title "u235" with lines
