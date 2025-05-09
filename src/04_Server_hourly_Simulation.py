import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from data import Delta_List

# Simulation parameters
simulation_duration = 24        # 24 hours
number_of_providers = 10        # Number of clients
peak_hours_Phi = 16.6667        # for floating point numbers we assumed 0.00001667 GB-S for  100,000 function calls
off_peak_hours_Phi = 8.333      # for  100,000 function calls
Lambda = 800

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

def sum_provider_utility(Mu_Grid, Hours_Grid):
    um_len = len(um_values)
    hour_len = len(hours)
    utility_values = np.zeros((hour_len, um_len))
   
    for i in range(hour_len):
        for j in range(um_len):
            utility_values[i, j] = sum_provider_utility_for_hour( Mu_Grid[i,j] , Hours_Grid[i,j])
    #print(utility_values)        
    return utility_values
    
def sum_clients_utility(Mu_Grid, Hours_Grid):
    um_len = len(um_values)
    hour_len = len(hours)
    utility_values = np.zeros((hour_len, um_len))
   
    for i in range(hour_len):
        for j in range(um_len):
            utility_values[i, j] = sum_clients_utility_for_hour( Mu_Grid[i,j] , Hours_Grid[i,j])
    #print(utility_values)        
    return utility_values    

def sum_provider_utility_for_hour(Mu, hour):
    s_utility = 0 
    Lambda_List = np.full(number_of_providers ,Lambda )
    
    if 8 <= hour < 20:
        Phi = peak_hours_Phi
    else:
        Phi = off_peak_hours_Phi
    utility =  provider_utility(Phi, Lambda_List, Mu)
    
    if utility>0 :
        s_utility += utility
    #print("Mu=" , Mu , ",Lambda =" ,Lambda , "s_utility" , s_utility)        
    return s_utility;
    
def sum_clients_utility_for_hour(Mu, hour):
    s_utility = 0 
    
    
    if 8 <= hour < 20:
       Phi = peak_hours_Phi
    else:
       Phi = off_peak_hours_Phi
    for provider in range(number_of_providers):
       #δ_u
        Delta_u = ((Delta_List[hour])[provider]) 
        #Delta_u, Lambda_u, Phi    
        utility =  client_utility(Delta_u, Lambda, Phi)
        #print(utility)
        if utility>0 and Delta_u > 0:
                s_utility += utility
    #print("Mu=" , Mu , ",Lambda =" ,Lambda , "s_utility" , s_utility)        
    return s_utility;
    


um_values = np.arange(6, 8.2, 0.2)

hours = np.arange(24)

#print (hours)

Mu_Grid, Hours_Grid = np.meshgrid(um_values, hours)


provider_results = sum_provider_utility(Mu_Grid, Hours_Grid)

clients_results = sum_clients_utility(Mu_Grid, Hours_Grid)

#plot 

fig = plt.figure(figsize=(12, 5))

#provider plot

ax1 = fig.add_subplot(121, projection='3d')

ax1.plot_surface(Mu_Grid, Hours_Grid, provider_results, cmap='viridis' )

ax1.set_xlabel('μ')
ax1.set_ylabel('hour')
ax1.set_zlabel('θ')

#client plot
ax2 = fig.add_subplot(122, projection='3d')
ax2.plot_surface(Mu_Grid, Hours_Grid, clients_results, cmap='viridis' ,label='Developers utility function')

ax2.set_xlabel('μ')
ax2.set_ylabel('hour')
ax2.set_zlabel('θ')
ax1.set_title('Serverless Provider Utility (Azure Functions 2021 Trace)')
ax2.set_title('Developers Utility Function (Azure Functions 2021 Trace)')
plt.tight_layout()




plt.show()
