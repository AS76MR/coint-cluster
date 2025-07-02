import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import coint
import time

seed = int(time.time()) % (2**32)
np.random.seed(seed)  

def generate_random_walk(n_steps, initial_value=100):
    """Generate a random walk (non-stationary time series)."""
    returns = np.random.normal(0, 1, n_steps)
    random_series = initial_value + np.cumsum(returns)
    return random_series

def generate_cointegrated_series(base_series, n_series, coint_strength, noise_std ):
    """Generate cointegrated series from a base random walk."""
    n_steps = len(base_series)
    cointegrated_series = []
    for _ in range(n_series):
        # Stationary error term (mean-reverting around base_prices)
        error = np.random.normal(0, noise_std, n_steps)
        error = np.cumsum(error)  
        # Cointegrated series = base_prices + stationary error
        series = base_series + coint_strength * error
        cointegrated_series.append(series)
    return cointegrated_series


n_steps = 1250  # Length of time series
n_coint_groups = 5  # Number of cointegrated groups
n_coint_per_group = 10  # Number of variables per cointegrated group
n_independent = 5  # Number of independent (non-cointegrated) variables
coint_strength=5.0 # strength of cointegration
noise_std=0.01 # stdev of noise


# Generate independent random walks (non-cointegrated variables)
independent_variables = [generate_random_walk(n_steps) for _ in range(n_independent)]
independent_names = [f"Indep_{i}" for i in range(n_independent)]

# Generate cointegrated groups
cointegrated_groups = []
cointegrated_names = []
for group_id in range(n_coint_groups):
    base_tume_series = generate_random_walk(n_steps)
    group_series = generate_cointegrated_series(base_tume_series, n_series=n_coint_per_group, coint_strength=coint_strength, noise_std=noise_std)
    cointegrated_groups.extend(group_series)
    cointegrated_names.extend([f"Group_{group_id}_Coint_{i}" for i in range(n_coint_per_group)])


# Combine all series into a DataFrame
all_series = cointegrated_groups + independent_variables
all_names = cointegrated_names + independent_names
variable_names = [f"Coint_{i}" for i in range(len(cointegrated_groups))] + [f"Indep_{i}" for i in range(n_independent)]
simulated_data = pd.DataFrame(np.array(all_series).T, columns=all_names)

print (simulated_data)
simulated_data.to_csv('data/coint_simulated_data.csv',index=False)
