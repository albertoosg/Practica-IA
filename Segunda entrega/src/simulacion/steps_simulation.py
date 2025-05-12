import random
import simpy
import simpy.events
from .clases.bank import Bank

class Steps:
    
    def __init__(self, env: simpy.Environment, bank: Bank, total_steps, operation_steps, clients) -> None:
        """this class creates the steps of the simulations.

        Args:
            env (simpy.Environment): Simulation environment.
            bank (Bank): Class Bank from bank
            total_steps (_type_): Amount of steps in each simulation.
            clients (_type_): The clients of the simulations
        """
        self.env = env
        self.bank = bank
        self.clients = clients
        self.total_steps = total_steps
        self.current_step = 0
        
        self.bank.total_steps = total_steps
        self.bank.current_steps = 0
        
        self.min_operations = max(1,round(len(clients) * 0.75))
        self.max_operations = len(clients) * 3
        
    def run_steps(self):
        """This function runs the steps of the simulation.
        """
        if self.current_step >= self.total_steps:
            print(f"Simulation completed.")
            return False
            
        self.bank.current_steps = self.current_step
        
        # The number of operations each step will make.
        operations_this_step = random.randint(self.min_operations, self.max_operations)
        
        print(f"\n--- STEP {self.current_step + 1} of {self.total_steps} ---")
        print(f"Performing {operations_this_step} operations this step (Client count: {len(self.clients)}).")
        
        for client in self.clients:
            client.process_step_payments()
            
        operations_pool = []
        for _ in range(operations_this_step):
            client = random.choice(self.clients)
            operations_pool.append(client)
            
        processes = []
        for client in operations_pool:
            process = self.env.process(client.perform_random_operation(self.current_step))
            processes.append(process)
          
        # We use AllOf to wait for all processes to finish before moving to the next step.
        self.env.run(until=simpy.events.AllOf(self.env, processes))
        self.current_step += 1
        return True
    
    def run_simulation(self):
        """This function runs the simulation and shows all the summaries of branches and bank.
        """
        
        while self.run_steps():
            pass
                   
        total_bank_loans = 0.0
        total_bank_investments = 0.0
        total_bank_clients = 0
        
        for branch in self.bank.branches:
            total_bank_loans += float(branch.total_borrowed)
            total_bank_investments += float(branch.total_invested)
            total_bank_clients += branch.total_clients
            
            print(f"\nSummary of {branch.name}:")
            print(f"Attended clients: {branch.total_clients}")
            print(f"Total amount lent by the branch: {branch.total_borrowed:.2f}€")
            print(f"Total amount invested by the clients: {branch.total_invested:.2f}€")
            print(f"Interest for loans: {branch.loan_interest*100:.2f}%")
            print(f"Interest for investments: {branch.invest_interest*100:.2f}%")
        
        print(f"\nGENERAL BANK SUMMARY:")
        print(f"Total clients attended: {total_bank_clients}")
        print(f"Total amount lent: {total_bank_loans:.2f}€")
        print(f"Total amount invested: {total_bank_investments:.2f}€")
        
        self.bank.best_invest_loan_condition()
