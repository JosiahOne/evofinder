function setup_err(){
  echo "Need to run setup.sh"
  exit 1
}
source env/bin/activate || setup_err
if [ "$#" -lt "2" ] ; then
  echo "Usage: ./run.sh python3 evofinder.py <input python file> <target_line_num> <example_file_1> <example_file_2> ..."
  exit 1
elif [ ! $1  = "python3" ] || [ ! $2 = "evofinder.py" ] ; then 
  echo "Usage: ./run.sh python3 evofinder.py <input python file> <target_line_num> <example_file_1> <example_file_2> ..."
  exit 1
fi
$arg
space=" "
for i in $@
do
  arg=$arg$space$i
done
$arg
