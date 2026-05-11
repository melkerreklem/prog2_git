""" MA3.py

Student:
Mail:
Reviewed by:
Date reviewed:

"""
import random
import matplotlib.pyplot as plt
import math as m
import functools
import concurrent.futures as future
import numpy as np
from statistics import mean 
from time import perf_counter as pc

def approximate_pi(n): # Ex1
    inside = 0
    outside = 0
    #plt.figure(figsize=(6,6))
    for num in range(n):
        x = random.uniform(-1,1)
        y = random.uniform(-1,1)
        if (x**2 + y**2)**(1/2) <= 1:
            inside += 1
            #plt.scatter(x, y, color = 'r')
        else:
            outside += 1
            #plt.scatter(x, y, color = 'b')
        pi_approx = 4 * inside / (inside + outside)
    print(f'number of points: {n}')
    print(f'pi approximation: {pi_approx}')
    #plt.show()
    return pi_approx

def sphere_volume(n, d): #Ex2, approximation
    #n is the number of points
    # d is the number of dimensions of the sphere 
    inside = 0
    outside = 0
    for num in range(n):
        lst = []
        for dim in range(d):
           x = random.uniform(-1,1)
           lst.append(abs(x))
        #print(lst)
        sq_sum = functools.reduce(lambda x,y : x+y, map(lambda z : z*z, lst))
        norm = m.sqrt(sq_sum)
        if norm <= 1:
            inside += 1
        else:
            outside += 1
    V_approx = 2**d * inside / (outside + inside)
    return V_approx

def hypersphere_exact(n,d): #Ex2, real value
    #n is the number of points
    # d is the number of dimensions of the sphere 
    V = (m.pi**(d/2))/(m.gamma(d/2 + 1))
    return V

#Ex3: parallel code - parallelize for loop
def sphere_volume_parallel1(n,d,np=10):
    #n is the number of points
    # d is the number of dimensions of the sphere
    #np is the number of processes
    with future.ProcessPoolExecutor() as ex:
        pn = [n for x in range(np)]
        pd = [d for x in range(np)]
        results = ex.map(sphere_volume, pn, pd)

        res_sum = 0
        for r in results:
            res_sum += r
        res_avg = res_sum/np
    return res_avg

#Ex4: parallel code - parallelize actual computations by splitting data

def sphere2(n,d):
    #n is the number of points
    # d is the number of dimensions of the sphere 
    inside = 0
    outside = 0
    for num in range(n):
        lst = []
        for dim in range(d):
           x = random.uniform(-1,1)
           lst.append(abs(x))
        #print(lst)
        sq_sum = functools.reduce(lambda x,y : x+y, map(lambda z : z*z, lst))
        norm = m.sqrt(sq_sum)
        if norm <= 1:
            inside += 1
        else:
            outside += 1
    return inside, outside

def sphere_volume_parallel2(n,d,np=10):
    #n is the number of points
    # d is the number of dimensions of the sphere
    #np is the number of processes
    with future.ProcessPoolExecutor() as ex:
        pn = [int(n/np) for x in range(np)]
        pd = [d for x in range(np)]
        all_points = ex.map(sphere2, pn, pd)

        inside_sum = 0
        outside_sum = 0
        for inside, outside in all_points:
            inside_sum += inside
            outside_sum += outside
    V_approx = 2**d * inside_sum / (outside_sum + inside_sum)
    return V_approx

 
def main():
    
    #Ex1
    print('EXERCISE 1')
    dots = [100, 200, 1000]
    for n in dots:
        approximate_pi(n)
    

    #Ex2
    print('EXERCISE 2')
    n = 100000
    d = 2
    sphere_volume(n,d)
    print(f"Actual volume of {d} dimentional sphere = {hypersphere_exact(n,d)}")
    print(f"Approximated volume of {d} dimentional sphere = {sphere_volume(n,d)}")

    n = 100000
    d = 11
    sphere_volume(n,d)
    print(f"Actual volume of {d} dimentional sphere = {hypersphere_exact(n,d)}")
    print(f"Approximated volume of {d} dimentional sphere = {sphere_volume(n,d)}")
    

    
    #Ex3
    print('EXERCISE 3')
    n = 100000
    d = 11
    start = pc()
    tot = 0
    for y in range(10):
        tot += sphere_volume(n,d)
    stop = pc()
    avg_seq = tot/10
    print(f"Ex3: Sequential time of dimension {d} and {n} number of points : {stop-start} s")
    print(f'Average function output: {avg_seq}')
    
    start = pc()
    avg_parallel = sphere_volume_parallel1(n, d, 10)
    stop = pc()
    print(f'Parallel time of dimension {d} and {n} number of points : {stop-start} s')
    print(f'Average function output: {avg_parallel}')
    

    
    #Ex4
    print('EXERCISE 4')
    n = 1000000
    d = 11
    start = pc()
    vol = sphere_volume(n,d)
    stop = pc()
    print(f"Ex4: Sequential time of dimension{d} and {n} number of points: {stop-start} s")
    print(f'Function output: {vol}')
    
    start = pc()
    V_parallel = sphere_volume_parallel2(n, d, np = 100)
    stop = pc()
    print(f'Parallel time of dimension {d} and {n} number of points: {stop-start} s')
    print(f'Average function output: {V_parallel}')

if __name__ == '__main__':
	main()