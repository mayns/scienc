# -*- coding: utf-8 -*-

__author__ = 'mayns'


import random
import matplotlib.pyplot as plt

xr = []
for x in xrange(100):
    n = 10000
    p = 0.3
    y = [random.uniform(1, n) for i in xrange(n)]
    p = [1 for j in y if j < n*p]
    xr.append(sum(p) / float(n) * 100)

plt.hist(xr, 100)
plt.show()