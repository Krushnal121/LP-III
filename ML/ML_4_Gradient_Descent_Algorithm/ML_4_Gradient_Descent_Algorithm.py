# Import necessary libraries
import numpy as np
import matplotlib.pyplot as plt

# Define the function and its derivative
def function(x):
    return (x + 3) ** 2

def derivative(x):
    return 2 * (x + 3)

# Gradient Descent parameters
learning_rate = 0.1  # Step size
n_iterations = 50    # Number of iterations
x_start = 2          # Starting point

# Lists to store x values and corresponding y values for visualization
x_values = [x_start]
y_values = [function(x_start)]

# Gradient Descent Loop
x = x_start
for i in range(n_iterations):
    gradient = derivative(x)           # Compute the gradient at the current point
    x = x - learning_rate * gradient    # Update x value
    y = function(x)                     # Compute y for the updated x

    # Append updated values for visualization
    x_values.append(x)
    y_values.append(y)

# Plot the function and the path of gradient descent
x_range = np.linspace(-10, 4, 100)
y_range = function(x_range)

plt.figure(figsize=(10, 6))
plt.plot(x_range, y_range, label="y = (x + 3)^2", color="blue")
plt.scatter(x_values, y_values, color="red", label="Gradient Descent Path")
plt.plot(x_values, y_values, color="red", linestyle="--")
plt.title("Gradient Descent to Find Local Minima of y = (x + 3)^2")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()

# Show the plot
plt.show()

# Print final results
print(f"Local minimum occurs at x = {x_values[-1]:.4f}, y = {y_values[-1]:.4f}")
