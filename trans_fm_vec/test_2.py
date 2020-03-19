import sys


for line in sys.stdin:
    arr = line.strip().split(' ')
    print (arr[0] + "\t" + str(len(arr[0])))
