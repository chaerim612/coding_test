import sys

N = int(sys.stdin.readline())
stack=[]

for i in range(0,N):
    commamd = sys.stdin.readline().split()
    
    if commamd[0]=='push':
        num = int(commamd[1])
        stack.insert(0,num)
    
    elif commamd[0]=='pop':
        if len(stack) == 0 :
            print(-1)
        else :
            print(stack[0])
            del stack[0]
    
    elif commamd[0]=='empty':
        if not stack:
            print(1)
        else:
            print(0)
    
    elif commamd[0]=='size':
        print(len(stack))
    
    else:
        if not stack :
            print(-1)
        else :
            print(stack[0])