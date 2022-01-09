N =int(input())
P = input()
result = 0

P_list = sorted(list(map(int, P.split(' '))))

for i in range(1,N+1,1) : 
    result += sum(P_list[:i])
print(result)