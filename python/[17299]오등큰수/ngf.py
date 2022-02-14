import sys
from collections import Counter

N = int(sys.stdin.readline().rstrip())
A = list(map(int, sys.stdin.readline().rstrip().split()))
count = Counter(A)
result = [-1] * N
index = []

for n in range(N):
    while index and count[A[index[-1]]] < count[A[n]]:
        result[index.pop()] = A[n]
    
    index.append(n)

print(*result)
