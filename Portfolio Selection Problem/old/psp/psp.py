import random
import math
import numpy.linalg
import scipy.linalg as spla
import matplotlib.pyplot as plt
import pandas as pd
import csv

# инициализация
m = 5  # количство активов
m1 = m + 1
T = 104  # количество  временных периодов
T1 = T + 1
actives = ['', 'AAPL', 'MSFT', 'MCD', 'YNDX', 'TSM', 'US1', 'ASIX', 'ATGE', 'ATVI', 'ADBE']  # некоторый набор активов
# q = [[0] * T] * m1
q = [[0] * T for i in range(m1)]  # стоимость акции # num from 0
# date = [[''] * T] * m1
date = [[''] * T for i in range(m1)]  # дата транзакции # num from 0
# x = [[0] * T] * m1
x = [[0] * T1 for i in range(m1)]  # коэффициент доходности # num from 1
WSCR = [0] * T1
WUP = [0] * T1
WEG = [0] * T1
WONS = [0] * T1
bscr = [0] * T1
bup = [0] * T1
beg = [0] * T1
bons = [0] * T1

Bn = 100  # количество экспертов
Bn1 = Bn + 1
# B = [[[0] * m1] * T1]  * Bn1
B = [[[0] * m1 for i in range(T1)] for j in range(Bn1)]  # эксперты # num from 1

# генерируем Bn случайных экспертов
# доли должны находиться в диапазоне от 0 до 1
for i in range(1, Bn1):
    for t in range(1, T1):
        rest = 1
        for j in range(1, m):
            tmp = random.uniform(0, rest)
            B[i][t][j] = tmp
            diff = rest - B[i][t][j]
            if diff >= 0:
                rest = diff

        B[i][t][m] = rest

b = [[0] * m1] * T1  # распределение долей активов
j = 1
for i in range(1, m1):
    b[j][i] = 1 / m  # на начальном шаге распределение - наивная диверсификация

# считываем и обработаываем данные об активах
for i in range(1, m1):
    file = open(str(i) + ".csv", "r")
    j = -1
    for line in file:
        if j >= 0:
            datei, qi = line.split(';')
            date[i][j] = datei
            q[i][j] = float(qi)
        if j > 0:
            x[i][j] = q[i][j] / q[i][j - 1]
        j += 1

# функция подсчета дохода от эксперта b
def W_T(b, t):
    prod = 1
    W_0 = 1  # для простоты положим W_0 = 1
    for t1 in range(1, t):
        sum = 0
        for i in range(1, m1):
            sum += x[i][t] * b[t][i]
        prod *= sum

    result = W_0 * prod
    return result


# последовательный константный ребалансируемый алгоритм
def SCR(B, t):  # B - эксперты
    wBest = 1
    WBest = 0

    # ищем распределение эксперта, с максимальным доходом
    for w in range(1, Bn1):
        Wcurr = W_T(B[w], t)
        if Wcurr > WBest:
            wBest = w
            WBest = Wcurr

    bt1 = B[wBest][t]
    return bt1


# универсальный портфельный алгоритм
def UP(B, t):  # B - эксперты
    sum = 0
    bt1 = [0] * m1  # результирущий массив
    # ищем распределение эксперта, с максимальным доходом
    for w in range(1, Bn1):
        sum += W_T(B[w], t)

    for i in range(1, m1):
        wsum = 0
        for w in range(1, Bn1):
            wsum += B[w][t][i] * W_T(B[w], t)

        bt1[i] = wsum / sum

    return bt1


# информация первого порядка
def X_T(b, t):
    x_t = 0  # увеличение / уменьшение дохода за период
    for i in range(1, m1):
        x_t += x[i][t] * b[i]

    return x_t


# алгоритм экспоненциального градиента
def EG(bt, t):
    Eta = 1  # константа, влияющая на увеличение долей
    sum = 0
    isum = [0] * m1  # доля дохода от iго актива
    bt1 = [0] * m1  # результирущий массив
    x_t = X_T(bt, t)
    for i in range(1, m1):
        isum[i] = math.exp((Eta * x[i][t]) / x_t)
        sum += isum[i]

    for i in range(m1):
        bt1[i] = isum[i] / sum

    return bt1


