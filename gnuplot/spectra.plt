#!/gnuplot

set term png linewidth 2
set xrange [1:12]
#set logscale y
#set format y "10^{%L}"

times = "CFY 1s 1minute 1hour 24hours 1week 1year"

nuclide = 'u235'
nuclide_title = '{}^{235}U'
set output "../output/".nuclide.".png"
set title nuclide_title

plot for [t in times] '../output/'.nuclide.'/'.nuclide.'time'.t.'_gamma.dat' using 1:2 title t with lines


nuclide = 'pu239'
nuclide_title = '{}^{239}Pu'
set output "../output/".nuclide.".png"
set title nuclide_title

plot for [t in times] '../output/'.nuclide.'/'.nuclide.'time'.t.'_gamma.dat' using 1:2 title t with lines


nuclide = 'u238'
nuclide_title = '{}^{238}U'
set output "../output/".nuclide.".png"
set title nuclide_title

plot for [t in times] '../output/'.nuclide.'/'.nuclide.'time'.t.'_gamma.dat' using 1:2 title t with lines


nuclide = 'pu241'
nuclide_title = '{}^{241}Pu'
set output "../output/".nuclide.".png"
set title nuclide_title

plot for [t in times] '../output/'.nuclide.'/'.nuclide.'time'.t.'_gamma.dat' using 1:2 title t with lines
