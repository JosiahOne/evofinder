import sys


def main():
  line1 = sys.stdin.readline()
  line2 = sys.stdin.readline()

  if int(line1) < 10:
    print("Some usual thing")
  else:
    print("Some other (interesting) thing?")


main()
