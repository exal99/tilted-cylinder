#from math import *
import matplotlib.pyplot as plt
import functools
import numpy as np

CASE = -1

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
    a = 2 * np.sqrt(radius**2 - x**2)
    b = (height/np.sin(angle) - (x+radius)/(np.tan(angle)))
    return a * b 

def draw_case_line(max_volume, x, case):
    plt.plot((x,x), (0,max_volume), "--")
    plt.text(x + 0.1, 0.8*max_volume, f"Fall {case}")

def volume(length, radius, angle, height):
    global CASE
    max_volume = radius ** 2 * np.pi * length
    bars=1000
    area_func = functools.partial(area, length, radius, height, angle)
    if length*np.sin(angle) < height < 2*radius*np.cos(angle):
        x1 = height/np.cos(angle) - length*np.tan(angle) - radius
        x2 = height/np.cos(angle) - radius
        bars_1 = int(round(bars/(2*radius) * (x1 + radius)))
        bars_2 = int(round(bars/(2*radius) * (x2 - x1)))
        v1 = integrate(lambda x : 2 * np.sqrt(radius**2 - x**2) * length,
                       bars_1, -radius, x1)
        v2 = integrate(area_func, bars_2, x1, x2)

        if CASE != 0:
            draw_case_line(max_volume, height, 3)
            CASE = 0

        return v1 + v2
    if 0 <= height < 2*radius * np.cos(angle):
        x1 = height/np.cos(angle) - radius
        bars_1 = int(round(bars/(2*radius) * (x1 + radius)))
        v=integrate(area_func, bars_1, -radius, x1)

        if CASE != 1:
            draw_case_line(max_volume, height, 1)
            CASE = 1

        return v
    if length*np.sin(angle) < height <= length*np.sin(angle) + 2*radius*np.cos(angle):
        x1 = height/np.cos(angle) - length * np.tan(angle) - radius
        bars_1 = int(round(bars/(2*radius) * (x1 + radius)))
        bars_2 = int(round(bars/(2*radius) * (radius - x1)))
        v1 = integrate(lambda x : 2 * np.sqrt(radius**2 - x**2) * length,
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
    vol = np.vectorize(functools.partial(volume, length, radius, angle))
    too = length*np.sin(angle) + 2 * radius * np.cos(angle)
    num_points = 1000
    x = np.linspace(0, too, num_points)
    y = vol(x)
    return x, y

fig, ax = plt.subplots()

ax.spines['left'].set_position(('data', 0.0))
ax.spines['bottom'].set_position(('data', 0.0))
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')


x1, y1 = gen_points(8,3,np.pi/4)

plt.setp(ax.get_yticklabels()[1], visible=False)
plt.setp(ax.get_xticklabels()[1], visible=False)

plt.plot(x1,y1, "k")

plt.show()