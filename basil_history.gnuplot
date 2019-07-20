set terminal png size 600,400 enhanced
set output '/dev/stdout'
set xdata time
set timefmt '%Y-%m-%d %H:%M:%S'
set format x "%d/%m\n%H:%M"
set datafile separator ','
set ylabel '% Moisture Content'
# set xtics rotate
plot '< cat -' using 1:2 notitle w points
