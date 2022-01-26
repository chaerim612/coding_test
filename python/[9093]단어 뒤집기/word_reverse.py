import sys

T = int(sys.stdin.readline())
result = ''
test_cases = []

for t in range(T):
    test_case = sys.stdin.readline()
    reverse_item = ''.join(reversed(test_case)).split()[::-1]
    result = ' '.join(reverse_item)
    test_cases.append(result)
    result = ''

for t in range(T):
    print(test_cases[t])