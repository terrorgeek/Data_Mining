M=int(raw_input())
lineM=map(int,raw_input().split(" "))
N=int(raw_input())
lineN=map(int,raw_input().split(" "))
lineM=set(lineM)
lineN=set(lineN)
a=lineM.difference(lineN)
b=lineN.difference(lineM)
c=a|b
c=list(c)
c.sort()
for i in c:
    print i