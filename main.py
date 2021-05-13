import numpy as np
import matplotlib.pyplot as plt

# Основная программа----------------------------------------------------------------------------------------------------------------------------------
# Настройка параметров-----------------------------------------------------------------------
from func import *

gen = 800  # Количество итераций
pc = 0.25  # Кросс вероятность
pm = 0.02  # Вероятность мутации
popsize = 10  # Численность населения
n = 20  # Количество пунктов #,Длина хромосомы n
w = [3, 0.1, 0.2, 1, 0.5, 0.3, 0.4, 0.7, 2.8, 2.2, 0.25, 2.9, 0.9, 0.8, 0.9, 0.1,2.2,1.1,0.5,0.9]  # Весовой список каждого элемента
c = [50, 80, 60, 30, 40, 35, 40, 60, 20, 15, 45, 40, 60, 40, 35,50,80,5,11,100]  # Список цен на каждый товар
W = 7  # Объем рюкзака
M = 5  # Penalty значение
fun = 1  # 1-Первый метод декодирования,2-Второй метод декодирования (штраф)
# Initialize-------------------------------------------------------------------------
# Начальное население (кодирование)
population = init(popsize, n)
# Оценка работоспособности (декодирование)
if fun == 1:
    value, s = fitnessfun1(population, n, w, c, W)
else:
    value, s = fitnessfun2(population, n, w, c, W, M)
# Начальный номер кроссовера
ncross = 0
# Начальный номер мутации
nmut = 0
# Сохранение оптимальной стоимости каждого поколения и соответствующего ему человека
t = []
best_ind = []
last = []  # Сохраните ценность фитнеса последнего поколения людей
realvalue = []  # Сохранить декодированное значение последнего поколения
# Цикл---------------------------------------------------------------------------
for i in range(gen):
    print("Количество итераций:")
    print(i)
    # Cross
    offspring_c = crossover(population, pc, ncross)
    # Изменение #
    # offspring_m=mutation1(offspring,pm,nmut)
    offspring_m = mutation2(offspring_c, pm, nmut)
    mixpopulation = population + offspring_m
    # Расчет функции фитнеса
    if fun == 1:
        value, s = fitnessfun1(mixpopulation, n, w, c, W)
    else:
        value, s = fitnessfun2(mixpopulation, n, w, c, W, M)
        # Выбор рулетки
    population = roulettewheel(mixpopulation, value, popsize)
    # Магазин современных оптимальных решений
    result = []
    if i == gen - 1:
        if fun == 1:
            value1, s1 = fitnessfun1(population, n, w, c, W)
            realvalue = s1
            result = value1
            last = value1
        else:
            for j in range(len(population)):
                g1, f1, s1 = decode2(population[j], n, w, c)
                result.append(f1)
                realvalue.append(s1)
            last = result
    else:
        if fun == 1:
            value1, s1 = fitnessfun1(population, n, w, c, W)
            result = value1
        else:
            for j in range(len(population)):
                g1, f1, s1 = decode2(population[j], n, w, c)
                result.append(f1)
    maxre = max(result)
    h = result.index(max(result))
    # Добавить оптимальное решение каждого поколения в результирующую популяцию
    t.append(maxre)
    best_ind.append(population[h])

# Выходной результат-----------------------------------------------------------------------
if fun == 1:
    best_value = max(t)
    hh = t.index(max(t))
    f2, s2 = decode1(best_ind[hh], n, w, c, W)
    print('Оптимальная комбинация это:')
    print(s2)
    print('Оптимальное решение:')
    print(f2)
    print('Алгебра, где появляется оптимальное решение:')
    print(hh)
    # Построить кривую сходимости
    plt.plot(t)
    plt.title('The curve of the optimal function value of each generation with the number of iterations',
              color='#123456')
    plt.xlabel('the number of iterations')
    plt.ylabel('the optimal function value of each generation')
    plt.show()
else:
    """    best_value=max(result)
    hh=result.index(max(result))
    s2 = realvalue[hh]
    print('Оптимальная комбинация это:')
    print(s2)
    print('Оптимальное решение:')
    print(f2) """
