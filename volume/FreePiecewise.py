import sympy as sp
import matplotlib.pyplot as plt
import numpy as np


class FreePiecewise:
    """
    This is ChatGPT, since it is basically a bunch of boiler plate code very similar to VolumePoly and MaxEntDist.
    I didn't want to do it again
    TODO unified view of the three concepts (probably VolumePoly < MaxEntDist < FreePiecewise in terms of generality).
    """
    def __init__(self, intervals, expressions):
        assert len(intervals) == len(expressions), "Each interval must have a corresponding expression."

        self.intervals = intervals
        self.expressions = expressions

    def __call__(self, value):
        for (a, b), expr in zip(self.intervals, self.expressions):
            if a <= value < b or (b == sp.oo and value >= a):
                return expr.subs('T', value).evalf()
        return 0  # Return 0 if value doesn't fall into any interval

    def __str__(self):
        result = []
        for (a, b), expr in zip(self.intervals, self.expressions):
            result.append(f"Interval [{a}, {b}): {expr}")
        return "\n".join(result)

    def __mul__(self, number):
        if isinstance(number, (int, float)):
            new_expressions = [expr * number for expr in self.expressions]
            return FreePiecewise(self.intervals, new_expressions)
        else:
            raise ValueError("Can only multiply by a number (int or float).")

    @property
    def pairs(self):
        return list(zip(self.intervals, self.expressions))

    def plot(self, no_show=False, title = ''):
        nr = 5

        for (a, b), expr in zip(self.intervals, self.expressions):
            if b == sp.oo:
                # Plot on [a, a+1] and mark it
                x_vals = np.linspace(float(a), float(a) + 1, nr)
                y_vals = [float(expr.subs('v', x)) for x in x_vals]
                plt.plot(x_vals, y_vals, label=f"{expr} on [{a}, ∞)", linestyle='dashed')
                plt.axvline(x=float(a) + 1, color='gray', linestyle='dotted')
                plt.text(float(a) + 0.5, max(y_vals), '∞', ha='center', va='bottom')
            else:
                x_vals = np.linspace(float(a), float(b), nr)
                y_vals = [expr.subs('T', x).evalf() for x in x_vals]
                plt.plot(x_vals, y_vals, label=f"{expr} on [{a}, {b})")

            # Add dotted vertical lines at the borders of the intervals
            plt.axvline(x=float(a), color='gray', linestyle='dotted')
            if b != sp.oo:
                plt.axvline(x=float(b), color='gray', linestyle='dotted')

        plt.xlabel('v')
        plt.ylabel('f(v)')
        if title:
            plt.title(f'FreePiecewise: {title}')
        # plt.legend()
        plt.grid(True)
        plt.tight_layout()
        if not no_show:
            plt.show()

if __name__ == '__main__':

    # Example usage
    intervals = [(0, 1), (1, 2), (2, sp.oo)]
    expressions = [sp.sympify('v**2'), sp.sympify('2*v + 1'), sp.sympify('v - 1')]

    piecewise_function = FreePiecewise(intervals, expressions)

    # Testing the __call__ method
    for v in [0.5, 1.5, 2.5, 3.5]:
        result = piecewise_function(v)
        print(f"f({v}) = {result}")

    # Testing the __str__ method
    print(piecewise_function)

    # Testing the __mul__ method
    scaled_function = piecewise_function * 2
    print(scaled_function)

    # Testing the plot method
    piecewise_function.plot()
