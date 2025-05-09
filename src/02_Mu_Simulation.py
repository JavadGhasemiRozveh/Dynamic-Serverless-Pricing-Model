import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
import sys
from data import Delta_List


# Define utility functions for clients and provider
def client_utility(Delta_u, Lambda_u, Phi):
    # λ_u * log(1+ δ_u ) - δ_u * φ
    result = Lambda_u * np.log(1 + Delta_u) -  (Delta_u * Phi )
    #print("Delta_u=" , Delta_u ,",Lambda_u=" , Lambda_u , ",Phi= " , Phi , ",Lambda_u * np.log(1 + Delta_u)=" ,Lambda_u * np.log(1 + Delta_u) , ",Delta_u * Phi=" , Delta_u * Phi , ",result=" ,  result)
    return result

def provider_utility(Phi, Lambda_List, Mu):
    # sum((λ_u / δ_u) -1) * (φ - μ )
    Q = np.sum([optimal_consumption(Lambda_u, Phi) for Lambda_u in Lambda_List])
    
    return (Phi - Mu) * Q

def optimal_consumption(Lambda_u, Phi):
    #print ("Lambda_u=" , Lambda_u , "Phi = " , Phi)
    # (λ_u / δ_u) -1
    return max((Lambda_u / Phi) - 1, 0)


# Mu ranges from 6 to 16.6667, validated against Azure Functions 2021 Trace invocation patterns
# Simulation parameters
simulation_duration = 24        # 24 hours
number_of_providers = 10        # Number of clients
peak_hours_Phi = 16.6667        # for floating point numbers we assumed 0.00001667 GB-S for  100,000 function calls
off_peak_hours_Phi = 8.333      # for  100,000 function calls
Min_Mu = 6                          # Marginal cost for the provider for  100,000 function calls

Lambda_List = np.full(number_of_providers ,800 )  # Utility parameters for each client    


Mu_list=[]
provider_utility_list = []
# Simulation
for Mu_w in range(11):
    Mu = Min_Mu + (peak_hours_Phi - Min_Mu )/10 * Mu_w 
    Mu_list.append(Mu)
    
    this_hour_utility =0
    print ("*****************************")
    print ( "Mu = ", Mu)
    print ("*****************************")
    for hour in range(simulation_duration):
        if 8 <= hour < 20:
            Phi = peak_hours_Phi
        else:
            Phi = off_peak_hours_Phi
        utility =  provider_utility(Phi, Lambda_List, Mu)
        print("Hour=" , hour , ",utility =" ,utility)
        if utility>0 :
            this_hour_utility += utility
        
    provider_utility_list.append(this_hour_utility);
   
    # Results
   
        
    

plt.plot(Mu_list, provider_utility_list, marker='x', label='Serverless utility function θ (Azure Functions 2021 Trace)')

plt.xlabel('μ')
plt.ylabel('Serverless utility function(θ)')

plt.xticks(Mu_list)
plt.legend()
plt.show()
