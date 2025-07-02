# Cointegration-Based Time Series Clustering

This project clusters multiple time series using a **k-medoids** algorithm, where the distance metric is based on cointegration strength rather than simple correlation. It is designed for applications where understanding long-term equilibrium relationships between time series is more important than capturing short-term fluctuations.

## 🔍 Why Use Cointegration Instead of Correlation?

Correlation measures short-term co-movements between time series, which can be misleading when dealing with non-stationary data. Two time series may appear correlated because they share a trend, even if there's no meaningful economic or statistical relationship.

**Cointegration**, on the other hand, identifies whether a linear combination of two non-stationary time series is stationary — suggesting a **long-run equilibrium**. This makes it a more robust and insightful measure when clustering financial or economic time series.

## 📁 Project Structure

├── data/
│ ├── coint_simulated_data.csv # Simulated cointegrated time series
│ └── coint_pairwise_data.csv # Pairwise ADF statistics (Engle-Granger residuals)
│
├── src/
│ ├── cointsim.py # Generates simulated cointegrated time series
│ ├── pairwise.py # Calculates pairwise ADF statistics
│ └── km.py # Runs k-medoids clustering on ADF-based distances

**Methodology**
Cointegration Testing: The core measure of similarity is based on the Engle-Granger test, which performs an ADF (Augmented Dickey-Fuller) test on the residuals of a linear regression between each pair of time series.

Clustering: A k-medoids algorithm is used instead of k-means to allow for arbitrary (non-Euclidean) distance metrics. Here, the "distance" is derived from the strength of cointegration — typically, the ADF test statistic.

Note: While this implementation uses Engle-Granger, the design allows for replacing this metric with other cointegration measures (e.g., Johansen, Phillips-Ouliaris).
