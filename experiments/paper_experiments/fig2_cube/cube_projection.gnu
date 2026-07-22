# Projection of the T=1.5 slice on the delays (t1, t2) (Figure 2, top right).
# Call: gnuplot -e "datadir='DIR'; outfile='OUT.png'" cube_projection.gnu
set terminal pngcairo font "Arial,16" size 728,728
set output outfile
set size square
set xrange [0:1]
set yrange [0:1]
set xtics 0, 0.5, 1
set ytics 0, 0.5, 1
set xlabel "t_1"
set ylabel "t_2"
set key off
plot datadir.'/out15.dat' u 1:2 w p lc 3 pt 7 ps 0.3 notitle
