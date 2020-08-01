import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
from textgen import txt_file


def get_data(symbols, dates):
    df = pd.DataFrame(index=dates)
    if 'SPY' not in symbols:
       symbols.insert(0, 'SPY')
    for symbol in symbols:
        tmp = pd.read_csv("{}.csv".format(symbol), index_col='Date',
                             parse_dates=True, usecols=['Date', 'Adj Close'], na_values=['nan'])
        tmp = tmp.rename(columns={'Adj Close': symbol})
        df = df.join(tmp)
        if symbol == 'SPY':  # drop dates SPY did not trade
            df = df.dropna(subset=["SPY"])
    return df

def cdr(df):
    dreturns = df.copy()
    dreturns[1:] = (df[1:] / df[:-1].values) - 1
    dreturns.iloc[0, :] = 0
    return dreturns

def alpha(start_date, end_date, symbols, sym):
    dates = pd.date_range(start_date, end_date)
    df = get_data(sym, dates)
    daily_returns = cdr(df)
    daily_returns.plot(kind='scatter', x='SPY', y=f"{symbols}")# cmap='RdYlGn'
    beta,alpha = np.polyfit(daily_returns['SPY'], daily_returns[f'{symbols}'], 1)
    write_ab(alpha,beta)

    #y = mx + b
    #y = beta* daily['SPY] + alpha
    #beta is the slope, how reactive is the stock to the market. a beta of 1 means that when the market goes up 1%,
    #then the stock will go up 1%
    #y axis is called alpha, if positive, means its returning more than the market overall

    plt.plot(daily_returns['SPY'], beta*daily_returns['SPY'] + alpha, '-',color='r')
    #can calculate the correlation of the scatterplot, which essentially checks the STDDEV
    plt.title("Daily returns")

    dr = daily_returns.corr(method='pearson')
    x = 0.04
    y = -0.08
    if beta > 1.0:
        betacolor = '#7CFC00'
    else:
        betacolor = '#FF0000'

    corrcol = '#D3D3D3'

    plt.text(x, y, f"Beta: {beta}\nAlpha: {alpha}", size=10,
             ha="center", va="center",
             bbox=dict(boxstyle="square",
             ec=betacolor,fc=betacolor,))
    plt.text(-x-.01, -y, f"Correlation: {dr}", size=10,
             ha="center", va="center",
             bbox=dict(boxstyle="square",
             ec='#150906',fc=corrcol,))

    #the closer to 1, the more it is correlated
    cor = daily_returns.corr(method='pearson')
    a = cor.iloc[-1, 0]
    write_corr(a)
    plt.show()


def write_ab(alpha,beta):
    txt_file.write("\n\nBeta: ")
    txt_file.write("{:.2f}".format(beta))
    txt_file.write("\nAlpha: ")
    txt_file.write("{:.4f}".format(alpha))

def write_corr(a):
    txt_file.write(f"\nCorrelation: ")
    txt_file.write("{:.4f}".format(a))