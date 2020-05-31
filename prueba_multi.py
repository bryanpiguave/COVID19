# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 16:43:04 2020

@author: Bryan Piguave
"""

from multiprocessing import Process, Queue

def f(q,x):
    y=x**2
    q.put(y)
    return y

if __name__ == '__main__':
    q = Queue()
    n=100
    l =[0]*n
    for i in range(n):
        p = Process(target=f, args=(q,i))
        p.start()
        p.join()
        l[i]=q.get()