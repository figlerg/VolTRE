import math

import sympy as sp
from sympy import oo

# Define the variables
T, lambda1, lambda2 = sp.symbols('T lambda1 lambda2')

# Define the polynomial and exponential term
p_T = T**2
exp_term = sp.exp(lambda1 * T + lambda2 * T**2)

# Define the integrand
integrand = p_T * exp_term

# Define the integration bounds
L = sp.symbols('L')
result = sp.integrate(integrand, (T, 0, math.inf))

# Display the result
sp.pretty_print(result)

# print(sp.simplify(result).pretty_print(result))
print(result := result.subs(lambda1, 1))
print(result := result.subs(lambda2, 4))

print(result.evalf())
print(oo == math.inf)

print(result > 100000000)