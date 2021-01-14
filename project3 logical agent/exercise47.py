'''import numpy as np
from scipy import stats
n = 10
wait_list = []
for m in range(1, n + 1):
    if stats.binom.cdf(m, n, 0.5) - stats.binom.cdf(n - m - 1, n, 0.5) > 0.95:
        wait_list.append(m)
print(min(wait_list))'''

mod = 2181271
p = 3881
result  = []
for i in range(1,27):
    result.append(pow(p,i) % mod)

print(result)
int weight[26] = {3881, 1974535, 365312, 2130993, 1185472, 516293, \
    1326355, 1965466, 68859, 1126717, 1521593, 601836, 1765546, 711815, 1064929, 1662175,\
    882828, 1659998, 1158975, 201173, 2038666, 592829, 1709715, 2158804, 56413, 811753]
'''import numpy as np
a = np.array([[-0.13,0.29], [-0.55,-1.72], [-1.23, 0.79], [-0.37, -0.48]])
b = a.transpose()
c = np.matmul(b,a)
d = np.array([-0.22, 0.78, -0.74, 0.23]).transpose()
e = np.matmul(b,d)
r = np.linalg.solve(c, e)

#print(c)
#print(e)
#print(r)

x = np.array([3,2,-1])
y = np.array([0,2,-3])
z = np.array([2,6,7])

result1 = np.cross(np.cross(x,y), np.cross(y,z))
result2 = np.cross(x, y - 2*z)

print(result1)
print(result2)'''

