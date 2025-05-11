import numpy as np
import matplotlib.pyplot as plt
from data import Delta_List

# Simulation parameters
simulation_duration = 24        # 24 hours
number_of_providers = 10        # Number of developers
peak_hours_Phi = 16.6667        # DSP price φ ($0.00001667 per GB-s) per 100,000 invocations, peak hours (8 AM–8 PM) [1]
off_peak_hours_Phi = 8.333      # DSP price φ ($0.00000833 per GB-s) per 100,000 invocations, off-peak hours (8 PM–8 AM) [1]
static_Phi = 16.6667            # Static price ($0.00001667 per GB-s) per 100,000 invocations [1]
Mu = 6                          # Marginal cost μ per 100,000 invocations [30]
Lambda_u = 800                  # λ_u: Client utility parameter per developer [33]

# Smith and Lee (2024) adaptive pricing parameters [6]
adaptive_min_Phi = 12           # Minimum price ($0.000012 per GB-s) per 100,000 invocations
adaptive_max_Phi = 20           # Maximum price ($0.000020 per GB-s) per 100,000 invocations

# Define utility functions (from existing scripts)
def client_utility(Delta_u, Lambda_u, Phi):
    # λ_u * log(1 + δ_u) - δ_u * φ
    return Lambda_u * np.log(1 + Delta_u) - (Delta_u * Phi)

def provider_utility(Phi, Lambda_List, Mu):
    # sum((λ_u / φ) - 1) * (φ - μ)
    Q = np.sum([max((Lambda_u / Phi) - 1, 0) for Lambda_u in Lambda_List])
    return (Phi - Mu) * Q

# Adaptive pricing model (simplified linear regression approximation of Smith and Lee [6])
def adaptive_price(hour, Delta_List):
    # Predict price based on previous hour's total invocations
    if hour == 0:
        return (adaptive_min_Phi + adaptive_max_Phi) / 2  # Initial price: midpoint
    prev_invocations = sum(Delta_List[hour-1])  # Total δ_u for previous hour
    # Linear mapping: min_invocations=700 (10*70), max_invocations=1000 (10*100)
    normalized = (prev_invocations - 700) / (1000 - 700)
    price = adaptive_min_Phi + normalized * (adaptive_max_Phi - adaptive_min_Phi)
    return max(min(price, adaptive_max_Phi), adaptive_min_Phi)

# Simulation
Lambda_List = np.full(number_of_providers, Lambda_u)  # Uniform λ_u for all developers
resource_utilization_dsp = []
resource_utilization_adaptive = []
provider_utility_dsp = []
provider_utility_adaptive = []
client_cost_dsp = []
client_cost_adaptive = []
client_cost_static = []

for hour in range(simulation_duration):
    # DSP pricing
    Phi_dsp = peak_hours_Phi if 8 <= hour < 20 else off_peak_hours_Phi
    # Adaptive pricing (Smith and Lee [6])
    Phi_adaptive = adaptive_price(hour, Delta_List)
    # Static pricing
    Phi_static = static_Phi

    hour_utilization_dsp = 0
    hour_utilization_adaptive = 0
    hour_cost_dsp = 0
    hour_cost_adaptive = 0
    hour_cost_static = 0

    for provider in range(number_of_providers):
        Delta_u = Delta_List[hour][provider]  # δ_u from Azure trace [33]

        # DSP model
        utility_dsp = client_utility(Delta_u, Lambda_List[provider], Phi_dsp)
        if utility_dsp > 0 and Delta_u > 0:
            hour_utilization_dsp += Delta_u
            hour_cost_dsp += Delta_u * Phi_dsp

        # Adaptive model
        utility_adaptive = client_utility(Delta_u, Lambda_List[provider], Phi_adaptive)
        if utility_adaptive > 0 and Delta_u > 0:
            hour_utilization_adaptive += Delta_u
            hour_cost_adaptive += Delta_u * Phi_adaptive

        # Static model
        hour_cost_static += Delta_u * Phi_static

    resource_utilization_dsp.append(hour_utilization_dsp)
    resource_utilization_adaptive.append(hour_utilization_adaptive)
    provider_utility_dsp.append(provider_utility(Phi_dsp, Lambda_List, Mu))
    provider_utility_adaptive.append(provider_utility(Phi_adaptive, Lambda_List, Mu))
    client_cost_dsp.append(hour_cost_dsp / number_of_providers)
    client_cost_adaptive.append(hour_cost_adaptive / number_of_providers)
    client_cost_static.append(hour_cost_static / number_of_providers)

# Calculate total costs and savings
total_cost_dsp = sum(client_cost_dsp) * number_of_providers
total_cost_adaptive = sum(client_cost_adaptive) * number_of_providers
total_cost_static = sum(client_cost_static) * number_of_providers

cost_savings_dsp = (total_cost_static - total_cost_dsp) / total_cost_static * 100
cost_savings_adaptive = (total_cost_static - total_cost_adaptive) / total_cost_static * 100

# Print results
print(f"DSP Cost Savings: {cost_savings_dsp:.2f}%")
print(f"Adaptive Pricing [6] Cost Savings: {cost_savings_adaptive:.2f}%")
print(f"DSP Provider Utility: {sum(provider_utility_dsp):.2f}")
print(f"Adaptive Provider Utility: {sum(provider_utility_adaptive):.2f}")

# Plot results
plt.figure(figsize=(12, 8))

# Resource Utilization
plt.subplot(2, 2, 1)
plt.plot(resource_utilization_dsp, marker='x', label='DSP')
plt.plot(resource_utilization_adaptive, marker='s', label='Adaptive [6]')
plt.title('A. Resource Utilization')
plt.xlabel('Hour')
plt.ylabel('Number of Functions (δ)')
plt.legend()

# Provider Utility
plt.subplot(2, 2, 2)
plt.plot(provider_utility_dsp, marker='x', label='DSP')
plt.plot(provider_utility_adaptive, marker='s', label='Adaptive [6]')
plt.title('B. Provider Utility')
plt.xlabel('Hour')
plt.ylabel('Utility Function (θ)')
plt.legend()

# Client Cost
plt.subplot(2, 2, 3)
plt.plot(client_cost_dsp, marker='x', label='DSP')
plt.plot(client_cost_adaptive, marker='s', label='Adaptive [6]')
plt.plot(client_cost_static, marker='o', label='Static')
plt.title('C. Average Developer Cost')
plt.xlabel('Hour')
plt.ylabel('Cost ($)')
plt.legend()

# Total Cost Savings
plt.subplot(2, 2, 4)
labels = ['DSP', 'Adaptive [6]']
savings = [cost_savings_dsp, cost_savings_adaptive]
plt.bar(labels, savings)
plt.title('D. Total Cost Savings')
plt.ylabel('Savings (%)')

plt.tight_layout()
plt.savefig('dsp_vs_adaptive_comparison.png')
plt.show()
