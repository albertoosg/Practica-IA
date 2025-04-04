#José Emparanza, Alberto Sainz y Santiago Norzagaray
#CUNEF Universidad
#Inteligencia Artificial
#Bank Branches Structure

#Libraries.
import simpy
import random

from branch_bank import Bank
from branch_client import Client
from branch import Bank_Branch
 
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
        


if __name__ =='__main__':    
    """Main entry point to run the bank simulation.
    """     
    env = simpy.Environment()
    branch1 = Bank_Branch(env, "Bank Branch A", 2)
    branch2 = Bank_Branch(env, "Bank Branch B", 2)
    branch3 = Bank_Branch(env, "Bank Branch C", 2)
    bank = Bank(env, "Bank Central", [branch1, branch2, branch3])
    
    while True:
        try:
            clients = int(input("¿How many clients do you want for this simulation? "))
            min_salary = int(input("Put the minimum amount that clients will have: "))
            max_salary = int(input("Put the maximum amount that clients will have: "))
            
            if clients <= 0 or min_salary < 0 or max_salary < 0:
                print("Please put positive values. Thank you.")
                continue
            if min_salary > max_salary:
                print("The min_salary cant be bigger than the max_salary.")
                continue
            break
        except ValueError:
            print("Error. Please enter integers.")
            
    print("\nInitial balance for each client:")
    initial_money= []
    initial_balances = {}
    for i in range(clients):
        balance = random.randint(min_salary, max_salary)
        initial_money.append(balance)
        initial_balances[f"Client {i+1}"] = balance
        print(f"Client {i+1}: {balance}€")
    print("\nStarting simulation...\n") 

    #Run the simulation.
    env.process(generate_client(env, bank, clients, min_salary, max_salary, initial_money))
    env.run()

    #Summary from each bank branch.
    for branch in bank.branches:
        print(f"\nSummary of {branch.name}: ")
        print(f"Attended clients: {branch.total_clients}")
        print(f"Total amount lent by the bank branch: {branch.total_borrowed}€")
        print(f"Total amount invested by the clients: {branch.total_invested}€")
    
    #Total summary of the bank.
    bank.general_summmary() 
    
    #Export the information to the csv file.
    bank.export_simulation_csv()
