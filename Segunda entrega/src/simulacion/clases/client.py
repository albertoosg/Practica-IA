#José Emparanza, Alberto Sainz y Santiago Norzagaray
#CUNEF Universidad
#Inteligencia Artificial
#Bank Branches Structure

#Libraries.
import random
import simpy
from .bank import Bank
from .branch import Bank_Branch
from simulacion.fuzzy_risk import evaluate_risk

#Class representing clients of the bank.
class Client:
    def __init__(self, env: simpy.Environment, name: str, branch: Bank_Branch, bank: Bank, min_salary: int, max_salary: int, initial_money: int, age: int)-> None:
        """Represents a visit of the client to the bank.

        Args:
            env (simpy.Environment): Simulation environment.
            name (str): The name of th client.
            branch (Bank_Branch): The branch destinated to each client.
            money (int): The money each client has.
            min_salary (int): The minimum salary the clients will have.
            max_salary (int): The maximum salary the clients will have.
            initial_money (int): The initial money clients have.
            age (int): The age that clients have.
        """
        self.env = env
        self.name = name
        self.branch = branch
        self.money = initial_money
        self.bank = bank
        self.min_salary = min_salary
        self.max_salary = max_salary
        self.age = age
        self.active_loans = []
        self.active_investments = []
    
    #Simulates the customer's visit to the bank branch.    
    def perform_random_operation(self, current_step = 0):
        
        operation = random.choice(["deposit", "retire", "invest", "loan"])
        quantity = random.randint(self.min_salary, self.max_salary)
        
        # We put the risk_value only on the invest and loan operations.
        if operation in ["invest", "loan"] and quantity > 0 and self.money > 0:
            risk_val = evaluate_risk(self.age, self.money, quantity)
        else:
            risk_val = None
        
        
        arrival = self.env.now
        with self.branch.counters.request() as turno:
            yield turno #Wait his turn to be served.
            start = self.env.now
            waiting_time = start - arrival
            print(f"{self.name} is being attended to at {self.branch.name} at {start:.2f} time units. (Time waiting {waiting_time:.2f} time units).")
                            
            yield self.env.timeout(0.5 + random.uniform(0.5, 1.5))
                
            if operation == "deposit":
                self.deposit(quantity)
                self.branch.total_clients += 1
            elif operation == "retire":
                self.retire(quantity)
                self.branch.total_clients += 1
            elif operation == "invest":
                self.invest(quantity)
                self.branch.total_clients += 1
            elif operation == "loan":
                self.request_loan(quantity)
                self.branch.total_clients += 1
                
            self.bank.historial.append((self.name, self.branch.name, round(arrival, 2), round(start, 2), round(waiting_time, 2),
                                        operation.capitalize(), quantity, current_step + 1, round(self.money, 2), round(risk_val, 2) if risk_val is not None else None))
           
            print(f"{self.name} finishes operation {operation} at {self.env.now:.2f} time units in step {current_step + 1}. Current balance: {self.money:.2f}€")
                
            
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
        """With loan function clients can apply for a loan with risks.

        Args:
            cantidad (int): The quantity of money a client asks for a loan.
        """
        try:
            risk_val = evaluate_risk(self.age, self.money, cantidad)
            print(f"{self.name} has a risk value of {risk_val: .2f} for a loan of {cantidad}€")
            
            if cantidad <= 0:
                print(f"Invalid loan amount requested: {cantidad}€")
                return
                
            if risk_val > 85: 
                print(f"{self.name} has a high risk value. Loan request denied.")
                return
                
            interest_loan = self.branch.loan_interest
            loan_payment = cantidad * (1 + interest_loan)
            
            steps_remaining = self.bank.total_steps - self.bank.current_steps
            if steps_remaining <= 0:
                print(f"{self.name} cannot get a loan at the last step of the simulation")
                return
            payment_per_step = loan_payment / steps_remaining
            self.money += cantidad
            self.active_loans.append((payment_per_step, steps_remaining))
            self.branch.total_borrowed += float(cantidad)  # Asegurar que sea float
            
            print(f"{self.name} apply for a loan of {cantidad}€. The amount they will have to pay back {loan_payment: .2f}")
            print(f"Will pay {payment_per_step:.2f}€ per step for {steps_remaining} steps.Current balance: {self.money}€")
        except Exception as e:
            print(f"Error processing loan request: {e}")
        
           
    def invest(self, cantidad: int):
        """With invest function, clients can invest money with some risks.

        Args:
            cantidad (int): The quantity of money a client wants to invest.
        """
        try:
            if cantidad <= 0:
                print(f"Invalid investment amount: {cantidad}€")
                return
                
            risk_val = evaluate_risk(self.age, self.money, cantidad)
            print(f"{self.name} has a risk value of {risk_val: .2f}% for an investment of {cantidad}€")
            
            if risk_val > 85:  
                print(f"{self.name} has a high risk value. Investment request denied.")
                return       
 
            if self.money >= cantidad: # They quantity they invest has to be smaller or equal to the amount of money they have.
                self.money -= cantidad
                interest_invest = self.branch.invest_interest
                investment_return = cantidad * (1 + interest_invest)
                
                steps_remaining = self.bank.total_steps - self.bank.current_steps
                if steps_remaining <= 0:
                    self.money += investment_return
                    self.branch.total_invested += float(cantidad)  # Asegurar que sea float
                    
                    print(f"{self.name} invests {cantidad}€ and inmediatly receives {investment_return:.2f}€")
                    return
                return_per_step = investment_return / steps_remaining
                self.active_investments.append((return_per_step, steps_remaining))
                self.branch.total_invested += float(cantidad)  # Asegurar que sea float
                print(f"{self.name} invest {cantidad}€. The amount they will get back is {investment_return:.2f}€")
                print(f"Will receive {return_per_step:.2f}€ per step for {steps_remaining} steps. Current balance: {self.money:.2f}€")
            else:
                print(f"{self.name} cant invest {cantidad}€, insufficient balance.")
        except Exception as e:
            print(f"Error processing investment: {e}")
            
    def process_step_payments(self):
        """With this function we calculate the payments and the returns clients have to make or receive in each step (loans and investments).

        """
        remaining_loans = []
        total_loan_payment = 0
        
        for payment_per_step, steps_remaining in self.active_loans:
            self.money -= payment_per_step
            total_loan_payment += payment_per_step
            
            if steps_remaining > 1:
                remaining_loans.append((payment_per_step, steps_remaining - 1))
        
        if total_loan_payment > 0:
            print(f"{self.name} pays {total_loan_payment:.2f}€ for active loans this step.")
        self.active_loans = remaining_loans
        
        remaining_investments = []
        total_investment_return = 0
        
        for return_per_step, steps_remaining in self.active_investments:
            self.money += return_per_step
            total_investment_return += return_per_step
            
            if steps_remaining > 1:
                remaining_investments.append((return_per_step, steps_remaining - 1))
                
        if total_investment_return > 0:
            print(f"{self.name} receives {total_investment_return:.2f}€ from active investments this step.")
        
        self.active_investments = remaining_investments
        if self.money < 0:
            print(f"WARNING: {self.name} has negative balance: {self.money: .2f}€")