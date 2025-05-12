import random
import simpy
from .bank import Bank
from .client import Client


#Continuous costumer/client generator.   
def generate_client(env, bank: Bank, clients: int, min_salary: int, max_salary: int, initial_money):
    """
    Generates clients that arrive to the bank during the simulation time.

    Args:
        env (simpy.Environmnent): Simulation environment.
        bank (Bank): Bank instance with branches.
        clients (int): The number of clients that are going to be involved in the simulation.
        min_salary (int): The minimum salary the clients will have.
        max_salary (int): The maximum salary the clients will have.

    """
    
    for i in range(clients):
        yield env.timeout(random.uniform(0.0, 2.0))
        branch = bank.assign_branch()
        Client(env, f"Client {i+1}", branch, bank, min_salary, max_salary, initial_money[i])
   