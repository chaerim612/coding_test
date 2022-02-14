N = int(input())
A = list(map(int, input().split()))

result = [-1] * N   # -1 출력을 위해
stack = []  # 인덱스 저장

for n in range(N):
    while stack and A[stack[-1]] < A[n]:    # stack이 비어있지 않으면서 A의 n번째 이전 원소가 n번째 원소보다 작을때
        result[stack.pop()] = A[n]          ## 이전 인덱스가 없을 경우를 대비해 stack이라는 인덱스 리스트르 넣은 것
    
    stack.append(n)

print(*result)  # 이렇게 쓰면 리스트가 문자열처럼 보인다
