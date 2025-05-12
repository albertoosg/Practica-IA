import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Define the fuzzy input variable 'age', from 18 to 75.
age = ctrl.Antecedent(np.arange(18, 76, 1), 'edad')
# Define the fuzzy input variable 'saldo', from 0 to 5000.
saldo = ctrl.Antecedent(np.arange(0, 5001, 1), 'saldo')  
# Define the fuzzy input variable 'quantity', from 0 to 5000.
quantity = ctrl.Antecedent(np.arange(0, 5001, 1), 'quantity')  
#Define the fuzzy output variable 'risk', from 0 to 100.
risk = ctrl.Consequent(np.arange(0, 101, 1), 'risk')

# Four categories for age. 
#Define membership functions for 'age' using triangular fuzzy sets:
age['muy joven'] = fuzz.trimf(age.universe, [18, 18, 30])
age['joven'] = fuzz.trimf(age.universe, [25, 35, 45])
age['adulto'] = fuzz.trimf(age.universe, [40, 50, 60])
age['mayor'] = fuzz.trimf(age.universe, [55, 75, 75])

# Four categories for saldo.
#Define membership functions for 'saldo' using triangular fuzzy sets:
saldo['muy bajo'] = fuzz.trimf(saldo.universe, [0, 0, 1000])
saldo['bajo'] = fuzz.trimf(saldo.universe, [800, 1500, 2200])
saldo['medio'] = fuzz.trimf(saldo.universe, [2000, 3000, 4000])
saldo['alto'] = fuzz.trimf(saldo.universe, [3500, 5000, 5000])

# Four categories for quantity.
#Define membership functions for 'quantity' using triangular fuzzy sets:
quantity['muy pequeña'] = fuzz.trimf(quantity.universe, [0, 0, 1000])
quantity['pequeña'] = fuzz.trimf(quantity.universe, [800, 1500, 2200])
quantity['media'] = fuzz.trimf(quantity.universe, [2000, 3000, 4000])
quantity['grande'] = fuzz.trimf(quantity.universe, [3500, 5000, 5000])

# Risk range.
risk['bajo'] = fuzz.trimf(risk.universe, [0, 0, 45])
risk['medio'] = fuzz.trimf(risk.universe, [35, 55, 75])
risk['alto'] = fuzz.trimf(risk.universe, [65, 100, 100])

# The rules of the simulations.
rule1  = ctrl.Rule(age['muy joven'] & saldo['muy bajo'] & quantity['muy pequeña'], risk['alto'])
rule2  = ctrl.Rule(age['muy joven'] & saldo['muy bajo'] & quantity['grande'], risk['medio'])
rule3  = ctrl.Rule(age['muy joven'] & saldo['medio'] & quantity['media'], risk['medio'])
rule4  = ctrl.Rule(age['muy joven'] & saldo['alto'] & quantity['grande'], risk['bajo'])

rule5  = ctrl.Rule(age['joven'] & saldo['muy bajo'] & quantity['muy pequeña'], risk['alto'])
rule6  = ctrl.Rule(age['joven'] & saldo['muy bajo'] & quantity['grande'], risk['medio'])
rule7  = ctrl.Rule(age['joven'] & saldo['bajo'] & quantity['grande'], risk['medio'])
rule8  = ctrl.Rule(age['joven'] & saldo['medio'] & quantity['grande'], risk['bajo'])
rule9  = ctrl.Rule(age['joven'] & saldo['alto'] & quantity['media'], risk['bajo'])

rule10 = ctrl.Rule(age['adulto'] & saldo['muy bajo'] & quantity['muy pequeña'], risk['alto'])
rule11 = ctrl.Rule(age['adulto'] & saldo['muy bajo'] & quantity['media'], risk['medio'])
rule12 = ctrl.Rule(age['adulto'] & saldo['bajo'] & quantity['grande'], risk['bajo'])
rule13 = ctrl.Rule(age['adulto'] & saldo['medio'] & quantity['media'], risk['medio'])
rule14 = ctrl.Rule(age['adulto'] & saldo['alto'] & quantity['media'], risk['bajo'])

rule15 = ctrl.Rule(age['mayor'] & saldo['muy bajo'] & quantity['muy pequeña'], risk['alto'])
rule16 = ctrl.Rule(age['mayor'] & saldo['muy bajo'] & quantity['media'], risk['medio'])
rule17 = ctrl.Rule(age['mayor'] & saldo['bajo'] & quantity['media'], risk['bajo'])
rule18 = ctrl.Rule(age['mayor'] & saldo['medio'] & quantity['pequeña'], risk['medio'])
rule19 = ctrl.Rule(age['mayor'] & saldo['medio'] & quantity['grande'], risk['bajo'])
rule20 = ctrl.Rule(age['mayor'] & saldo['alto'] & quantity['grande'], risk['bajo'])

rule21 = ctrl.Rule(age['muy joven'] & saldo['bajo']  & quantity['muy pequeña'], risk['alto'])
rule22 = ctrl.Rule(age['joven'] & saldo['bajo']  & quantity['media'], risk['medio'])
rule23 = ctrl.Rule(age['adulto'] & saldo['medio'] & quantity['pequeña'], risk['medio'])
rule24 = ctrl.Rule(age['mayor'] & saldo['alto']  & quantity['muy pequeña'], risk['medio'])

risk_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8,
                               rule9, rule10, rule11, rule12, rule13, rule14, rule15, rule16,
                               rule17, rule18, rule19, rule20, rule21, rule22, rule23, rule24])


def evaluate_risk(val_age, val_saldo, val_quantity):
    """Evaluates the risk of operations depending on age, saldo and quantity.

    Args:
        val_age (_type_): Evaluate the age.
        val_saldo (_type_): Evaluate the saldo.
        val_quantity (_type_): Evaluate the quantity.

    """
    
    try:
        # Limitar los valores a los rangos definidos
        val_age = min(max(val_age, 18), 75)
        val_saldo = min(max(val_saldo, 0), 5000)
        val_quantity = min(max(val_quantity, 0), 5000)
        
        risk_simulator = ctrl.ControlSystemSimulation(risk_ctrl)
        risk_simulator.input['edad'] = val_age
        risk_simulator.input['saldo'] = val_saldo
        risk_simulator.input['quantity'] = val_quantity
        risk_simulator.compute()
        
        if 'risk' in risk_simulator.output:
            return risk_simulator.output['risk']
        else:
            print("No se activo ninguna regla para edad = {val_age}, saldo = {val_saldo}, cantidad = {val_quantity} ")
            return 100
        
    except Exception as e:
        print(f"[RISK ERROR] edad = {val_age}, saldo = {val_saldo}, cantidad = {val_quantity} -> {e}")
        return 100  # Valor alto de riesgo por defecto en caso de error

