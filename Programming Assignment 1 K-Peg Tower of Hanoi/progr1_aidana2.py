import sys
import math
from collections import deque

# this is from the https://levelup.gitconnected.com/the-easy-guide-to-python-command-line-arguments-96b4607baea1 website
import argparse
parser = argparse.ArgumentParser(description='k-peg tower of hanoi')
parser.add_argument("disks", type = int)
parser.add_argument("k_peg", type = int)

args = parser.parse_args()


n = int(args.disks)
n_peg = int(args.k_peg)



Towers = deque()


def is_everything_legal():
    result = True
    for i in range(n_peg):
        for j in range(len(Towers[i])):
            for k in range(j, len(Towers[i])):
                if (Towers[i][k] < Towers[i][j]):
                    result = False
    return (result)


# Function ${\sf move\_top\_disk (source, dest)}$ moves the top-disk from ${\sf source}$ and places it on ${\sf dest}$.  Following this, it checks if any larger-diameter disk has been placed on a smaller diameter disk in any of the 4 Pegs.

def move_top_disk(source, dest):
    x = Towers[source].popleft()
    Towers[dest].appendleft(x)
    if (True == is_everything_legal()):
        y = " (Legal)"
    else:
        y = " (Illegal)"

    print("Move disk " + str(x) + " from Peg " + str(source + 1) + " to Peg " + str(dest + 1) + y)


def move_using_three_pegs(number_of_disks, source, dest, intermediate):
    if (1 == number_of_disks):
        move_top_disk(source, dest)
    else:
        move_using_three_pegs(number_of_disks - 1, source, intermediate, dest);
        move_top_disk(source, dest)
        move_using_three_pegs(number_of_disks - 1, intermediate, dest, source)


# This is the recursive solution to the 4-Peg Tower of Hanoi Problem -- where we move $(\lfloor \frac{\mbox{no of disks}}{2} \rfloor)$-many disks from the source-peg to the first-intermediate peg, and we let it sit there till the remaining disks are moved from the source-peg to the destination-peg using the second-intermediate peg (via the 3-Peg solution).  Following this, we move the $(\lfloor \frac{\mbox{no of disks}}{2} \rfloor)$-many disks from the first-intermediate peg to the detination peg.

def move_using_four_pegs(number_of_disks, source, dest, intermediate1, intermediate2):
    if (number_of_disks > 0):
        k = math.floor(math.sqrt(2 * number_of_disks))
        move_using_four_pegs(number_of_disks - k, source, intermediate1, intermediate2, dest)
        move_using_three_pegs(k, source, dest, intermediate2)
        move_using_four_pegs(number_of_disks - k, intermediate1, dest, intermediate2, source)

# The idea of using stack to move the disks from one peg to another was taken from : https://stackoverflow.com/questions/12545231/tower-of-hanoi-edit-k-peg-solution
def move(number_of_disks, source, dest, stack):
    if (number_of_disks == 1):
        move_top_disk(source, dest)
    elif (number_of_disks < 3):
        move_using_three_pegs(number_of_disks, source, dest, stack[-1])
    elif (n_peg <= 4):
        move_using_four_pegs(source, dest, stack[-2], stack[-1])


    else:

        if (len(stack) >= 2):
            p = math.floor(number_of_disks / 2)
        else:
            p = number_of_disks - 1

        # move top "p" disks from peg 1 to peg i

        middle = stack.popleft()
        stack.appendleft(dest)

        move(p, source, middle, stack)

        # move "n-p" disks from peg 1 to another peg
        stack.popleft()

        move(number_of_disks - p, source, dest, stack)

        # move top "p" disks from peg i to peg k
        stack.appendleft(source)
        move(p, middle, dest, stack)


for i in range(n_peg):
    X = deque()
    if (i == 0):
        for j in range(n):
            X.append(j + 1)
    Towers.append(X)

pegs = deque()
for i in range(n_peg - 3):
    pegs.append(i + 1)

move(n, 0, n_peg - 1, pegs)
