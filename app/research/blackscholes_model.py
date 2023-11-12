import math
from scipy.stats import norm

# Function to calculate the Black-Scholes call option price
def black_scholes_call(S, K, T, r, sigma):
    d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    call_price = S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
    return call_price

# Function to calculate the Black-Scholes put option price
def black_scholes_put(S, K, T, r, sigma):
    d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    put_price = K * math.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    return put_price

# Example usage:
S = 2,326.90  # Current stock price
K = 110  # Strike price
T = 1    # Time to expiration (in years)
r = 0.05 # Risk-free interest rate
sigma = 0.2  # Volatility

call_option_price = black_scholes_call(S, K, T, r, sigma)
put_option_price = black_scholes_put(S, K, T, r, sigma)

print(f"Call Option Price: {call_option_price:.2f}")
print(f"Put Option Price: {put_option_price:.2f}")
