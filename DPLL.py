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
        self.testing = True # make false for more performance

    def run_solver(self, file, testing=False):
        self.testing = testing
        self.parse_input(file) # generates self.formula
        self.solve()
        print("SATus is : ", self.SATus)

    def solve(self):
        SATus = status.WORKING
        self.build_occurrence_stats()  # builds self.stats
        # if not modifying formula, only apply pure literal once
        self.apply_pure_literal()
        counter = 0
        dec_counter = 0
        keep_prop = False
        while SATus is status.WORKING:
            if not keep_prop:
                self.decide()
                dec_counter += 1
                keep_prop = True
            else:
                # propagate until there's nothing else to propagate
                var = self.apply_unit_prop()
                keep_prop = var is not None
            counter +=1
            SATus = self.check_SATus() # backtracking is in here
        self.SATus = SATus
        self.counter = counter
        self.dec_counter = dec_counter

    def check_SATus(self):
        # check for SAT or UNSAT
        SAT_poss = len(self.model) == self.nvars
        for clause in self.formula:
            if all([self.in_model(v) for v in clause]):
                # if all vars in clause are assigned
                tval = self.eval_clause(clause)
                if not tval: # if a clause is false
                    # see if we need to backtrack or FAIL
                    if self.testing:
                        print("model: ", self.model)
                        print("failure in clause: ", clause)
                    SATus = self.try_backtrack()
                    return SATus
                # else:
                #       SAT_poss = SAT_poss and tval
        # if we get here and haven't stopped, we could be SAT
        # or keep working
        if SAT_poss:
            return status.SAT
        else:
            return status.WORKING

    def apply_pure_literal(self):
        stats = self.stats
        # see if each literal in formula is pure
        # and not in  model yet
        for clause in self.formula:
            for variable in clause:
                pure = stats[-variable] == 0
                inmodel = self.in_model(variable)
                if pure and (not inmodel):
                    self.add_to_model(variable)

    def decide(self):
        if self.vars_left_unassigned() > 0:
            var = self.pick_unassigned()
            self.add_to_model(var)
            self.mark_decision(var)

    def apply_unit_prop(self):
        for clause in self.formula:
            unassigned = [v for v in clause if (not self.in_model(v))]
            if len(unassigned) == 1:
                # if there is  just one unassigned variable, check
                # rest of clause to see if it is false under model
                u_var = unassigned[0]
                subclause = clause.copy()
                subclause.remove(u_var)
                subclause_is_true = self.eval_clause(subclause)
                if not subclause_is_true:
                    # if rest of clause is false, unit prop
                    self.add_to_model(u_var)
                    if self.testing:
                        print("Propagated ", u_var, " because of clause ", clause)
                    return u_var # this is the var we prop'ed
                    # leave loop because we should check SATus
        return None # if there was nothing to propagate, report that

    def try_backtrack(self):
        if len(self.decisions) == 0:
            return status.UNSAT
        else:
            self.backtrack()
            return status.WORKING

    def backtrack(self):
        last_dec_var = self.decisions.pop() # take last decision and remove
        d_ind = self.model.index(last_dec_var) # get index in model
        self.model = self.model[:d_ind] # keep part of model before last decision
        self.model.append(-last_dec_var) # change decision
        if self.testing:
            print("Backtracked. Changed ", last_dec_var, " to ", -last_dec_var,
                  ". Discarded ", self.nvars - d_ind - 1, " values.")

    def eval_clause(self, clause):
        # only for clauses or sub clauses which are fully defined in the model
        # evaluate truth value of clause or sub clause under the model
        status = False
        for v in clause:
            v_in_m = v in self.model
            if self.testing:
                nv_in_m = -v in self.model
                assert(v_in_m or nv_in_m)
            status = status or v_in_m
        return status

    def build_occurrence_stats(self):
        # step through formula, create dictionary counting how many times a thing occurs
        stats = dict(zip(range(-self.nvars,self.nvars+1),np.zeros((2*self.nvars+1)).astype(int))) # all literals and their negations
        del stats[0] # delete entry for 0 because there is no variable 0
        for clause in self.formula:
            for variable in clause:
                stats[variable] += 1
        self.stats = stats # will not change unless we modify formula

    def vars_left_unassigned(self):
        return self.nvars - len(self.model)

    def pick_unassigned(self):
        # pick unassigned variable with most occurrences
        # so that we run into conflicts as fast as possible
        # (could also pick some other heuristic)
        return self.get_random_unassigned()

    def get_most_frequent_unassigned(self):
        unassigned = [k for k in self.stats.keys()
                      if (not self.in_model(k)) and (self.stats[k] > 0)] # not in model but in formula
        # sort by most frequently occurring
        sorted_unassigned = sorted(unassigned, key=self.stats.get, reverse=True)
        return sorted_unassigned[0] # return most frequent

    def get_least_frequent_unassigned(self):
        unassigned = [k for k in self.stats.keys()
                      if (not self.in_model(k)) and (self.stats[k] > 0)]  # not in model but in formula
        # sort by least frequently occurring
        sorted_unassigned = sorted(unassigned, key=self.stats.get)
        return sorted_unassigned[0]  # return most frequent

    def get_random_unassigned(self):
        unassigned = [k for k in self.stats.keys()
                      if (not self.in_model(k)) and (self.stats[k] > 0)]  # not in model but in formula
        return np.random.choice(unassigned)

    def mark_decision(self, var):
        self.decisions.append(var)
        if self.testing:
            print("decisions: ", self.decisions)

    def add_to_model(self, variable):
        self.model.append(variable)

    def in_model(self, variable):
        # check if variable or its negation is in the model
        return (variable in self.model) or (-variable in self.model)

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
        self.model = []
        self.decisions = []

    def stripper(self, stringtuple):
        return [int(x) for x in stringtuple.split()][:-1] # drop final 0