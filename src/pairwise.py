import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller, coint
from itertools import combinations



def calculate_pairwise_coint_adf(df, pvalue_threshold=0.05):
    """Calculate pairwise cointegration with ADF statistics on residuals."""
    tickers = df.columns
    pairs = list(combinations(tickers, 2))
    results = []

    for pair in pairs:
        try:
            #print (pair)
            # Perform Engle-Granger cointegration test (which uses ADF on residuals)
            _, pvalue, crit_values = coint(df[pair[0]], df[pair[1]], autolag='BIC')

            # Get the ADF statistic from the cointegration test residuals
            adf_stat = coint(df[pair[0]], df[pair[1]], return_results=False)[0]

            results.append({
                'Variable1': pair[0],
                'Variable2': pair[1],
                'ADF Statistic': adf_stat,
            })
            results.append({
                'Variable2': pair[0],
                'Variable1': pair[1],
                'ADF Statistic': adf_stat,
            })
        except Exception as e:
            print(f"Error processing pair {pair}: {str(e)}")
            continue

    #minimum=results['ADF Statistic'].min()
    #maximum=results['ADF Statistic'].max()

    #results['ADF Statistic']=(results['ADF Statistic']-minimum)/(maximum-minimum)

    return pd.DataFrame(results)



# Example usage
if __name__ == "__main__":
    stock_data = pd.read_csv( 'data/coint_simulated_data.csv')
    coint_results = calculate_pairwise_coint_adf(stock_data)
    # Save results
    coint_results.to_csv('data/coint_pairwise_data.csv')
