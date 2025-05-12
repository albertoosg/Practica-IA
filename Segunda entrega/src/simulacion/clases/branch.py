#José Emparanza, Alberto Sainz y Santiago Norzagaray
#CUNEF Universidad
#Inteligencia Artificial
#Bank Branches Structure

#Libraries
import simpy

#Class representing the bank branches.
class Bank_Branch:
    def __init__(self, env: simpy.Environment, name: str, num_counters: int, loan_interest: float, invest_interest: float) -> None:
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
        self.counters = simpy.Resource(env, capacity = num_counters) #Counters available.
        self.loan_interest = loan_interest
        self.invest_interest = invest_interest
        # Inicializar contadores en 0
        self.total_clients = 0
        self.total_borrowed = 0.0
        self.total_invested = 0.0