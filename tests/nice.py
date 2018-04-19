import sys

def foo():
  print("Do something")


if len(sys.stdin.readline()) < 15:
  size = 0
  if len(sys.stdin.readline()) > 20:
    size = 20
  else:
    size = 5

  for i in range(size):
    if i == 18:
      print("Got to 18")
    else:
      print(i)
else:
  foo()
