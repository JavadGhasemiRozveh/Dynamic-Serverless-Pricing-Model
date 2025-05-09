#Use Python 3.12 
#pip install numpy
#pip install matplotlib
#pip install scipy




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


# Pricing: peak_hours_Phi = 16.6667 and off_peak_hours_Phi = 8.333 per 100,000 invocations, scaled from AWS Lambda's $0.00001667 per GB-s
# Simulation parameters
simulation_duration = 24        # 24 hours
number_of_providers = 10        # Number of clients
peak_hours_Phi = 16.6667        # for floating point numbers we assumed 0.00001667 GB-S for  100,000 function calls
off_peak_hours_Phi = 8.333      # for  100,000 function calls
Mu = 6                          # Marginal cost for the provider for  100,000 function calls



cost_saving_plt=[]
Lambda_plt=[]
# Simulation
for Lambda_w in range(10):

    # Initialize lists and variabels 
    resource_utilization = []
    client_count=[]
    provider_utility_list = []
    client_utility_list = []
    cost_static_array = []
    cost_dynamic_array = []
    total_cost_static = 0
    total_cost_dynamic = 0

    Lambda_List = np.full(number_of_providers ,Lambda_w * 100 )  # Utility parameters for each client    
    print( Lambda_List)
    for hour in range(simulation_duration):
        if 8 <= hour < 20:
            Phi = peak_hours_Phi
        else:
            Phi = off_peak_hours_Phi
        #print( hour , "," , Phi)
        hour_utilization = 0
        hour_client_count = 0
        hour_static_cost = 0
        hour_dynamic_cost = 0 
        sum_client_utility=0
        i= 0
        for provider in range(number_of_providers):
            #δ_u
            Delta_u = ((Delta_List[hour])[i]) 

            this_client_utility = client_utility(Delta_u, Lambda_List[i], Phi)
            if this_client_utility >0 and Delta_u > 0:
                cost_static = Delta_u * peak_hours_Phi
                cost_dynamic = Delta_u * Phi
                
                hour_utilization += Delta_u
                hour_client_count += 1
                total_cost_static += cost_static
                total_cost_dynamic += cost_dynamic

                hour_static_cost += cost_static
                hour_dynamic_cost += cost_dynamic
                sum_client_utility += this_client_utility
                
            i += 1
            
        resource_utilization.append(hour_utilization)
        client_count.append(hour_client_count)
        if hour_utilization > 0 :
            provider_utility_list.append(provider_utility(Phi, Lambda_List, Mu))
        else :
            provider_utility_list.append(0)
        client_utility_list.append(sum_client_utility / number_of_providers)
        cost_static_array.append(hour_static_cost / number_of_providers)
        cost_dynamic_array.append(hour_dynamic_cost / number_of_providers)

    # Results
    if total_cost_static >0 :
        
        cost_savings = (total_cost_static - total_cost_dynamic) / total_cost_static * 100
        print ("Lambda =" ,Lambda_List[0], ",cost_savings=", cost_savings)
        cost_saving_plt.append(cost_savings)
        Lambda_plt.append(Lambda_List[0]) 
        
        plt.figure(figsize=(10, 6))
        
        plt.subplot(2, 2, 1)
        plt.plot(resource_utilization,marker='x', label='Resource used')
        
        plt.title(f"A. Resource Utilization λ={Lambda_List[0]} (Azure Functions 2021 Trace)")
        
        plt.xlabel('Hour')
        plt.ylabel('Number of functions (δ) ')
        plt.legend()
        
        

        plt.subplot(2, 2, 2)
        plt.plot(provider_utility_list,marker='x', label='Serverless Provider')
        plt.plot(client_utility_list,marker='s', label='Developer')
        plt.title('B.Utiltiy functions  ')
        plt.xlabel('Hour')
        plt.ylabel('Utiltiy function (θ)  ')
        plt.legend()
        


        plt.subplot(2, 2, 3)
        plt.plot(cost_static_array,marker='x', label='Static Pricing')
        plt.plot(cost_dynamic_array,marker='s', label='DSP Pricing')
        plt.title('C.cost ')
        plt.xlabel('Hour')
        plt.ylabel('Cost  ($)')
        plt.legend()
        
        
        plt.subplot(2, 2, 4)
        labels = ['Static', 'DSP']
        costs = [total_cost_static, total_cost_dynamic]
        plt.bar(labels ,costs )
        plt.title('D.Total cost saving')
        plt.ylabel('Total Cost ($)')
        

        plt.tight_layout()
        plt.show()
    else :
        cost_saving_plt.append(0)
        Lambda_plt.append(Lambda_List[0]) 
        print("Developer utility was negative")


plt.plot(Lambda_plt, cost_saving_plt ,marker='x', label='Cost saving by λ')
plt.xlabel('λ')
plt.ylabel('Total cost save%')

plt.xticks(Lambda_plt)

plt.show()
