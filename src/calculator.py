operators = ["+", "-", "/", "*", "x"]

def calculate(expression):
    numbers = []
    ops = []
    digits = []

    # Parse expression
    for char in expression:
        if char.isdigit():
            digits.append(char)

        elif char in operators:
            if not digits:
                return "Invalid expression"

            numbers.append(int("".join(digits)))
            digits.clear()

            if char == "x":
                char = "*"

            ops.append(char)

        else:
            return "Invalid character"

    if digits:
        numbers.append(int("".join(digits)))

    # First pass: * and /
    i = 0
    while i < len(ops):
        if ops[i] == "*":
            numbers[i] = numbers[i] * numbers[i + 1]
            del numbers[i + 1]
            del ops[i]

        elif ops[i] == "/":
            numbers[i] = numbers[i] / numbers[i + 1]
            del numbers[i + 1]
            del ops[i]

        else:
            i += 1

    # Second pass: + and -
    result = numbers[0]

    for i, op in enumerate(ops):
        if op == "+":
            result += numbers[i + 1]
        elif op == "-":
            result -= numbers[i + 1]

    return result


if __name__ == "__main__":
    while True:
        expr = input("calc: ")
        print(calculate(expr))
