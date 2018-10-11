from math import *
import matplotlib.pyplot as plt
import functools
import numpy as np

CASE = -1

def debug(func):
    def wrap(*args, **kwargs):
        print(*args)
        return func(*args, **kwargs)
    return wrap

def integrate_left(f, num_bars, start, stop):
    if start == stop or num_bars == 0:
        return 0
    bar_width = (stop-start)/num_bars
    #print(f"int: {num_bars}, {start + bar_width}, {stop + bar_width}")
    return sum(f(x) * bar_width for x in np.linspace(start + bar_width, stop, num_bars,
                                                      endpoint=False))

def integrate_right(f, num_bars, start, stop):
    if start == stop or num_bars == 0:
        return 0
    bar_width = (stop-start)/num_bars
    return sum(f(x) * bar_width for x in np.linspace(start, stop - bar_width, num_bars, endpoint=False))

def integrate(f, num_bars, start, stop):
    left = integrate_left(f, num_bars, start, stop)
    right = integrate_right(f, num_bars, start, stop)
    return (left + right) / 2

def area(length, radius, height, angle, x):
    a = 2 * sqrt(radius**2 - x**2)
    b = (height/sin(angle) - (x+radius)/(tan(angle)))
    return a * b 

def draw_case_line(max_volume, x, case):
    plt.plot((x,x), (0,max_volume), "--")
    plt.text(x + 0.1, 0.8*max_volume, f"Fall {case}")

def volume(length, radius, angle, height):
    global CASE
    max_volume = radius ** 2 * pi * length
    bars=1000
    area_func = functools.partial(area, length, radius, height, angle)
    if length*sin(angle) < height < 2*radius*cos(angle):
        x1 = height/cos(angle) - length*tan(angle) - radius
        x2 = height/cos(angle) - radius
        bars_1 = round(bars/(2*radius) * (x1 + radius))
        bars_2 = round(bars/(2*radius) * (x2 - x1))
        v1 = integrate(lambda x : 2 * sqrt(radius**2 - x**2) * length,
                       bars_1, -radius, x1)
        v2 = integrate(area_func, bars_2, x1, x2)

        if CASE != 0:
            draw_case_line(max_volume, height, 3)
            CASE = 0

        return v1 + v2
    if 0 <= height < 2*radius * cos(angle):
        x1 = height/cos(angle) - radius
        bars_1 = round(bars/(2*radius) * (x1 + radius))
        v=integrate(area_func, bars_1, -radius, x1)

        if CASE != 1:
            draw_case_line(max_volume, height, 1)
            CASE = 1

        return v
    if length*sin(angle) < height <= length*sin(angle) + 2*radius*cos(angle):
        x1 = height/cos(angle) - length * tan(angle) - radius
        bars_1 = round(bars/(2*radius) * (x1 + radius))
        bars_2 = round(bars/(2*radius) * (radius - x1))
        v1 = integrate(lambda x : 2 * sqrt(radius**2 - x**2) * length,
                       bars_1, -radius, x1)
        v2 = integrate(area_func, bars_2, x1, radius)

        if CASE != 2:
            draw_case_line(max_volume, height, 2)
            CASE = 2

        return v1 + v2
    else:
        v=integrate(area_func, bars, -radius, radius)

        if CASE != 3:
            draw_case_line(max_volume, height, 4)
            CASE = 3

        return v

def gen_points(length, radius, angle):
    vol = functools.partial(volume, length, radius, angle)
    too = length*sin(angle) + 2 * radius * cos(angle)
    num_points = 1000
    return [(x, vol(x)) for x in np.linspace(0, too, num_points)]

fig, ax = plt.subplots()
#ax = fig.add_subplot(1,1,1)

ax.spines['left'].set_position(('data', 0.0))
ax.spines['bottom'].set_position(('data', 0.0))
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')

#plt.xticks([2,4,6,8,10])
#plt.yticks([50,100,150,200])

points = gen_points(8,3,pi/4)
x1, y1 = [coord[0] for coord in points], [coord[1] for coord in points]

#points2 = gen_points(8,3,pi/6)
#x2, y2 = [coord[0] for coord in points2], [coord[1] for coord in points2]

plt.setp(ax.get_yticklabels()[1], visible=False)
plt.setp(ax.get_xticklabels()[1], visible=False)

plt.plot(x1,y1, "k") #, x2, y2, "b")



plt.show()