def ONS(t):
    Beta = 1
    Delta = 1

    a = [[[0] * m] * m] * T
    o1 = [[0] * m1] * T
    o2 = [[0] * m1] * T

    # информация первого и второго порядков
    # информация первого порядка
    # увеличение / уменьшение дохода за период
    x_t = 0
    for i in range(1, m1):
        x_t += x[i][t] * b[t-1][i]

    x_t_2 = x_t * x_t

    teta1 = [[0] * m1] * T  # информация первого порядка
    teta2 = [[[0] * m1] * m1] * T  # информация второго порядка

    # информация первого порядка
    # изменение цены i-го актива по отношению к доходу за период
    for i in range(1, m1):
        teta1[t][i] = x[i][t] / x_t

    # информация второго порядка
    # изменение цен i-го и j-го активов по отношению к доходу за период в квадрате
    for i in range(1, m1):
        for j in range(1, m1):
            teta2[t][i][j] = -x[i][t] * x[j][t] / x_t_2

    for i in range(1, m1):
        for j in range(1, m1):
            if t == 0:
                a[t][i-1][j-1] = 1
            else:
                a[t][i-1][j-1] = a[t - 1][i-1][j-1] - teta2[t][i][j]

    for i in range(1, m1):
        if t == 0:
            o1[t][i] = (1 + 1 / Beta) * teta1[t][i] + o1[t - 1][i]
        else:
            o1[t][i] = 0

    # numpy.set_printoptions(precision=17)
    anp = numpy.array(a[t])
    P, L, U = spla.lu(anp.T.dot(anp))
    #spla.solve(anp.T.dot(anp), numpy.eye(5))
    #ainv = numpy.linalg.inv(anp)
    minb = -1
    ainv = U
    # print(ainv)

    for i in range(1, m1):
        sumj = 0
        for j in range(1, m1):
            sumj += ainv[i-1][j-1] * o1[t][j]

        o2[t][i] = Delta * sumj

    for t1 in range(1, Bn1):
        minb = -1
        sum1 = 0
        for i in range(1, m1):
            sum1 += a[t][i-1][i-1] * (o2[t][i] - B[t1][i])

        sum2 = 0
        for i in range(1, m):
            for j in range(i + 1, m1):
                sum2 += a[t][i-1][j-1] * (o2[t][i] - B[t1][i]) * (o2[t][j] - B[t1][j])

        newb = sum1 + 2 * sum2
        if minb == -1 or newb < minb:
            minb = newb
            mint = t1

    return B[mint][t]

beg[0] = b[0]
for t in range(1, T):
    bscr[t] = SCR(B, t)
    WSCR[t] = W_T(bscr, t)
    # for i in range(1, m1):
    # 	print(bscr[t][i], end=" ")

    # print()

    bup[t] = UP(B, t)
    WUP[t] = W_T(bup, t)
    # for i in range(1, m1):
    # 	print(bup[t][i], end=" ")
    # print()

    beg[t] = EG(beg[t-1], t)
    WEG[t] = W_T(beg, t)
    # for i in range(1, m1):
    # 	print(beg[t][i], end=" ")
    # print()

    bons[t] = ONS(t)
    WONS[t] = W_T(bons, t)
#    for i in range(1, m1):
# 	    print(bons[t][i], end=" ")
#    print()

print(WSCR[T - 1], WUP[T - 1], WEG[T - 1], WONS[T - 1])



# анализ

# BH
xtrans = [[0] * m1 for i in range(T1)]
for i in range(T1):
    for j in range(m1):
        xtrans[i][j] = x[j][i]

# APY от BH на каждом активе

APYbh = [0] * m1
for i in range(m1):
    xtrans[0][i] = 1 # для простоты
for i in range(1,m1):
    APYbh[i] = (xtrans[T-1][i] / xtrans[0][i])**2-1 # годовая процентная прибыль

ASTDVbh = [0] * m1
for i in range(1,m1):
    sum = 0
    mubh = math.log(xtrans[T - 1][i] / xtrans[0][i]) / T
    for t in range(1, T):
	    x_t = xtrans[t][i]
	    sum += math.log(x_t - mubh)**2
    sigmabh = sum / T # стандартное отклонение
    ASTDVbh[i] = sigmabh * math.sqrt(T) # годовое стандартное отклонение

fig, ax = plt.subplots(figsize=(12, 6))
ax.scatter(x=APYbh, y=ASTDVbh, marker='o', c='w', edgecolor='b')
ax.set_title('отношение APY и ASTDV от BH на каждом активе')
ax.set_xlabel('$APY$')
ax.set_ylabel('$ASTDV$')
# ax.legend(loc='upper left')
fig.tight_layout()
plt.show()

# SCR
WSCR[0] = 1 # для простоты
APYscr = (WSCR[T-1] / WSCR[0])**2-1 # годовая процентная прибыль
# sum = 0
# for t in range(1, T):
# 	x_t = X_T(bscr, t)
# 	sum += ln(x_t)

# muscr = sum / T
muscr = math.log(WSCR[T - 1] / WSCR[0]) / T
sum = 0
for t in range(1, T):
	x_t = X_T(bscr[t], t)
	sum += math.log(x_t - muscr)**2
sigmascr = sum / T # стандартное отклонение
ASTDVscr = sigmascr * math.sqrt(T) # годовое стандартное отклонение

#максимальная просадка
MDDscr = -1000000000
for i in range(1,T1):
    for j in range(1,i):
        MDDscr = max(MDDscr, WSCR[j] - WSCR[i])

relAPY_ASTDVscr = APYscr / ASTDVscr
relAPY_MDDscr = APYscr / MDDscr

# UP
WUP[0] = 1 # для простоты
APYup = (WUP[T-1] / WUP[0])**2-1 # годовая процентная прибыль
# sum = 0
# for t in range(1, T):
# 	x_t = X_T(bup, t)
# 	sum += math.log(x_t)

