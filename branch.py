#José Emparanza, Alberto Sainz y Santiago Norzagaray
#CUNEF Universidad
#Inteligencia Artificial
#Bank Branches Structure

#Libraries
import simpy

#Class representing the bank branches.
class Bank_Branch:
    def __init__(self, env: simpy.Environment, name: str, volume: int):
        """Represents a bank branch.

        Args:
            env (simpy.Environment): Simulation environment.
            name (str): The name of the branch.
            volume (int): The number of counters at every branch.
            counters (simpy.Resource): Simpy resource that represents counters.
            total_clients (int): Total number of clients that enters to the bank.
            total_borrowed(int): Total amount borrowed by the bank.
            total_invested(int): Total amount invested by the clients.
        """
        self.env = env
        self.name = name
        self.counters = simpy.Resource(env, capacity = volume) #Counters available.
        self.total_clients = 0
        self.total_borrowed = 0
        self.total_invested = 0