from collections import deque
import sys

# 실제 큐
deq = deque([])

# 최종 출력
result = []

for _ in range(0, int(sys.stdin.readline())) : 
    command = sys.stdin.readline().split()

    if command[0] == 'push':
        deq.append(command[1])
    
    elif command[0] == 'pop':
        if len(deq) >= 1:
            result.append(deq.popleft())
        else:
            result.append(-1)
    
    elif command[0] == 'size':
        result.append(len(deq))
    
    elif command[0] == 'empty':
        if len(deq) >= 1:
            result.append(0)
        else:
            result.append(1)
            
    elif command[0] == 'front':
        if len(deq) >= 1:
            result.append(deq[0])
        else:
            result.append(-1)
    
    elif command[0] == 'back':
        if len(deq) >= 1:
            result.append(deq[1])
        else:
            result.append(-1)
            
for item in result:
    print(item)
