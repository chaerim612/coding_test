N = int(input())
cnt = 0

# 방법1
# if N==4 or N==7 :
#     print(-1)

# elif (N%5==1) or (N%5==3) :
#     cnt=(N//5)+1
#     print(cnt)
# elif (N%5==2) or (N%5==4) :
#     cnt=(N//5)+2
#     print(cnt)
# else : 
#     cnt=N//5
#     print(cnt)


#방법2
# while N >= 0 :
#     if N % 5 == 0 :
#         cnt += N // 5
#         print(cnt)
#         break
#     else :
#         N -= 3
#         cnt += 1
    
# else : 
#     print(-1)

N = int(input())
cnt = -1

Y_lst = [N//5, N//5-1, N//5-2]

for Y in Y_lst :
    if Y < 0 or (N-5*Y) < 0 :
        continue
    if (N-5*Y)%3 == 0:
        X = (N-5*Y)//3
        cnt = X+Y
        
print(cnt)