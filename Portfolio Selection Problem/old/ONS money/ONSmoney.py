import numpy
import csv 

m = 2
m1 = m + 1
T = 152
money = ['', 'EUR', 'USD']
q = [] # price # num from 0
date = [] # num from 0

for i in range(1,m):
	file = open(str(i)+".csv", "r")	
	for line in file:
		init = line.split(';')
		date.append(init[0])
		q.append(init[1])





b = [[0] * T] * m1
t = 0	
for i in range(1,m1):
	b[t][i] = 1 / m

teta1 = [[0] * m1] * T
teta2 = [[[0] * m1] * m1] * T
a = [[[0] * m1] * m1] * T
o1 = [[0] * m1] * T
o2 = [[0] * m1] * T

for t in range(T+1):
	x_t = 0
	for i in range(1,m1):
		x_t += x[t][i] * b[t][i]

	x_t_2 = x_t * x_t
	
	for i in range(1,m1):
		teta1[t][i] = x[t][i] / x_t
	
	for i in range(1, m1):
		for j in range(1, m1):
			teta2[t][i][j] = -x[t][i] * x[t][j] / x_t_2

	for i in range(1, m1):
		for j in range(1, m1):
			if t == 0:
				a[t][i][j] = 1
			else:
				a[t][i][j] = a[t - 1][i][j] - teta[t][i][j]

	for i in range(1,m1):
		if t == 0:
			o1[t][i] = (1 + 1 / Beta) * teta1[t][i] + o1[t-1][i]
		else:
			o1[t][i] = 0

	# ainv = inverse(a)
	ainv = linalg.inv(a[t])

	for i in range(1, m1):
		sumj = 0
		for j in range(1, m1):
			sumj += ainv[t][i][j] * o1[t][j]

		o2[t][i] = Delta * sumj