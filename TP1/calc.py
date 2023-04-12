import sys
import getopt

operator = ''
num1 = ''
num2 = ''

try:
    opts, args = getopt.getopt(sys.argv[1:], 'o:n:m:', ['operator=', 'num1=', 'num2='])
except getopt.GetoptError:
    print('Usage: calc.py -o <operator> -n <num1> -m <num2>')
    sys.exit(2)

for opt, arg in opts:
    if opt in ('-o', '--operator'):
        operator = arg
    elif opt in ('-n', '--num1'):
        num1 = arg
    elif opt in ('-m', '--num2'):
        num2 = arg

if not operator or not num1 or not num2:
    print('Usage: calculator.py -o <operator> -n <num1> -m <num2>')
    sys.exit(2)

try:
    num1 = float(num1)
    num2 = float(num2)
except ValueError:
    print('Error: Invalid number')
    sys.exit(2)

result = None

if operator == '+':
    result = num1 + num2
    print(f'{num1} {operator} {num2} = {result}')
elif operator == '-':
    result = num1 - num2
    print(f'{num1} {operator} {num2} = {result}')
elif operator == 'por':
    result = num1 * num2
    print(f'{num1} * {num2} = {result}')
elif operator == '/':
    result = num1 / num2
    print(f'{num1} {operator} {num2} = {result}')


