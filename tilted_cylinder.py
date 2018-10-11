from math import *
import matplotlib.pyplot as plt
import functools
import numpy as np

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

a = False
b = False
c = False
d = False

def volume(length, radius, angle, height):
    global a,b,c,d
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
        if not a:
            plt.plot((height,), (v1+v2,), "bo")
            a = True
        return v1 + v2
    if 0 <= height < 2*radius * cos(angle):
        x1 = height/cos(angle) - radius
        bars_1 = round(bars/(2*radius) * (x1 + radius))
        v=integrate(area_func, bars_1, -radius, x1)
        if not b:
            plt.plot((height,), (v,), "bo")
            b = True
        return v
    if length*sin(angle) < height <= length*sin(angle) + 2*radius*cos(angle):
        x1 = height/cos(angle) - length * tan(angle) - radius
        bars_1 = round(bars/(2*radius) * (x1 + radius))
        bars_2 = round(bars/(2*radius) * (radius - x1))
        v1 = integrate(lambda x : 2 * sqrt(radius**2 - x**2) * length,
                       bars_1, -radius, x1)
        v2 = integrate(area_func, bars_2, x1, radius)

        if not c:
            plt.plot((height,), (v1+v2,), "bo")
            c = True
        return v1 + v2
    else:
        v=integrate(area_func, bars, -radius, radius)
        if not d:
            plt.plot((height,), (v,), "bo")
            d = True
        return v

def gen_points(length, radius, angle):
    vol = functools.partial(volume, length, radius, angle)
    too = length*sin(angle) + 2 * radius * cos(angle)
    num_points = 1000
    return [(x, vol(x)) for x in np.linspace(0, too, num_points)]


points = gen_points(8,3,pi/4)
x1, y1 = [coord[0] for coord in points], [coord[1] for coord in points]

points2 = gen_points(8,3,pi/6)
x2, y2 = [coord[0] for coord in points2], [coord[1] for coord in points2]

#x1 = 8/cos(pi/4) - 8 * tan(pi/4) - 3
#area_func = functools.partial(area, 8, 3, 8*sin(pi/4) + 2*3*cos(pi/4), pi/4)
#print(integrate(area_func, 1000, -3, x1) + integrate(area_func, 1000, x1, 3))
#print(integrate(lambda x : 2*sqrt(9-x**2) * 8,1000, -3, 3))
#print(volume(8,3,pi/4, 8*sin(pi/4) + 2*3*cos(pi/4)))

plt.plot(x1,y1, "k", x2, y2, "b")
print(x1[-1], y1[-1])
plt.show()