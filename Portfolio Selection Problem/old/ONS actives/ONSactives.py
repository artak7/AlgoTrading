import numpy
import csv 
import random

Beta = 1
Delta = 1
m = 5
m1 = m + 1
T = 104
T1 = T + 1 
actives = ['', 'AAPL', 'MSFT', 'MCD', 'YNDX', 'TSM']
q = [[0] * T] * m1  # price # num from 0
date = [[''] * T] * m1 # num from 0
x = [[0] * T] * m1 # num from 1

for i in range(1,m1):
	file = open(str(i)+".csv", "r")	
	j = 0
	for line in file:
		datei, qi = line.split(';')
		date[i][j] = datei
		q[i][j] = int(qi)
		if j > 0:
			x[i][j] = q[i][j] / q[i][j-1]
		j += 1

b = [[0] * m1] * T
j = 0	
for i in range(1,m1):
	b[j][i] = 1 / m

teta1 = [[0] * m1] * T
teta2 = [[[0] * m1] * m1] * T
a = [[[0] * m1] * m1] * T
o1 = [[0] * m1] * T
o2 = [[0] * m1] * T

for t in range(1,T1):
	x_t = 0 # информация первого порядка # увеличение / уменьшение дохода за период
	for i in range(1,m1):
		x_t += x[i][t] * b[t][i]

	x_t_2 = x_t * x_t # информация второго порядка
	
	for i in range(1,m1):
		teta1[t][i] = x[i][t] / x_t
	
	for i in range(1, m1):
		for j in range(1, m1):
			teta2[t][i][j] = -x[i][t] * x[j][t] / x_t_2

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

	ainv = linalg.inv(a[t])
	minb = -1

	for i in range(1, m1):
		sumj = 0
		for j in range(1, m1):
			sumj += ainv[t][i][j] * o1[t][j]

		o2[t][i] = Delta * sumj

	for t1 in range(1,Tbg)
		for i in range(1, m1):
			sum1 += a[t][i][i] * (o[t][i] - bg[t1][i])

		for i in range(1, m):
			for j in range(i+1, m1):
				sum2 += a[t][i][j] * (o[t][i] - bg[t1][i]) * (o[t][j] - bg[t1][j])

		newb = sum1 + 2 * sum2
		if (minb == -1 || newb < minb)
			minb = newb
			mint = t1 


bg from projection 4.1