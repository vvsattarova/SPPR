import numpy as np


def matrixgame(input, P, Q):
    # input = [[8, 11, 9, 3, 5], [3, 8, 3, 0, 6], [9, 11, 4, 12, 6], [11, 6, 11, 11, 1], [8, 4, 0, 7, 7]]
    # P = [0.55, 0.0, 0.18, 0.0, 0.26]
    # Q = [0.0, 0.0, 0.18, 0.01, 0.8]

    answer = {}
    answer2 = {}

    lower_price = max([min(x) for x in input])
    upper_price = min([max(x) for x in np.rot90(input)])

    if lower_price == upper_price:
        print("Седловая точка есть, ответ v = ", str(lower_price))
        if lower_price > 0:
            print("Игра выгодна для игрока А")
        elif lower_price < 0:
            print("Игра выгодна для игрока B")
        return 1
    else:
        buff = 0
        for i, pin in zip(input, P):
            buff += pin * sum([x * y for x, y in zip(i, Q)])
        print("Выигрыш игрока А (проигрыш игрока В) при игре в смешанных стратегиях = ", str(buff))
        for k, i in enumerate(np.flipud(np.rot90(input)), 1):
            answer["H(P,B{})".format(k)] = sum([x * y for x, y in zip(i, P)])
        for k, i in enumerate(input, 1):
            answer2["H(P,A{})".format(k)] = sum([x * y for x, y in zip(i, Q)])
        for i in [(x, y) for x, y in answer.items()]:
            print("Выйгрыш игрока А в ситуации {0[0]} = {0[1]}".format(i))
        for i in [(x, y) for x, y in answer2.items()]:
            print("Проигрыш игрока В в ситуации {0[0]} = {0[1]}".format(i))
        return 0

index = 1
matrixes = []
Pelements = []
Qelements = []
temp = []
sedlovaya_tochka = 0
with open("matrix.txt") as f:
    for line in f:
        if index < 6:
            a = [int(x) for x in line.split()]
            temp.append(a)
        if index == 6:
            matrixes.append(temp)
            temp = []
            a = [float(x) for x in line.split()]
            Pelements.append(a)
        if index == 7:
            a = [float(x) for x in line.split()]
            Qelements.append(a)
            index = 0
        index += 1

for i in range(len(matrixes)):
    print("***************************************** Игра {} *********************************************".format(i+1))
    print()
    sedlovaya_tochka += matrixgame(matrixes[i], Qelements[i], Pelements[i])
    print()

print("Игр с седловой точкой: ", str(sedlovaya_tochka))
print("Игр без седловой точки: ", str(len(Pelements) - sedlovaya_tochka))