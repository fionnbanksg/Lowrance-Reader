import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load CSV into a pandas DataFrame
data = pd.read_csv('transpose_slow_ping.csv', header=None)

# Convert DataFrame to a numpy array
matrix = data.values

# Plot the matrix as an image
plt.imshow(matrix, cmap='viridis', aspect='auto')
plt.colorbar()  # Add a colorbar for reference
plt.show()
