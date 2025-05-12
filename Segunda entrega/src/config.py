# SIMULATION PARAMETERS:

BANK_NAME = "Bank Central"

#Number of simulation steps (time units).
TOTAL_STEPS = 5

#The branches with number of counters and risk for each operations (loans and investments).
BRANCHES = [{"name": "Bank Branch A", "counters": 2, "loan_interest": 0.05, "invest_interest": 0.03},
            {"name": "Bank Branch B", "counters": 2, "loan_interest": 0.04, "invest_interest": 0.08},
           {"name": "Bank Branch C", "counters": 2, "loan_interest": 0.03, "invest_interest": 0.06}]

#Number of clients per simulation.
NUM_CLIENTS_OPTIONS = [10, 20]

# SALARY CONFIGUTRATION:
# Minimum initial salary.
MIN_SALARY_OPTIONS = [100, 200]
#Maximum initial salary.
MAX_SALARY_OPTIONS = [1000, 5000]