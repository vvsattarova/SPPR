import numpy as np
import time as tm
from scipy.optimize import linprog
from pulp import *
from cvxopt.modeling import variable, op


def work(m, s, a):
    matrix = m
    sender = s
    acceptor = a
    sender_num = 0
    acceptor_num = 0
    open_flag = False
    vector = []
    for ii in matrix:
        for jj in ii:
            vector.append(jj)
    for i in range(len(sender)):
        sender_num += sender[i]
        acceptor_num += acceptor[i]
    if sender_num == acceptor_num:
        print("Задача закрытая")
    elif sender_num > acceptor_num:
        print("Задача открытая")
        open_flag = True
    elif sender_num < acceptor_num:
        print("Задача открытая")
        temp = sender.copy()
        sender = acceptor.copy()
        acceptor = temp.copy()
        open_flag = True
    array_of_x = []
    x_names = []
    array_of_x_data = np.zeros(25, dtype=int)
    matrix_angle_method = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
    temp_sender = sender.copy()
    temp_acceptor = acceptor.copy()
    for i in range(25):
        x_num = "x{}".format(i+1)
        x_names.append(x_num)
        x = pulp.LpVariable(x_num, lowBound=0)
        array_of_x.append(x)
    i = 0
    j = 0
    while i != 5 and j != 5:
        if temp_sender[i] == 0:
            i += 1
        elif temp_acceptor[j] == 0:
            j += 1
        elif temp_sender[i] >= temp_acceptor[j]:
            matrix_angle_method[i][j] = temp_acceptor[j]
            temp_sender[i] -= temp_acceptor[j]
            temp_acceptor[j] = 0
            j += 1
        elif temp_sender[i] < temp_acceptor[j]:
            matrix_angle_method[i][j] = temp_sender[i]
            temp_acceptor[j] -= temp_sender[i]
            temp_sender[i] = 0
            i += 1

    print("Метод северо-западного угла")
    print(matrix_angle_method)
    i = 0
    j = 0
    sum = 0
    for i in range(5):
        for j in range(5):
            sum += matrix_angle_method[i][j] * matrix[i][j]
    print("Стоимость: ", str(sum))

    problem = pulp.LpProblem("0", LpMaximize)
    problem += - matrix[0][0] * array_of_x[0] - matrix[0][1] * array_of_x[1] - matrix[0][2] * array_of_x[2] - matrix[0][3]\
           * array_of_x[3] - matrix[0][4] * array_of_x[4] \
           - matrix[1][0] * array_of_x[5] - matrix[1][1] * array_of_x[6] - matrix[1][2] * array_of_x[7] - matrix[1][3]\
           * array_of_x[8] - matrix[1][4] * array_of_x[9] \
           - matrix[2][0] * array_of_x[10] - matrix[2][1] * array_of_x[11] - matrix[2][2] * array_of_x[12] - \
           matrix[2][3] * array_of_x[13] - matrix[2][4] * array_of_x[14] \
           - matrix[3][0] * array_of_x[15] - matrix[3][1] * array_of_x[16] - matrix[3][2] * array_of_x[17] - \
           matrix[3][3] * array_of_x[18] - matrix[3][4] * array_of_x[19] \
           - matrix[4][0] * array_of_x[20] - matrix[4][1] * array_of_x[21] - matrix[4][2] * array_of_x[22] - \
           matrix[4][3] * array_of_x[23] - matrix[4][4] * array_of_x[24], "Функция цели"

    problem += array_of_x[0] + array_of_x[1] + array_of_x[2] + array_of_x[3] + array_of_x[4] <= sender[0] #поставщик
    problem += array_of_x[5] + array_of_x[6] + array_of_x[7] + array_of_x[8] + array_of_x[9] <= sender[1] #поставщик
    problem += array_of_x[10] + array_of_x[11] + array_of_x[12] + array_of_x[13] + array_of_x[14] <= sender[2] #поставщик
    problem += array_of_x[15] + array_of_x[16] + array_of_x[17] + array_of_x[18] + array_of_x[19] <= sender[3] #поставщик
    problem += array_of_x[20] + array_of_x[21] + array_of_x[22] + array_of_x[23] + array_of_x[24] <= sender[4] #поставщик

    problem += array_of_x[0] + array_of_x[5] + array_of_x[10] + array_of_x[15] + array_of_x[20] == acceptor[0] #потребитель
    problem += array_of_x[1] + array_of_x[6] + array_of_x[11] + array_of_x[16] + array_of_x[21] == acceptor[1] #потребитель
    problem += array_of_x[2] + array_of_x[7] + array_of_x[12] + array_of_x[17] + array_of_x[22] == acceptor[2] #потребитель
    problem += array_of_x[3] + array_of_x[8] + array_of_x[13] + array_of_x[18] + array_of_x[23] == acceptor[3] #потребитель
    problem += array_of_x[4] + array_of_x[9] + array_of_x[14] + array_of_x[19] + array_of_x[24] == acceptor[4] #потребитель

    problem.solve()
    print("Result: ")
    temp_ind = 0
    for variable in problem.variables():
        array_of_x_data[x_names.index(variable.name)] = int(variable.varValue)
    print("Стоимость доставки: ", str(abs(value(problem.objective))))
    for i in range(5):
        for j in range(5):
            print('%3d' % array_of_x_data[i*5+j], end=" ")
        print()

    # start = tm.time()
    # x = variable(25, "x")
    # z = (matrix[0][0] * x[0] + matrix[0][1] * x[1] + matrix[0][2] * x[2] + matrix[0][3] * x[3] + matrix[0][4] * x[4] +
    #  matrix[1][0] * x[5] + matrix[1][1] * x[6] + matrix[1][2] * x[7] + matrix[1][3] * x[8] + matrix[1][4] * x[9] +
    #  matrix[2][0] * x[10] + matrix[2][1] * x[11] + matrix[2][2] * x[12] + matrix[2][3] * x[13] + matrix[2][4] *
    #  x[14] + matrix[3][0] * x[15] + matrix[3][1] * x[16] + matrix[3][2] * x[17] + matrix[3][3] * x[18] + matrix[3][4]
    #  * x[19] + matrix[4][0] * x[20] + matrix[4][1] * x[21] + matrix[4][2] * x[22] + matrix[4][3] * x[23] +
    #  matrix[4][4] * x[24])
    #
    # mass1 = (x[0] + x[1] + x[2] + x[3] + x[4] <= sender[0]) #поставщик
    # mass2 = (x[5] + x[6] + x[7] + x[8] + x[9] <= sender[1]) #поставщик
    # mass3 = (x[10] + x[11] + x[12] + x[13] + x[14] <= sender[2]) #поставщик
    # mass4 = (x[15] + x[16] + x[17] + x[18] + x[19] <= sender[3]) #поставщик
    # mass5 = (x[20] + x[21] + x[22] + x[23] + x[24] <= sender[4]) #поставщик
    #
    # mass6 = (x[0] + x[5] + x[10] + x[15] + x[20] == acceptor[0]) #потребитель
    # mass7 = (x[1] + x[6] + x[11] + x[16] + x[21] == acceptor[1]) #потребитель
    # mass8 = (x[2] + x[7] + x[12] + x[17] + x[22] == acceptor[2]) #потребитель
    # mass9 = (x[3] + x[8] + x[13] + x[18] + x[23] == acceptor[3]) #потребитель
    # mass10 = (x[4] + x[9] + x[14] + x[19] + x[24] == acceptor[4]) #потребитель
    #
    # x_non_negative = (x>=0)
    # problem = op(z, [mass1, mass2, mass3, mass4, mass5, mass6, mass7, mass8, mass9, mass10, x_non_negative])
    # problem.solve(solver="glpk")
    # print("Result: {}".format(x.value))
    # print("Price: {}".format(problem.objective.value()[0]))
    # stop = tm.time()
    # print(stop-start)


    start = tm.time()
    c = vector.copy()
    a_ub=[[1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0],
      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1]]
    b_ub=sender.copy()
    a_eq=[[1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0],[0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,],
      [0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0],[0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,],
      [0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1]]
    b_eq = acceptor.copy()
    res = linprog(c,a_ub,b_ub,a_eq,b_eq)
    print()
    print("Стоимость доставки: ", str(res.fun))
    stop = tm.time()
    print(stop-start)


acceptors = []
senders = []
temp = []
temp_send = []
matrixes = []
index = 1
count = 0
with open("transporttasks.txt") as f:
    for line in f:
        if index == 1:
            count += 1
            a = [int(x) for x in line.split()]
            acceptors.append(a)
        if index > 1 and index < 7:
            a = [int(x) for x in line.split()]
            b = a.pop(0)
            temp_send.append(b)
            temp.append(a)
        if index == 7:
            senders.append(temp_send)
            matrixes.append(temp)
            index = 0
            temp = []
            temp_send = []
        index += 1

index = 0
acceptors.pop(len(acceptors)-1)
for index in range(len(acceptors)):
    work(matrixes[index], senders[index], acceptors[index])
    print()
    print()
    print()

# acceptor = [10, 10, 25, 25, 30]
# sender = [10, 20, 10, 30, 10]
# matrix = [[1, 5, 7, 9, 3],
# [4, 6, 4, 7, 13],
# [1, 5, 3, 4, 9],
# [2, 4, 2, 10, 3],
# [3, 2, 5, 6, 4]]