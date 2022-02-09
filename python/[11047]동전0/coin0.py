N, K = map(int, input().strip().split())

coin_type = []
cnt = 0

for _ in range(N):
    coin_type.append(int(input().strip()))

for i in range(N-1, -1, -1):
    if K == 0:
        break
    elif coin_type[i] > K:
        continue
    cnt += K // coin_type[i]
    K = K % coin_type[i]

print(cnt)

