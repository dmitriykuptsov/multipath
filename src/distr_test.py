from delays import ExponentialDelay
import numpy as np
import matplotlib.pyplot as plt

output = []
gen = ExponentialDelay([0.3, 0.3]);

for i in range(0, 1000):
    output.append(gen.generate())

plt.hist(x=output, bins = 30)
plt.show()
print(np.mean(output))