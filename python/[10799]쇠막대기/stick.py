bar = list(input())
stack = []
bar_total = 0

for b in range(len(bar)):
    if bar[b] == '(':
        stack.append(bar[b])
        print(stack)
        
    else:
        if bar[b-1] == '(':
            stack.pop()
            bar_total += len(stack)
            print(bar_total)
        else:
            stack.pop()
            bar_total += 1
            print(bar_total)
        
print(bar_total)