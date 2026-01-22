import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42) # for repeatability 👍

u = np.random.uniform(0, 1, 10000)
n = np.random.normal(0, 1, 10000)

plt.figure(figsize=(8,5))

plt.hist(u, bins=100, density=True, alpha=0.6, label="Uniform")
plt.hist(n, bins=100, density=True, alpha=0.6, label="Normal")

plt.xlabel("Value")
plt.legend()

plt.show()

"""
We can see that np.random.uniform is basically pure random (or at least trying to be)
the 0 and 1 is the lowest and highest number they can be

But on the other hand, np.random.normal is a normal distribution
0 is the median, 1 is the standard deviation
So the randomness is based on normal distribution of the given arguemnts
"""