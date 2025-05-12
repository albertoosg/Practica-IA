#José Emparanza, Alberto Sainz y Santiago Norzagaray
#CUNEF Universidad
#Inteligencia Artificial
#Bank Branches Structure

#Libraries.
import simpy
import random

from simulacion.clases.bank import Bank
from simulacion.clases.client import Client
from simulacion.clases.branch import Bank_Branch
from simulacion.steps_simulation import Steps
from config import BRANCHES, BANK_NAME, TOTAL_STEPS, NUM_CLIENTS_OPTIONS, MIN_SALARY_OPTIONS, MAX_SALARY_OPTIONS

# Generates all posible scenarios of simulation parameters using cartesian product.
# Thes combinations will be used to run different simulation scenarios in a loop.
combinations = []
for num_clients in NUM_CLIENTS_OPTIONS:
    for min_salary in MIN_SALARY_OPTIONS:
        for max_salary in MAX_SALARY_OPTIONS:
            combinations.append((num_clients, min_salary, max_salary))

for num_clients, min_salary, max_salary in combinations:
    if min_salary >= max_salary:
        continue
    
    print(f"\nSimulation with {num_clients} clients with salary between {min_salary} and {max_salary} and Steps: {TOTAL_STEPS}")
    
    # Create and start the simulation:
    env = simpy.Environment()
    branches = [Bank_Branch(env, branch["name"], branch["counters"], branch["loan_interest"], branch["invest_interest"]) for branch in BRANCHES]
    bank = Bank(env, BANK_NAME, branches)
    
    clients = []
    for i in range(num_clients):
        branch = random.choice(bank.branches)
        balance = random.randint(min_salary, max_salary)
        age = random.randint(18, 75)
        client = Client(env, f"Client {i+1}", branch, bank, min_salary, max_salary, balance, age)
        clients.append(client)
        
    simulation = Steps(env = env, bank=bank, total_steps=TOTAL_STEPS, operation_steps=0, clients=clients)
    simulation.run_simulation()
    
    # Exporting the simulation results to the .csv files.
    filename = f"simulation_{num_clients}_{min_salary}_{max_salary}.csv"
    bank.export_simulation_csv(filename = filename)
