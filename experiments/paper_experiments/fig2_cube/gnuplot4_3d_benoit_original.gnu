set terminal pngcairo font "Arial,16" size 1024,728 # Use a larger font size,
#set terminal pdf
set output 'outall2.png'
set pointsize 0.3
set xrange [0:1]
set yrange [0:1]
set zrange [0:1]
set style fill transparent solid 0.2 noborder
#set style circle radius 0.

set xtics offset 0.2,-0.3   # Adjust x-axis tics
set ytics offset 0.4,-0.3   # Adjust y-axis tics
set ztics offset 0.5,0.0   # Adjust z-axis tics

set xtics 0.2, 0.2, 1

set view equal xyz
set view 80,66
#set view 90,45
set ticslevel 0  # Moves the axis to the bottom
set key off
splot 'cube.txt' u 1:2:3:(1) w l ls 6 notitle,\
	'out05.dat' w p lc 1 pt 7 title "T=0.5",\
	'out10.dat' w p lc 2 pt 7 title "T=1.0",\
	'out15.dat' w p lc 3 pt 7 title "T=1.5",\
	'out20.dat' w p lc 4 pt 7 title "T=2.0",\
	'out25.dat' w p lc 5 pt 7 title "T=2.5"
	
#splot 'cube.txt' u 1:2:3:(1) w l ls 6 notitle,\
#	'out4_20.dat' w p lc 3 pt 7 title "T=1.5"
