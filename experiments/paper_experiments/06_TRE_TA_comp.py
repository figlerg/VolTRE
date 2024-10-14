import matplotlib.pyplot as plt
import pandas as pd

# Use the PDF backend which doesn't require LaTeX installed
# plt.rcParams.update({
#     "pgf.texsystem": "pdflatex",  # Use pdflatex (commonly available)
#     "font.family": "serif",       # Use serif fonts (like LaTeX)
#     "text.usetex": True,          # Enable LaTeX rendering
#     "pgf.rcfonts": False,         # Disable font setup for consistency
# })

plt.rcParams.update({
    "pgf.texsystem": "pdflatex",  # Use pdflatex (commonly available)
    "font.family": "serif",       # Use serif fonts (like LaTeX)
    "text.usetex": True,          # Enable LaTeX rendering
    "pgf.rcfonts": False,         # Disable font setup for consistency
    "font.size": 10,              # Set default font size (match your LaTeX document)
    "axes.labelsize": 10,         # Set the size of axis labels
    "legend.fontsize": 9,         # Set the size of the legend
    "xtick.labelsize": 9,         # Set the size of x-tick labels
    "ytick.labelsize": 9,         # Set the size of y-tick labels
})

# Sample (fake) data for the two plots
x_1 = [2, 3, 4, 5, 6, 7]  # n TA_Killer
x_2 = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21]

# y1_a = [0.01, 0.01, 0.06, 1.45, 24.93, float('nan')]  # Dataset TA TA_Killer
# y2_a = [0.48, 0.58, 1.24, 2.27, 5.3, 12.33]   # Fake dataset 2 for subplot A
# y1_b = [0.01, 0.01, 0.01, 0.03, 0.07, 0.18, 0.44, 0.98] # Dataset TA Thick_Language
# y2_b = [0.06, 0.4, 0.76, 2.18, 5.04, 18.73, 36.14, 95.75] # Fake dataset 2 for subplot B

y1_a = [0.01, 0.01, 0.06, 1.45, 24.93, float('nan')]
y2_a = [0.48,0.58,1.24,2.27,5.03,12.33]
    # ,40.02,139.64]

y1_b = [0.01,0.01,0.01,0.03,0.07,0.18,0.44,0.98,2.10,4.28,8.32]
# y2_b = [0.08,0.46,1.04,3.30,14.27,12.95,64.51,64.61,275.88,304.64,542.13]
thicktwin_df = pd.read_csv('05_thicktwin.csv',delimiter=' ')

y2_b = thicktwin_df['execution time']

# Create a figure with two subplots arranged horizontally
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 3))

# Plot for subplot A
ax1.plot(x_1, y2_a, label='TRE Sampler')
ax1.plot(x_1, y1_a, label='TA Sampler')
ax1.set_title('Bad-for-TA Family of Languages')  # Subtitle for the first plot
ax1.set_xlabel('n')
ax1.set_ylabel('time (s)')
ax1.legend()

# Plot for subplot B
ax2.plot(x_2, y2_b, label='TRE Sampler')
ax2.plot(x_2, y1_b, label='TA Sampler')
ax2.set_title(r'Language of $e_{ex3}$')  # Subtitle for the second plot
ax2.set_xlabel('n')
ax2.set_ylabel('time (s)')
ax2.legend()

# Adjust layout to make sure titles and labels fit well
plt.tight_layout()

# plt.show()
plt.savefig("06_TRE_TA_comp.pdf")  # Use .pgf if you prefer
