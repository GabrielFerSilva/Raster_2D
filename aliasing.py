import random as rd
import numpy as np

def aliasing_filter(string,sigma,N):
    if string.lower() == 'box':
        return box(N,sigma)
    elif string.lower() == 'hat':
        return hat(N,sigma)
    elif string.lower() == 'gaussian':
        return gaussian(N,sigma)

def box(N,sigma):
    return np.random.uniform(-sigma, sigma, size=(N, 2))

def hat(N,sigma):
    u1 = np.random.uniform(0, sigma, size=(N, 2))
    u2 = np.random.uniform(0, sigma, size=(N, 2))
    return u1 - u2

def gaussian(N,sigma): 
    return np.random.normal(loc=0, scale=sigma, size=(N, 2))
