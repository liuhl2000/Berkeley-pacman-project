import random
a = random.choices([1,2,3], [1,1,1], k=1)
b = {'a': 1, 'b':2}
b['c'] += 1
print(b['c'])
print(a)