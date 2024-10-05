"""
http://www.usaco.org/index.php?page=viewproblem2&cpid=1155


find one char,
GHHHGHHHG
 ^  ^  ^
 l  i  r

(i-l)*(r-i)
+ i-l-1 (if >=2 H in the middle)
+ r-i-1 (if >=2 H in the middle)

go through all the char.
if i==l or i==r, it will be zero

"""

import sys


def solution(n, instr):
    ret = 0
    for i in range(0, n):
        ch = instr[i]

        # find the left index GG[H]HHHHH(G)HH
        left = i
        while left-1 >= 0 and instr[left-1] != ch:
            left -= 1
        right = i
        
        # find the right index HH(G)HHHHH[H]GG
        while right+1 < n and instr[right+1] != ch:
            right += 1

        ret += (i-left) * (right-i)

        # remember to add left and right, and minus 1
        if i-left >= 2:
            ret += i-left-1
        if right-i >= 2:
            ret += right-i-1
        #print(left, right, i, ret)

    return ret




# main
n = int(input())
instr = input()

# lines = open(sys.argv[1]).readlines()
# n = int(lines[0].strip())
# instr = lines[1].strip()

ret = solution(n, instr)
print(ret)
