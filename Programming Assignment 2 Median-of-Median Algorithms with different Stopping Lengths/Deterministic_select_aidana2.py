#!/usr/bin/env python3
# coding: utf-8
import sys
import argparse
import random
import numpy as np
import time
import math
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf
sys.setrecursionlimit(3000)

# sort the array and pick the k-th smallest element from the sorted-array
def sort_and_select(current_array, k) :
    # sort the array
    sorted_current_array = np.sort(current_array)

    return sorted_current_array[k]

def deterministic_select(current_array, k, div) :
    if (len(current_array) <= div) :
        # just use any method to pick the k-th smallest element in the array
        # I am using the sort-and-select method here
        return sort_and_select(current_array, k)
    else :
        # I need this array to compute the median-of-medians...
        medians_of_smaller_arrays_of_size_m = []

        # first, split current_array into smaller arrays with 5 elements each
        # there might be a better way than what I am doing... but this will work...
        for i in range(0,len(current_array), div):
            smaller_array_of_size_m = []
            smaller_array_of_size_m.extend(current_array[i:i+div])

           # smaller_array_of_size_m.extend([current_array[i+1:i+div]])
           # for l in range(1,div,1):
            #  if ((i + l) < len(current_array)):
             #   smaller_array_of_size_m.extend([current_array[i+l]])
            #print(len(smaller_array_of_size_m))

            # we need each of these cases as len(smaller_array_of_size_five) can be anything between 1 and 5
            # based on len(smaller_array_of_size_five) we are computing the median of smaller_array_of_size_five for each case
            if (len(smaller_array_of_size_m) == 1):
                medians_of_smaller_arrays_of_size_m.extend([deterministic_select(smaller_array_of_size_m, 0, div)])
            elif(len(smaller_array_of_size_m)%2 == 1):
                medians_of_smaller_arrays_of_size_m.extend([deterministic_select(smaller_array_of_size_m, int((len(smaller_array_of_size_m)+1)/2), div)])
            else:
                medians_of_smaller_arrays_of_size_m.extend([deterministic_select(smaller_array_of_size_m, int(len(smaller_array_of_size_m)/2), div)])

        # compute the meadian of the medians_of_smaller_arrays_of_size_five array by recursion
        p = deterministic_select(medians_of_smaller_arrays_of_size_m, int(len(medians_of_smaller_arrays_of_size_m)/2), div)
        # split the current_array into three sub-arrays: Less_than_p, Equal_to_p and Greater_than_p
        Less_than_p = []
        Equal_to_p = []
        Greater_than_p = []
        for x in current_array :
            if (x < p) :
                Less_than_p.extend([x])
            if (x == p) :
                Equal_to_p.extend([x])
            if (x > p) :
                Greater_than_p.extend([x])

        if (k < len(Less_than_p)) :
            return deterministic_select(Less_than_p, k, div)
        elif (k >= len(Less_than_p) + len(Equal_to_p)) :
            return deterministic_select(Greater_than_p, (k - len(Less_than_p) - len(Equal_to_p)), div)
        else :
            return p


#initializing all the values
#arrrays for running time for the deterministic select
t = []
t_ave = [[0] * 5 for ti in range(10)]

#arrrays for running time for the sort and pick algorithm
t_sort = []
t_ave_sort = [[0] * 5 for _ in range(10)]

trials = 100
list_of_m = [5, 7, 9, 11, 13]

#rows and columns for tracking time
row = 0
column = 0
# rows and columns for inserting graphs on one list
f_row = 0
f_col = 0

fig, axes = plt.subplots(nrows=3, ncols=3)
pdf = matplotlib.backends.backend_pdf.PdfPages("output.pdf")



for n in range(1000, 10000, 1000):
    for m in list_of_m:
        for i in range(trials):
            n_array = [random.randint(1,100*n) for _ in range(n)]
            k1 = int((n + 1)/2)


            t0 = time.time()
            kth_smallest = deterministic_select(n_array, k1, m)
            t1 = time.time()
            t.append((t1 - t0))

            t2 = time.time()
            kth_smallest_sort = sort_and_select(n_array, k1)
            t3 = time.time()
            t_sort.append((t3-t2))


        #finding average trial time for each algorithm
        t_ave[row][column] = sum(t)/len(t)
        t_ave_sort[row][column] = sum(t_sort)/len(t_sort)
        t = []
        t_sort = []
        column = column + 1

    # Finding the m value with the minimum average running time
    result = np.where(t_ave[row] == np.amin(t_ave[row]))
    ind = result[0][0]


    # plotting the graph on one page
    axes[f_row, f_col].plot(list_of_m, t_ave[row], color = 'red')
    axes[f_row, f_col].plot(list_of_m, t_ave_sort[row], color = 'green')

    axes[f_row, f_col].set_title('Array Size = ' + str(n))

    f_col = f_col + 1
    if (f_col > 2):
        f_row = f_row + 1
        f_col = 0

    #updating column for t_ave
    column = 0
    row = row + 1


fig.subplots_adjust(hspace=0.5)
plt.show()


pdf.savefig(fig)
pdf.close()
