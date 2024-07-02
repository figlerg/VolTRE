def start():
    return "a1+"


def step(prev_expr, n):
    return f"< a{n} . {prev_expr} >_[{0},{n}]"


def generate_expression(n):
    expression = start()
    for i in range(2, n + 1):
        expression = step(expression, i)
    return expression


def save_to_file(filename, n):
    expression = generate_expression(n)
    with open(filename, 'w') as file:
        file.write(expression)

if __name__ == '__main__':

    n = 15

    name = f'TAkiller_{n}_gen.tre'
    save_to_file(n=n, filename=name)