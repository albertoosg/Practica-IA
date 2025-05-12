#José Emparanza, Alberto Sainz y Santiago Norzagaray
#CUNEF Universidad
#Inteligencia Artificial
#Bank Branches Structure

#Libraries
import random
import csv
import simpy
from typing import List
from .branch import Bank_Branch

#Class representing the bank with multiple branches.
class Bank:
    """Represents a bank with multiple branches.
    """
    def __init__(self, env: simpy.Environment, name: str, branches: List[Bank_Branch]) -> None:
        """Initializes the bank with branches defined by its capabiliities.

        Args:
            env (simpy.Environment): Simulation environment.
            name (str): The name of the bank.
            branches (List[Bank_Branch]): The quantity of branches the bank has.
            historial (List[]): Stores full history of all operations carried out during the simulation.
        """
        self.env = env
        self.name = name
        self.branches = branches 
        self.historial = []
        
    def assign_branch(self) -> Bank_Branch:
        """Selects a branch randomly to each client.

        Returns
            Bank_Branch: Branch selected.
        """
        return random.choice(self.branches) 
        
    def best_invest_loan_condition(self):
        best_branch_loan = min(self.branches, key = lambda i : i.loan_interest)
        best_branch_invest = max(self.branches, key = lambda i: i.invest_interest)
        
        print(f"\nBest Branch Conditions Summary:")
        print(f"Best loan conditions: {best_branch_loan.name} with {best_branch_loan.loan_interest*100:.2f}%")
        print(f"Best invest conditions: {best_branch_invest.name} with {best_branch_invest.invest_interest*100:.2f}%")
     
    #Function used to export the data from the simulation.   
    def export_simulation_csv(self, filename: str = "simulation.csv"):
        import os
        #We use project_root to save the results in the data_analisys folder (it's out of the src folder).
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")) 
        data_folder = os.path.join(project_root, "data_analisys")
        os.makedirs(data_folder, exist_ok=True)
        file_path = os.path.join(data_folder, filename)
        with open(file_path, mode = 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Clients", "Branch", "Arrival", "Start", "Waitint Time", "Operation", "Quantity", "Step", "Balance", "Risk"])
            for i in self.historial:
                writer.writerow(i)
        print(f"Simulation data exported to {file_path}")
        