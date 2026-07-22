# 3D slices of the hypercube language (Figure 2, top left).
# Parametrized version of gnuplot4_3d_benoit_original.gnu.
# Call: gnuplot -e "datadir='DIR'; cubefile='DIR/cube.txt'; outfile='OUT.png'" cube_3d.gnu
set terminal pngcairo font "Arial,16" size 1024,728
set output outfile
set pointsize 0.3
set xrange [0:1]
set yrange [0:1]
set zrange [0:1]
set style fill transparent solid 0.2 noborder

set xtics offset 0.2,-0.3
set ytics offset 0.4,-0.3
set ztics offset 0.5,0.0
set xtics 0.2, 0.2, 1

set view equal xyz
set view 80,66
set ticslevel 0
set key off
splot cubefile u 1:2:3:(1) w l ls 6 notitle,\
	datadir.'/out05.dat' w p lc 1 pt 7 title "T=0.5",\
	datadir.'/out10.dat' w p lc 2 pt 7 title "T=1.0",\
	datadir.'/out15.dat' w p lc 3 pt 7 title "T=1.5",\
	datadir.'/out20.dat' w p lc 4 pt 7 title "T=2.0",\
	datadir.'/out25.dat' w p lc 5 pt 7 title "T=2.5"
