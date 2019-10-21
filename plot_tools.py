# n queens plotter
import numpy as np
import matplotlib.pyplot as plt

class n_queens_plotter():
    def __init__(self, nvars, vals):
        self.n = int(np.sqrt(nvars))
        data = np.array(sorted(vals, key=dict(zip(vals, [abs(v) for v in vals])).get)).reshape((self.n,self.n))
        scaled_data = np.minimum(np.maximum(data, 0),1)
        self.data = scaled_data * range(1+10,self.n+1+10) # color data

    def plot(self):
        fig, ax = plt.subplots()
        ax.imshow(self.data)

        # gridlines
        ax.grid(which='major', axis='both', linestyle='-', color='c', linewidth=1)
        ax.set_xticks(np.arange(-.5, self.n, 1));
        ax.set_yticks(np.arange(-.5, self.n, 1));
        plt.show()

