import numpy
import csv 
import random

# инициализация
m = 5 # количство активов
m1 = m + 1
T = 104 # количество  временных периодов
T1 = T + 1 
actives = ['', 'AAPL', 'MSFT', 'MCD', 'YNDX', 'TSM'] # некоторый набор активов
q = [[0] * T] * m1  # стоимость акции # num from 0
date = [[''] * T] * m1 # дата транзакции # num from 0
x = [[0] * T] * m1 # коэффициент доходности # num from 1

Bn = 100 # количество экспертов
Bn1 = Bn + 1
B = [[0] * m1] * Bn1 # эксперты # num from 1

# генерируем Bn случайных экспертов
# доли должны находиться в диапазоне от 0 до 1
for i in range(1,Bn1):
	rest = 1
	for j in range(1,m1):
		B[i][j] = random.uniform(0, rest) 
		diff = rest - B[i][j]
		if diff >= 0:
			rest -= B[i][j]

b = [[0] * m1] * T # распределение долей активов
j = 0
for i in range(1,m1):
	b[j][i] = 1 / m    # на начальном шаге распределение - наивная диверсификация


# считываем и обработаываем данные об активах
for i in range(1,m1):
	file = open(str(i)+".csv", "r")
	j = -1
	for line in file:
		if j >= 0:
			datei, qi = line.split(';')
			date[i][j] = datei
			q[i][j] = float(qi)
		if j > 0:
			x[i][j] = q[i][j] / q[i][j-1]
		j += 1

# функция подсчета дохода от эксперта b
def W_T(b):
	for t in range(T):
		sum = 0
		for i in range(m1):
			sum += x[i][t] * b[i][t]

		prod += sum

	result = W_0 * prod

def ONS(t):
	Beta = 1
	Delta = 1

	a = [[[0] * m1] * m1] * T 
	o1 = [[0] * m1] * T
	o2 = [[0] * m1] * T
	
	# информация первого и второго порядков
	# информация первого порядка 
	# увеличение / уменьшение дохода за период
	x_t = 0 
	for i in range(1,m1):
		x_t += x[i][t] * b[t][i]

	x_t_2 = x_t * x_t 
	
	teta1 = [[0] * m1] * T # информация первого порядка
	teta2 = [[[0] * m1] * m1] * T # информация второго порядка

	# информация первого порядка
	# изменение цены i-го актива по отношению к доходу за период 
	for i in range(1,m1):
		teta1[t][i] = x[i][t] / x_t 
	
	# информация второго порядка 
	# изменение цен i-го и j-го активов по отношению к доходу за период в квадрате 
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

	for t1 in range(1,Bn1):
		for i in range(1, m1):
			sum1 += a[t][i][i] * (o[t][i] - B[t1][i])

		for i in range(1, m):
			for j in range(i+1, m1):
				sum2 += a[t][i][j] * (o[t][i] - B[t1][i]) * (o[t][j] - B[t1][j])

		newb = sum1 + 2 * sum2
		if minb == -1 or newb < minb:
			minb = newb
			mint = t1

	return B[mint]