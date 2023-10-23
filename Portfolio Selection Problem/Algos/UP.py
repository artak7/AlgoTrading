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

# универсальный портфельный алгоритм
def UP(B): # B - эксперты
	sum = 0
	bt1 = [0] * m1 # результирущий массив
	# ищем распределение эксперта, с максимальным доходом
	for w in range(1,Bn1): 
		sum += W_T(B[w])

	for i in range(1,m1):
		wsum = 0
		for w in range(1,Bn1):
			wsum += B[w][i] * W_T(B[w])

		bt1[i] = wsum / sum
	
	return bt1

