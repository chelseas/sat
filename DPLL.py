from enum import Enum

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
        funs = [self.apply_pure_literal,
                self.apply_unit_prop,
                self.decide]
        counter = 0
        while SATus is status.WORKING:
            if counter % 3 == 0:
                funs[0]()
            elif counter % 3 == 1:
                funs[1]()
            elif counter % 3 == 2:
                funs[2]()
            counter +=1
            SATus = self.check_SATus() # backtracking is in here

    def check_SATus(self):
        # check for SAT or UNSAT
        # if pseudofail, backtrack and continue
        # if real fal, report SATus as UNSAT
        pass

    def apply_pure_literal(self):
        pass

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