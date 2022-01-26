import sys

T = int(sys.stdin.readline())

for t in range(T):
    command = sys.stdin.readline().strip()
    stack = []
    for c in command:
        if c == '(':
            stack.append(c)
        elif c == ')':
            if len(stack) != 0 and stack[-1] == '(':
                stack.pop()
            else:
                stack.append(c)

    if len(stack) == 0:
        print('yes')
    else :
        print('no')

# import sys
# input = sys.stdin.readline

# n = int(input())

# for _ in range(n):
#    stack = 0
#    x = input().rstrip()
#    for i in range(len(x)):
#      if x[i] == '(':
#        stack += 1
#      else:
#        stack -= 1
#        if stack < 0:
#          print('NO')
#          break
#    if stack == 0:
#      print('YES')
#    elif stack > 0:
#      print('NO')
