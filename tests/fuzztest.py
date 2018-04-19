import sys
def opOne(a,b):
    if a-b > 0:
        t = b*b
    else:
        t = a+b
    return t
def opTwo(c,x):
    for i in range(len(c)):
        if len(x) > i:
            if len(x)/(i+1) < 3:
                c[i]="0"
            else:
                c[i]="1"
        else:
            if i/(len(x)+1) < 3:
                c[i]="1"
            else:
                c[i]="0"
    return c
def main():
    x = input()
    try:
        if int(x) > 23:
            y = int(x) + 1
            size = 0
            for i in range(y):
                size += opOne(i,y)
            print(float(x))
        elif int(x) <= 23:
            y = opOne(int(x),int(x))
            size = y + 2

    except (ValueError):
        if len(x)<5:
            x = x.upper()
            size = 5
        else:
            size = 15

    A = [x for j in range(size)]
    print(opTwo(A,x))
    score = 0
    for j in  opTwo(A,x):
        if j == "1":
            score += 1

    print("score: ", score)

    return
main()

