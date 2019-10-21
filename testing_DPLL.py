from DPLL import DPLL
import time
from plot_tools import n_queens_plotter
from nqueens import n_queens

solver = DPLL()

#for n in range(1,100):
n=10
print("n is: ", n)
n_queens(n).encode("/Users/Chelsea/scratch")
t = time.time()
solver.run_solver("/Users/Chelsea/scratch/n_queens_"+str(n)+".txt", testing=False)
dt = time.time() - t
print("dt: ", dt, " seconds, aka ", dt/60, " minutes.")
print("counter: ", solver.counter)
print("decisions: ", solver.dec_counter)

#n_queens_plotter(solver.nvars, solver.model).plot()