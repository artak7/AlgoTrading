import numpy
import csv 

# Beta = 0
# Delta = 0
# m = input()

m = 3
m1 = m + 1
usdrubfile = open("USDRUB_180101_190101.csv", "r")
eurrubfile = open("EURRUB_180101_190101.csv", "r")

for line in usdrubfile:
	init = line.split(';')
	ER_date.append(init[2])
	ER_time.append(init[3])
	ER_open.append(init[4])
	ER_hi.append(init[5])
	ER_lo.append(init[6])
	ER_close.append(init[7])

x = [[0] * T] * m1
# read x_it

# T = ?
T = 2

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