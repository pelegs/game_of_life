#!/usr/bin/env python3
# -*- coding: iso-8859-15 -*-

import numpy as np
from itertools import product
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def neighbors(i, j):
    idsx = np.arange(i-dis, i+dis+1)
    idsy = np.arange(j-dis, j+dis+1)
    if wrap:
        idsx = [x%nx for x in idsx]
        idsy = [y%ny for y in idsy]
    else:
        idsx = [x for x in idsx if 0 <= x < nx]
        idsy = [y for y in idsy if 0 <= y < ny]
    l = list(product(idsx, idsy))
    l.remove((i,j))
    return l

def num_alive(mat, i, j):
    return np.sum([mat[cell] for cell in neighbors(i,j)])


def new_status(mat, i, j):
    n = num_alive(mat, i, j)
    status = mat[i,j]
    if (n in [2,3] and status) or (n==3 and not status):
        return 1
    else:
        return 0

def next_status(mat):
    s0, s1 = mat.shape
    idsx = np.arange(0, s0)
    idsy = np.arange(0, s1)
    ids = list(product(idsx, idsy))
    new_matrix = np.zeros((s0, s1))
    for id in ids:
        new_matrix[id] = new_status(mat, id[0], id[1])
    return new_matrix


nx, ny = 100, 100
dis=1
wrap=True
m_init = np.random.randint(0, 2, size=(nx,ny))
#m_init = np.zeros((nx, ny), dtype=np.bool)
#m_init[1,2] = m_init[2,2] = m_init[3,2] = m_init[3,1] = m_init[2,0] = 1
num_steps = 100

frames = np.zeros((num_steps, nx, ny))
frames[0] = m_init
for i in range(1, num_steps):
    frames[i] = next_status(frames[i-1])

fig = plt.figure()
im = plt.imshow(frames[0], cmap=plt.cm.gray)
plt.axis('off')

def updatefig(i):
    im.set_array(np.logical_not(frames[i]))
    return [im]

ani = FuncAnimation(fig, updatefig, frames=range(num_steps),
                    interval=100, blit=True)
plt.show()
