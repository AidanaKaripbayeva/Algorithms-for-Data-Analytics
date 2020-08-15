#!/usr/bin/env python3
# coding: utf-8

# Gibbs-Sampling procedure to compute the Probability Matrix of a Discrete-Time Markov
# Chain whose states are the d-dimensional cartesian product of the form
# {0,1,...n-1} x {0,1,...n-1} x ... X {0,1,...n-1} (i.e. d-many products)
#
# The target stationary distribution is expressed over the n**d many states
#
# Written by Prof. R.S. Sreenivas for
# IE531: Algorithms for Data Analytics
#

import sys
import argparse
import random
import numpy as np
import time
import math
import matplotlib.pyplot as plt
import itertools as it
import random
from collections import Counter
random.seed( 30 )



# need this to keep the matrix print statements to 4 decimal places
np.set_printoptions(formatter={'float': lambda x: "{0:0.4f}".format(x)})

# This function computes a random n-dimensional probability vector (whose entries sum to 1)
def generate_a_random_probability_vector(n) :
    l = []
    for x in range(n):
        num = random.randint(1,101)
        l.append(num)

    s = sum(l)
    y = [float(number) / float(s) for number in l]

    return y

def get_lexicographic_index(x, n, dim) :
    num = 0
    for count,i in enumerate(x):

        num = num + n**(dim-count-1)*i

    return num

# Two d-tuples x and y are Gibbs-Neighbors if they are identical, or they differ in value at just
# one coordinate


def check_if_these_states_are_gibbs_neighbors(x, y) :
    # x and y are dim-tuples -- we will assume they are not equal
    # count the number of coordinates where they differ

    if(x == y):
        return True
    list_of_dif = [(i-j) for i, j in zip(x,y)]
    dict_of_dif = Counter(list_of_dif)
    if(dict_of_dif[0] < len(x)-1):
        return False

    return True

# Given two Gibbs-Neighbors -- that are not identical -- find the coordinate where they differ in value
# this is the "free-coordinate" for this pair
def free_coordinates_of_gibbs_neighbors(x, y) :
    # we assume x and y are gibbs neighbors, then the must agree on at least (dim-1)-many coordinates
    # or, they will disagree on just one of the (dim)-many coordinates... we have to figure out which
    # coordinate/axes is free
    list_of_dif = [(i-j) for i, j in zip(x,y)]
    for count,i in enumerate(list_of_dif):
        if( i != 0):
            return count
    pos = -1

    return pos

# This is an implementaton of the Gibbs-Sampling procedure
# The MC has n**dim many states; the target stationary distribution is pi
# The third_variable_is when set to True, prints the various items involved in the procedure
# (not advisable to print for large MCs)
def create_gibbs_MC(n, dim, pi, do_want_to_print) :
    if (do_want_to_print) :
        print ("Generating the Probability Matrix using Gibbs-Sampling")
        print ("Target Stationary Distribution:")
        for x in it.product(range(n), repeat = dim) :
            number = get_lexicographic_index(x, n, dim)
            print ("\u03C0", x, " = \u03C0(", number , ") = ", pi[number])

    # the probability matrix will be (n**dim) x (n**dim)
    probability_matrix = [[0 for x in range(n**dim)] for y in range(n**dim)]

    # the state of the MC is a dim-tuple (i.e. if dim = 2, it is a 2-tuple; if dim = 4, it is a 4-tuple)
    # got this from https://stackoverflow.com/questions/7186518/function-with-varying-number-of-for-loops-python
    for x in it.product(range(n), repeat = dim) :
        # x is a dim-tuple where each variable ranges over 0,1,...,n-1
        for y in it.product(range(n), repeat = dim) :
            if not check_if_these_states_are_gibbs_neighbors(x, y):
                continue
            if(x == y):
                continue


            x_ind = get_lexicographic_index(x, n, dim)
            y_ind = get_lexicographic_index(y, n, dim)
            pos_dif = free_coordinates_of_gibbs_neighbors(x, y)
            z = list(x)
            s = 0
            #countng the number of pi-s that should be added
            for i in range(n):
                z[pos_dif] = i
                z_ind = get_lexicographic_index(z, n, dim)
                s = s + pi[z_ind]

            probability_matrix[x_ind][y_ind] = (1/dim)*pi[y_ind]/(s)

    #finding the values for diagonal
    for i in range(n**dim):
        k = 0
        for j in range(n**dim):
            k = k + probability_matrix[i][j]
        probability_matrix[i][i] = 1 - k

    return probability_matrix

# Trial 1... States: {(0,0), (0,1), (1,0), (1,1)} (i.e. 4 states)
n = 3
dim = 2
a = generate_a_random_probability_vector(n**dim)
print("(Random) Target Stationary Distribution\n", a)
p = create_gibbs_MC(n, dim, a, True)
print ("Probability Matrix:")
print (np.matrix(p))

print ("Does the Probability Matrix have the desired Stationary Distribution?", np.allclose(np.matrix(a), np.matrix(a)* np.matrix(p)))

# Trial 2... States{(0,0), (0,1),.. (0,9), (1,0), (1,1), ... (9.9)} (i.e. 100 states)
n = 10
dim = 2
a = generate_a_random_probability_vector(n**dim)
p = create_gibbs_MC(n, dim, a, False)
print ("Does the Probability Matrix have the desired Stationary Distribution?", np.allclose(np.matrix(a), np.matrix(a)* np.matrix(p)))

# Trial 3... 1000 states
n = 10
dim = 3
t1 = time.time()
a = generate_a_random_probability_vector(n**dim)
p = create_gibbs_MC(n, dim, a, False)
t2 = time.time()
hours, rem = divmod(t2-t1, 3600)
minutes, seconds = divmod(rem, 60)
print ("It took ", hours, "hours, ", minutes, "minutes, ", seconds, "seconds to finish this task")
print ("Does the Probability Matrix have the desired Stationary Distribution?", np.allclose(np.matrix(a), np.matrix(a)* np.matrix(p)))

# Trial 4... 10000 states
n = 10
dim = 4
t1 = time.time()
a = generate_a_random_probability_vector(n**dim)
p = create_gibbs_MC(n, dim, a, False)
t2 = time.time()
hours, rem = divmod(t2-t1, 3600)
minutes, seconds = divmod(rem, 60)
print ("It took ", hours, "hours, ", minutes, "minutes, ", seconds, "seconds to finish this task")
print ("Does the Probability Matrix have the desired Stationary Distribution?", np.allclose(np.matrix(a), np.matrix(a)* np.matrix(p)))
