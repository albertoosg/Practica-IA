#José Emparanza, Alberto Sainz y Santiago Norzagaray
#CUNEF Universidad
#Inteligencia Artificial
#Bank Branches Structure

#Libraries
import random
import csv
import simpy
from typing import List, Tuple
from branch import Bank_Branch

#Class representing the bank with multiple branches.
class Bank:
    """Represents a bank with multiple branches.
    """
    def __init__(self, env: simpy.Environment, name: str, branches: List[Bank_Branch]):
        """Initializes the bank with branches defined by its capabiliities.

        Args:
            env (simpy.Environment): Simulation environment.
            name (str): The name of the bank.
            branches (List[Bank_Branch]): The quantity of branches the bank has.
        """
        self.env = env
        self.name = name
        self.branches = branches 
        self.historial: List[Tuple[str, str, float, float, float, str, float]] = []
        
    def assign_branch(self) -> Bank_Branch:
        """Selects a branch randomly to each client.

        Returns
            Bank_Branch: Branch selected.
        """
        return random.choice(self.branches) 
    
    def general_summmary(self):
        total_clients = sum(s.total_clients for s in self.branches)
        total_borrowed = sum(s.total_borrowed for s in self.branches)
        total_invested = sum(s.total_invested for s in self.branches)
        
        print(f"\nSummary of {self.name}: ")
        print(f"Total clients served: {total_clients}")
        print(f"Total loaned in all branches: {total_borrowed}€")
        print(f"Total invested in all branches: {total_invested}€")
     
    #Function used to export certain information from the simulation.   
    def export_simulation_csv(self, filename: str = "simulation.csv"):
        import os
        data_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data_analisys")
        os.makedirs(data_folder, exist_ok=True)
        file_path = os.path.join(data_folder, filename)
        with open(filename, mode = 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["CLients", "Branch", "Arrival", "Start", "Waitint Time", "Operation", "Quantity"])
            for i in self.historial:
                writer.writerow(i)
        print(f"Simulation data exported to {file_path}")
        