# muup = sum / T
muup = math.log(WUP[T - 1] / WUP[0]) / T
sum = 0
for t in range(1, T):
	x_t = X_T(bup[t], t)
	sum += math.log(x_t - muup)**2
sigmaup = sum / T # стандартное отклонение
ASTDVup = sigmaup * math.sqrt(T) # годовое стандартное отклонение

#максимальная просадка
MDDup = -1000000000
for i in range(1,T1):
    for j in range(i):
        MDDup = max(MDDup, WUP[j] - WUP[i])

relAPY_ASTDVup = APYup / ASTDVup
relAPY_MDDup = APYup / MDDup

# EG
WEG[0] = 1 # для простоты
APYeg = (WEG[T-1] / WEG[0])**2-1 # годовая процентная прибыль
# sum = 0
# for t in range(1, T):
# 	x_t = X_T(beg, t)
# 	sum += math.log(x_t)

# mueg = sum / T
mueg = math.log(WEG[T - 1] / WEG[0]) / T
sum = 0
for t in range(1, T):
	x_t = X_T(beg[t], t)
	sum += math.log(x_t - mueg)**2
sigmaeg = sum / T # стандартное отклонение
ASTDVeg = sigmaeg * math.sqrt(T) # годовое стандартное отклонение

#максимальная просадка
MDDeg = -1000000000
for i in range(1,T1):
    for j in range(i):
        MDDeg = max(MDDeg, WEG[j] - WEG[i])

relAPY_ASTDVeg = APYeg / ASTDVeg
relAPY_MDDeg = APYeg / MDDeg

# ONS
WONS[0] = 1 # для простоты
APYons = (WONS[T-1] / WONS[0])**2-1 # годовая процентная прибыль
# sum = 0
# for t in range(1, T):
# 	x_t = X_T(bons, t)
# 	sum += math.log(x_t)

# muons = sum / T
muons = math.log(WONS[T - 1] / WONS[0]) / T
sum = 0
for t in range(1, T):
	x_t = X_T(bons[t], t)
	sum += math.log(x_t - muons)**2
sigmaons = sum / T # стандартное отклонение
ASTDVons = sigmaons * math.sqrt(T) # годовое стандартное отклонение

#максимальная просадка
MDDons = -1000000000
for i in range(1,T1):
    for j in range(i):
        MDDons = max(MDDons, WONS[j] - WONS[i])

relAPY_ASTDVons = APYons / ASTDVons
relAPY_MDDons = APYons / MDDons

# Визуализация

APY = [APYscr, APYup, APYeg, APYons]
ASTDV = [ASTDVscr, ASTDVup, ASTDVeg, ASTDVons]
MDD = [MDDscr, MDDup, MDDeg, MDDons]
relAPY_ASTDV = [relAPY_ASTDVscr, relAPY_ASTDVup, relAPY_ASTDVeg, relAPY_ASTDVons]
relAPY_MDD = [relAPY_MDDscr, relAPY_MDDup, relAPY_MDDeg, relAPY_MDDons]
print(APY)
print(ASTDV)
print(MDD)

x = APY
y = ASTDV
data = numpy.column_stack((x, y))

Names = ["SCR", "UP", "EG", "ONS"]
table = [APY, ASTDV, Names]
df = pd.DataFrame(table, index=['x','y','Точка'], columns=['A','B','C','D'])
dft = df.T

fig, ax = plt.subplots(figsize=(10,4))
ax.scatter(x=x, y=y, marker='o', c='w', edgecolor='b')
ax.set_title('Cоотношение риска и производительности')
ax.set_xlabel('$APY$')
ax.set_ylabel('$ASTDV$')
dft.apply(lambda x: ax.annotate(x['Точка'], (x['x'], x['y'])), axis=1)
plt.show()

fig, (ax1, ax2) = plt.subplots(
    nrows=1, ncols=2,
    figsize=(12, 6)
)
ax1.bar(x=Names, height=APY, label=('x', 'y'), color="blue")
ax2.bar(x=Names, height=ASTDV, label=('x', 'y'), color="orange")
ax1.set_title('$APY$')
#ax2.legend(loc=(0.65, 0.8))
ax2.set_title('мера риска $ASTDV$')
ax2.yaxis.tick_right()

plt.show()
plt.show()


fig, (ax) = plt.subplots(
    figsize=(12, 6)
)

ax.bar(x=Names, height=APY, color="blue")
ax.bar(x=Names, height=ASTDV, color="orange")
ax.set_title('APY и ASTDV')
ax.yaxis.tick_right()

plt.show()

fig, (ax) = plt.subplots(
    figsize=(12, 6)
)

ax.bar(x=Names, height=ASTDV, color="blue")
ax.bar(x=Names, height=MDD, color="orange")
ax.set_title('ASTDV и MDD')
ax.yaxis.tick_right()

plt.show()



fig, (ax) = plt.subplots(
    figsize=(12, 6)
)

ax.bar(x=Names, height=relAPY_ASTDV, color="blue")
ax.bar(x=Names, height=relAPY_MDD, color="orange")
ax.set_title('APY/ASTDV и APY/MDD')
ax.yaxis.tick_right()

plt.show()

