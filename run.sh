source env/bin/activate;
$arg
space=" "
for i in $@
do
  arg=$arg$space$i
done
$arg
