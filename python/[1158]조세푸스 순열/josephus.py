import sys
from collections import deque

NK = sys.stdin.readline().strip().split()

list = deque([])
result = []

for _ in range(1, int(NK[0])+1):
    list.appendleft(_)

for _ in range(len(list)):
    list.rotate(int(NK[1]))
    n = list.popleft()
    result.append(n)

print('<'+', '.join(map(str, result))+'>')
