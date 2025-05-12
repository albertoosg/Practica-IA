#José Emparanza, Alberto Sainz y Santiago Norzagaray
#CUNEF Universidad
#Inteligencia Artificial
#Bank Branches Structure

#Libraries.
import random
import simpy
from .bank import Bank
from .branch import Bank_Branch

#Class representing clients of the bank.
class Client:
    def __init__(self, env: simpy.Environment, name: str, branch: Bank_Branch, bank: Bank, min_salary: int, max_salary: int, initial_money: int)-> None:
        """Represents the visit of a client to the bank.

        Args:
            env (simpy.Environment): Simulation environment.
            name (str): The name of th client.
            branch (Bank_Branch): The branch destinated to each client.
            money (int): The money each client has.
            min_salary (int): The minimum salary the clients will have.
            max_salary (int): The maximum salary the clients will have.
        """
        self.env = env
        self.name = name
        self.branch = branch
        self.money = initial_money
        self.bank = bank
        self.min_salary = min_salary
        self.max_salary = max_salary
        self.env.process(self.visit_branch()) 
    
    #Simulates the customer's visit to the bank branch.    
    def visit_branch(self):
        """
        Customer service process at the bank. Wait your turn and be served.
        """
        arrival = self.env.now
        print(f"{self.name} arrives to {self.branch.name} at {arrival:.2f}")
        with self.branch.counters.request() as turno:
            yield turno #Wait his turn to be served.
            start = self.env.now
            waiting_time = start - arrival
            print(f"{self.name} is being attended to at {self.branch.name} at {start:.2f} time units. (Time waiting {waiting_time:.2f} time units).")
            
            num_operations = random.randint(1, 4)
            for i in range(num_operations):
                operation = random.choice(["deposit", "retire", "invest", "loan"])
                quantity = random.randint(self.min_salary, self.max_salary)
                
                yield self.env.timeout(0.5 + random.uniform(0.5, 1.5))
                
                if operation == "deposit":
                    self.deposit(quantity)
                elif operation == "retire":
                    self.retire(quantity)
                elif operation == "invest":
                    self.invest(quantity)
                elif operation == "loan":
                    self.request_loan(quantity)
                
                self.bank.historial.append((self.name, self.branch.name, round(arrival, 2), round(start, 2), round(waiting_time, 2), operation.capitalize(), quantity))

            self.branch.total_clients += 1            
            print(f"{self.name} finishes his appointment at {self.branch.name} at {self.env.now:.2f} time units")
                
            
    def deposit(self, quantity: int):
        """
        With deposit function clients can deposit their money.
        
        Args:
            quantity (int): The amount of money the client wants to deposit.
        """
        self.money += quantity
        print(f"{self.name} deposit {quantity}€. Current balance: {self.money}€")
        
    
    def retire(self, quantity: int): 
        """
        With retire function clients can retire their money.
        
        Args:
            quantity (int): The amount of money the client wants to retire.
        """
        if self.money >= quantity: # They quantity they retire has to be smaller or equal to the amount of money they have.
            self.money -= quantity
            print(f"{self.name} withdraw {quantity}€. Current balance: {self.money}€")
        else:
            print(f"{self.name} tries to withdraw {quantity}€, but only has {self.money}€")
    
    
    def request_loan(self, cantidad: int):
        """
        With request_loan clients can request a loan to the bank. 

        Args:
            cantidad (int): The amount of money the client wants to request.
        """
        self.money += cantidad
        self.branch.total_borrowed += cantidad
        print(f"{self.name} apply for a loan of {cantidad}€. Current balance: {self.money}€")
    
    
           
    def invest(self, cantidad: int):
        """
        With invest function clients can invest their money. 

        Args:
            cantidad (int): The amount of money the client wants to invest.
        """
        if self.money >= cantidad: # They quantity they invest has to be smaller or equal to the amount of money they have.
            self.money -= cantidad
            self.branch.total_invested += cantidad
            print(f"{self.name} invest {cantidad}€. Current balance: {self.money}€")
        else:
            print(f"{self.name} cant invest {cantidad}€, insufficient balance.")
            