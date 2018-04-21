function setup_err(){
  echo "Need to run setup.sh"
  exit 1
}
# calls setup_err() if the virtual env can't be activated
source env/bin/activate || setup_err
if [ "$#" -lt "1" ] ; then
  echo "Usage: ./run.sh <shell_commands>"
  exit 1
fi
$arg
space=" "
for i in $@
do
  arg=$arg$space$i
done
$arg
