result = ""
flag = False
stack = ""

for i in input():
    if i == "<":
        flag = True
        result += stack[::-1]
        stack = ""
        result += i
        continue
    
    elif i == ">":
        flag = False
        result += i
        continue
    
    elif i == " ":
        result += stack[::-1] + " "
        stack = ""
        continue
        
    if flag:
        result += i
    else:
        stack += i

print(result + stack[::-1]) 