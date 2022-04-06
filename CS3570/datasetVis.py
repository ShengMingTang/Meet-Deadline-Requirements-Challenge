import matplotlib.pyplot as plt
import numpy as np

fnames = [f'block-priority-{i}.csv' for i in range(3)]

for i, fname in enumerate(fnames):
    data = np.loadtxt(fname, delimiter=',')
    plt.subplot(100 * len(fnames) + 10 + i)
    plt.plot(data[:, 0], data[:, 1], drawstyle='steps', label='steps (=steps-pre)')
    plt.plot(data[:, 0], data[:, 1], 'o--', color='grey', alpha=0.3)
    plt.xlabel('time')
    plt.ylabel('size')
    plt.title(fname)
plt.show()