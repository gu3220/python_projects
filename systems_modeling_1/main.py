from random import random
import math

z = []
s = []
m = 1000
a_tz = 39
a_ts = 39
b = 1
x = 1
tz_min = 4
tz_max = 12
ts_max = 8
ts_min = 2

def prng(xi, a, m, b):
    xi = (a*xi+b) % m
    return xi/m

zi = prng(x, a_tz, m, b)
si = prng(x, a_ts, m, b)

for i in range(10):
    zi = prng(zi*m, a_tz, m, b)
    z.append(round((zi*(tz_max-tz_min)+tz_min), 3))
    si = prng(si * m, a_ts, m, b)
    s.append(round((si * (ts_max - ts_min) + ts_min), 3))

def time(app):
    time = []
    t = 0
    for i in app:
        time.append(round((i+t), 3))
        t += i
    return time

def bf(time, work):
    s_new = work.copy()
    process = []
    buffer = []
    for i in range(len(time)):
        process.append([time[i], 0])
    last = 0
    for i in range(len(time)-1):
        if (s_new[i] + time[i]) > time[i+1]:
            process[i+1][0] += (s_new[i] + time[i]) - time[i+1]
            s_new[i + 1] += (s_new[i] + time[i]) - time[i + 1]
            if (i == len(time) - 2):
                last = (s_new[i] + time[i]) - time[i + 1]
    for i in range(len(process)):
        process[i][1] = process[i][0] + work[i]
        buffer.append([time[i], process[i][0]])
    count = [0 for i in range(10)]
    for i in range(len(process)-1):
        if process[i][1] > buffer[i+1][0]:
            times = 0
            c = i+1
            while c <= len(buffer)-1:
                if process[i][1] > buffer[c][0]:
                    times += 1
                    count[times] += process[i][1] - buffer[c][0]
                c+=1
    for i in range(len(count)-2, 0, -1):
        count[i] -= count[i+1]
    return count, last

def pr(time, work):
    buffer_time, last = bf(time, work)
    common_time = time[len(time) - 1] + work[len(work) - 1] + last
    print('Общее время: ', round(common_time, 3))
    bt = sum(buffer_time)
    print('Время нахождения программ в буфере: ', round(bt, 3))
    for i in range(len(buffer_time)):
        if(buffer_time[i] != 0):
            print('Время нахождения в буфере программ в количестве', i, '-', round(buffer_time[i], 3))
    for i in range(len(buffer_time)):
        if(buffer_time[i] != 0):
            tp = buffer_time[i]/common_time
            print('Вероятность нахождения в буфере программ в количестве', i, '-', round(tp, 3))

print('Линейный закон:')
time1 = time(z)
print('Входной поток заявок:', z)
print('Время обработки заявок сервером:', s)
print('Времена прихода программ:', time1)
pr(time1, s)

lz = 1/3
ls = 1/4

def exp(l):
    e = []
    for i in range(10):
        x = random()
        e.append(round((-1/l)*math.log(x, math.exp(1)), 3))
    return e

print('\nЭкспоненциальный закон:')
z_random = exp(lz)
s_random = exp(ls)
time2 = time(z_random)
print('Входной поток заявок:', z_random)
print('Время обработки заявок сервером:', s_random)
print('Времена прихода программ:', time2)
pr(time2, s_random)