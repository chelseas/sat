from enum import Enum

class status(Enum):
    SAT = 1
    UNSAT = 0

class DPLL():
    def __init__(self):
        pass

    def run_solver(self, file):
        self.parse_input(file)
        self.solve()

    def solve(self):
        pass

    def check_SATus(self):
        if len(self.formula) == 0:
            return status.SAT
        elif min([len(clause) for clause in self.formula]) == 0:
            return status.UNSAT
        else:
            return "in progress..."


    def parse_input(self, file):
        # stuff to read file
        self.formula = None # replace with stuff. list of clauses
