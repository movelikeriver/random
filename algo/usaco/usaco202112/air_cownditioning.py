"""
http://www.usaco.org/index.php?page=viewproblem2&cpid=1156


goal : 6 10 6 2 1 4 0 6 3 1
input: 8 7 5 3 7 4 9 10 2 0


step-1:

the delta is:
-2, 3, 1, -1, -6, 0, -9, -4, 1, 1 

find all the tops and bottoms,
-2, 3, 1, -1, -6, 0, -9, -4, 1, 1 
==>
-2, 3, -6, 0, -9, 1 
inserts 0 into gap between neg and pos
-2, 0, 3, 0, -6, 0, -9, 0, 1 
it's same as converting the neg to pos
2, 0, 3, 0, 6, 0, 9, 0, 1 


step-2 (basic solution: cut tops):

if the array is like multi-peak curve like [7, 4, 17, 7, 16, 6, 9],
it can be solved as:
[7, 4, 17, 7, 16, 6, 9]
remove one top, because tops can't be shared by one tune
[(7), 4, (17), 7, (16), 6, (9)]
==>
[4, 7, 6]
ret += 7-4 + 17-7 + 16-7 + 9-6 => 3+10+9+3=25

do it one more time
[4, (7), 6]
=>
[4, 6]
ret += 7-6

do it one more time
[4, (6)]
=>
[4]
ret += 6-4

then
ret += 4

ret = 32


step-2 (better solution: monotone stack):

[7, 4, 17, 7, 16, 6, 9]

find next bottom
[7, 4]
ret += 7-4 | 3
stack: [4]

find next bottom
[4, 17, 7]
ret += 17-7 | 3+10=13
stack: [4, 7] => [7]
note that, it's the same as [4, 17] => [17] 7 => [7] 17-7
if the next is greater, just replace the stack top,
if the next is less, sum the delta, and start the next one.

find next bottom
[7, 16, 6]
ret += 16-7 | 13+9=22
stack: [7, 6]
since 6 is a new bottom, need to handle 7 as well
ret += 7-6 | 22+1 = 23
stack: [6]

find next bottom
[6, 9] => [9]
ret += 9

ret = 23+9 = 32

"""

import sys


def pos_sol(input_list):
    ret = 0
    stack_top = input_list[0]
    for i in range(1, len(input_list)):
        v = input_list[i]
        if v < stack_top:
            ret += stack_top - v
        stack_top = v

    ret += stack_top
    return ret



def solution(goal, in_list):
    delta = []
    for i in range(len(goal)):
        delta.append(goal[i] - in_list[i])

    v = delta[0]
    if v < 0:
        v = -v
    sublist = [v]
    # [1, -1, -2, -2, 2] => [1, 0, 1, 2, 0, 2]
    for i in range(1, len(delta)):
        v = delta[i]
        prev = delta[i-1]
        if v == prev:
            # deduping
            continue
        if v * prev < 0:
            sublist.append(0)
        if v < 0:
            v = -v
        sublist.append(v)

    # print('sublist: {}'.format(sublist))
    return pos_sol(sublist)



# main
size = int(input())
goal = [int(x) for x in input().split(' ')]
in_list = [int(x) for x in input().split(' ')]

# lines = open(sys.argv[1]).readlines()
# size = int(lines[0].strip())
# goal = [int(x) for x in lines[1].strip().split(' ')]
# in_list = [int(x) for x in lines[2].strip().split(' ')]

# sanity check
assert len(goal) == size
assert len(in_list) == size

# print(goal)
# print(in_list)

ret = solution(goal, in_list)

# ret = pos_sol([1, 0, 1, 2, 0, 2])

print(ret)
