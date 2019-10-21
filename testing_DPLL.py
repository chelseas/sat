from DPLL import DPLL
import time
from plot_tools import n_queens_plotter
from nqueens import n_queens
import os

solver = DPLL()

# # test capacity of solver
# for n in range(1,100):
#     print("n is: ", n)
#     if not os.path.isfile("/Users/Chelsea/scratch/n_queens_"+str(n)+".txt"):
#         n_queens(n).encode("/Users/Chelsea/scratch")
#     t = time.time()
#     solver.run_solver("/Users/Chelsea/scratch/n_queens_"+str(n)+".txt", testing=False)
#     dt = time.time() - t
#     print("dt: ", dt, " seconds, aka ", dt/60, " minutes.")
#     print("counter: ", solver.counter)
#     print("decisions: ", solver.dec_counter)
#     if dt/60 > 5:
#         break

n = 5
n_queens(n).encode("/Users/Chelsea/scratch")
solver.run_solver("/Users/Chelsea/scratch/n_queens_"+str(n)+".txt", testing=False)
n_queens_plotter(solver.nvars, solver.model).plot()