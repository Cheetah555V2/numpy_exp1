import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)

N = 10000

points = np.random.uniform([-1,-1],[1,1],(N,2))


count = 0
for x, y in points:
    if x*x + y*y <= 1:
        count += 1

PI = 4 * count / N

print(f"PI is approximate to be {PI:.7f}")

plt.figure(figsize=(6,6))

# plot points
plt.scatter(points[:, 0], points[:, 1], s=1)

# create a circle
circle = plt.Circle(
    (0, 0),          # center
    1,               # radius
    alpha=0.25,       # transparency
    color = "orange"
)

# add circle to the plot
plt.gca().add_patch(circle)

plt.show()