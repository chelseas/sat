from enum import Enum
import numpy as np

class status(Enum):
    SAT = 1
    UNSAT = 0
    WORKING = 85

class DPLL():
    def __init__(self):
        self.model = []  # list of (var, bool) tuples
        self.decisions = []  # list of var (integers)

    def run_solver(self, file):
        self.parse_input(file) # generates self.formula
        self.solve()

    def solve(self):
        SATus = status.WORKING
        # if not modifying formula, only apply pure literal once
        self.apply_pure_literal()
        funs = [self.apply_unit_prop,
                self.decide]
        counter = 0
        while SATus is status.WORKING:
            if counter % 2 == 0:
                funs[0]()
            elif counter % 2 == 1:
                funs[1]()
            counter +=1
            SATus = self.check_SATus() # backtracking is in here

    def check_SATus(self):
        # check for SAT or UNSAT
        # if pseudofail, backtrack and continue
        # if real fail, report SATus as UNSAT
        pass

    def build_occurrence_stats(self):
        # step through formula, create dictionary counting how many times a thing occurs
        stats = dict(zip(range(-self.nvars,self.nvars+1),np.zeros((2*self.nvars+1)).astype(int))) # all literals and their negations
        del stats[0] # delete entry for 0 because there is no variable 0
        for clause in self.formula:
            for variable in clause:
                stats[variable] += 1
        self.stats = stats # will not change unless we modify formula

    def apply_pure_literal(self):
        self.build_occurrence_stats() # builds self.stats
        stats = self.stats
        # see if each literal in formula is pure
        # and not in  model yet
        for clause in self.formula:
            for variable in clause:
                pure = stats[-variable] == 0
                inmodel = self.check_if_in_model(variable)
                neginmodel = self.check_if_in_model(-variable)
                if pure and (not inmodel) and (not neginmodel):
                    self.add_to_model(variable)

    def add_to_model(self, variable):
        self.model.append(variable)

    def check_if_in_model(self, variable):
        return (variable in self.model)

    def backtrack(self):
        pass

    def parse_input(self, file):
        farray = open(file).read().split('\n')
        # get rid of comments
        # assume no whitespace at top of file
        # just:
        # c
        # c
        # p cnf .. ..
        # 1 3 -5 0
        # ...
        for i in range(len(farray)):
            if farray[i][0] is not 'c':
                assert(farray[i][0] is 'p')
                infos = farray[i].split()
                self.nvars = int(infos[-2])
                self.nclauses = int(infos[-1])
                break
        formula = [self.stripper(clause) for clause in farray[i+1:]]
        # strip empty clauses
        formula = [clause for clause in formula if len(clause)>0]
        self.formula = formula

    def stripper(self, stringtuple):
        return [int(x) for x in stringtuple.split()][:-1] # drop final 0