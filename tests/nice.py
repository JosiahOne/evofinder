import sys

def foo():
  print("Do something")


if len(sys.stdin.readline()) < 15:
  size = 0
  if len(sys.stdin.readline()) < 10:
    size = 10
  else:
    size = 5

  for i in range(size):
    if i == 8:
      print("Got to 8")
    else:
      print(i)
else:
  foo()
