set terminal png size 400,300 enhanced
set output '/dev/stdout'
set xdata time
set timefmt '%Y-%m-%d %H:%M:%S'
set datafile separator ','
set xtics rotate
plot '< cat -' using 1:2 notitle smooth csplines
