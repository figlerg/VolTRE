from enum import Enum


class Subfamily(Enum):
    VANILLA = 1
    STAR = 2


def start():
    return "<a1.a1*>_[0,1]"


def vanilla_step(prev_expr, n):
    return f"< a{n} . {prev_expr} >_[{0},{n}]"

def star_step(prev_expr, n):
    return f"< a{n}* . {prev_expr} >_[{0},{n}]"

def generate_expression(n, mode:Subfamily):
    """
    The TAkiller family. (Nested concatenation and restriction).
    """
    expression = None

    match mode:
        case Subfamily.VANILLA:
            expression = start()
            for i in range(2, n + 1):
                expression = vanilla_step(expression, i)

        case Subfamily.STAR:
            expression = start()
            for i in range(2, n + 1):
                expression = star_step(expression, i)

    assert expression, "Something went wrong during creation of example."

    return expression



def save_to_file(filename, expression):


    with open(filename, 'w') as file:
        file.write(expression)

    print(f"Saved {expression} \nto file {filename}.")

if __name__ == '__main__':

    n = 3

    mode = Subfamily.STAR
    name = f'TAkiller_{mode}_{n}_gen.tre'

    expr = generate_expression(n, mode)

    save_to_file(filename=name, expression=expr)
