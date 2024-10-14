import matplotlib.pyplot as plt
import numpy as np

# Data
n_values = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21]
T_values = [0.6, 1.3, 1.9, 2.6, 3.3, 3.9, 4.6, 5.2, 5.9, 6.6, 7.2]

ns = np.asarray(n_values)
print(ns * 2/3)

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(n_values, T_values, marker='o', linestyle='-', color='b')

# Adding title and labels
plt.title('Plot of n against T')
plt.xlabel('n')
plt.ylabel('T (Execution Time)')
plt.grid()

# Show the plot
plt.show()
