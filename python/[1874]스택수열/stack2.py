n = int(input())
stack = []      # 입력한 숫자가 들어가는 리스트
result = []     # 실제로 연산자가 들어가는 리스트
cnt = 0         
flag = True     # 수열을 만들 수 있는지 없는지 여부 확인

for items in range(0, n) : 
    N = int(input())
    
    # push
    while cnt < N : 
        cnt += 1
        stack.append(cnt)
        result.append('+')
    
    # pop
    if stack[-1] == N :
        stack.pop()
        result.append('-')
    # 스택을 만들 수 없는 경우 -> top != 입력 값
    else :
        flag = False
        break
    
if flag == False :
    print('NO')

else : 
    print('\n'.join(result))