#José Emparanza, Alberto Sainz y Santiago Norzagaray
#CUNEF Universidad
#Inteligencia Artificial
#Bank Branches Structure

#Libraries.
import simpy
import random
import itertools

from simulacion.bank import Bank
from simulacion.client import Client
from simulacion.branch import Bank_Branch     
from simulacion.generator import generate_client
from config import BRANCHES, BANK_NAME

num_clients_options = [20, 30]
min_salary_options = [100, 200]
max_salary_options = [3000, 5000]

combinations = list(itertools.product(num_clients_options, min_salary_options, max_salary_options))

for num_clients, min_salary, max_salary in combinations:
    if min_salary >= max_salary:
        continue
    
    print(f"Running simulation: {num_clients} clients, salary between {min_salary} and {max_salary}")
    env = simpy.Environment()
    branches = [Bank_Branch(env, b["name"], b["counters"]) for b in BRANCHES]
    bank = Bank(env, BANK_NAME, branches)
    
    initial_money = [random.randint(min_salary, max_salary) for _ in range(num_clients)]
    env.process(generate_client(env, bank, num_clients, min_salary, max_salary, initial_money))
    env.run()
    
    print(f"Results for {num_clients} clients, salary between {min_salary} and {max_salary}:")
    
    for branch in bank.branches:
        print(f"\nSummary of  {branch.name}:")
        print(f" Attended clients: {branch.total_clients}")
        print(f" Total amount lent by the bank branch: {branch.total_borrowed}€")
        print(f" Total invested by the clients: {branch.total_invested}€")

    bank.general_summmary()
    
    #Guardar en csv
    filename = f"simulation_{num_clients}_{min_salary}_{max_salary}.csv"
    bank.export_simulation_csv(filename = filename)