A = [43,23,1,0,15,31,4,7,11,3]
B = [0,1,2,3,4,5,6,7,8,9]
i = 1
while(1):
    temp = []
    for value in A:
        mod = ((11*value + 4)%i)%10
        temp.append(mod)
    temp.sort()
    if temp == B:
        break
    i += 1

print(i)
