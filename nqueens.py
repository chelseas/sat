# generate the constraints for the n queens puzzle
import numpy as np
import itertools as it
import os

class n_queens():
    def __init__(self, n):
        self.n = n
        self.vars = np.array([i for i in range(1,n*n+1)]).reshape(n,n)

    def encode(self, dir="/Users/Chelsea/scratch"):
        self.generate_constraints()
        self.print_file(dir)

    def generate_constraints(self):
        # todo: later make a SET of clauses, not just list
        self.gen_row()
        self.gen_col()
        self.gen_diag()
        self.gen_all_present()
        clauses = [self.row_constraints, self.col_constraints,
                   self.diag_constraints, self.all_present_constraints]
        self.clauses = [item for sublist in clauses for item in sublist]
        return self.clauses

    def print_file(self, dir):
        # write code to print file format
        # from clauses in self.clauses
        n = self.n
        fname = os.path.join(dir, "n_queens_" + str(n) + ".txt")
        with open(fname, "w") as f:
            for i in range(4):
                f.write("c\n")
            info_line = "p cnf " + str(n*n) + " " + str(len(self.clauses)) + "\n"
            f.write(info_line)
            for clause in self.clauses:
                stw = " ".join([str(j) for j in clause])
                stw = stw + " 0\n" # newline character
                f.write(stw)
        print("Success! Problem written to: ", fname)

    def gen_row(self):
        n = self.n
        vars = self.vars
        row_clauses = []
        for i in range(n): # for each row
            rowvars = vars[i,:]
            row_clauses.extend(self.gen_1_row(rowvars))
        self.row_constraints = row_clauses

    def gen_1_row(self, rowvars):
        # we want to generate pairs not(A and B)
        # or after using DeMorgan, (notA or notB)
        # because our clauses will be implicitly disjunctions ("or")
        # "row" could be a row or column or diagonal
        #
        neg_rv = [-v for v in rowvars] # negate each variable
        combos = it.combinations(neg_rv, 2)
        return combos

    def gen_col(self):
        n = self.n
        vars = self.vars
        col_clauses = []
        for j in range(n):
            colvars = vars[:,j]
            col_clauses.extend(self.gen_1_row(colvars))
        self.col_constraints = col_clauses

    def gen_diag(self):
        n = self.n
        vars = self.vars
        offset = range(-(n-1),n)
        diag_clauses = []
        # do topleft-bottomright diagonals
        for o in offset:
            diag = np.diagonal(vars, offset=o)
            diag_clauses.extend(self.gen_1_row(diag))
        # do topright-bottomleft diagonals
        for o in offset:
            diag = np.diagonal(np.fliplr(vars), offset=o)
            diag_clauses.extend(self.gen_1_row(diag))
        self.diag_constraints = diag_clauses

    def gen_all_present(self):
        # mandate that each row must have at least 1 queen
        n = self.n
        vars = self.vars
        all_present_clauses = []
        for i in range(n):
            all_present_clauses.append(tuple(vars[i,:]))
        self.all_present_constraints = all_present_clauses



