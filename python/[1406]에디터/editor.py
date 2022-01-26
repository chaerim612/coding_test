import sys

line = sys.stdin.readline().strip()
stack = line.split()
count = len(stack)
M = int(sys.stdin.readline().strip())

for m in range(0,M):
    command = sys.stdin.readline().strip()
    
    if 'P' == command[0]:
        stack.insert(count, command.strip().split()[-1])
        count += 1
    elif 'L' == command[0]:
        if count > 0 :
            count -= 1
    elif 'D' == command[0]:
        if count < len(stack) : 
            count += 1
    elif 'B' == command[0]:
        if count > 0 :
            stack.pop()
            count -= 1

print(''.join(stack))