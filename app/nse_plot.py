from nse_scrape import NSE
import matplotlib.pyplot as plt
import mplfinance as mpf
import pandas as pd

def plot_candlestick(df):
    # Convert the 'date' column to datetime format (if not already)
    df['date'] = pd.to_datetime(df['date'])

    # Ensure the dataframe is sorted by date
    df = df.sort_values('date')

    # Plotting the candlestick chart
    fig, ax = plt.subplots(figsize=(12, 6))
    mpf.plot(df, type='candle', ax=ax, xdate=True, datetime_format='%Y-%m-%d',
             title='Candlestick Chart', ylabel='Price', show_nontrading=True)

    # Show the plot
    plt.show()

# Assuming 'open', 'low', 'high', and 'close' are the column names for OLHC data
# plot_candlestick(df[['date', 'open', 'low', 'high', 'close']])

if __name__ == '__main__':
    from datetime import date
    nse = NSE()
    df = nse.getHistoricalData('SBIN', 'EQ', date(2023, 10, 20), date(2023, 11, 20))
    # Plot the stock data using the plot_stock_data function
    # plot_candlestick(df)
    print(df)
    
    df.plot(x='date', y='close', kind='line')
    
    plt.show()
