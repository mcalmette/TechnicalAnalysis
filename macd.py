import pandas as pd
import matplotlib.pyplot as plt
from textgen import txt_file


def macd(start_date,end_date,name,sym):
    dates = pd.date_range(start_date, end_date)
    df1 = pd.DataFrame(index=dates)  # emptyDF

    dfStock = pd.read_csv(f"{sym[0]}.csv", index_col="Date", parse_dates=True, usecols=['Date', 'Adj Close'],
                          na_values=['nan'])
    df1 = df1.join(dfStock, how='inner')
    adj = df1['Adj Close']

    ema12 = adj.ewm(span=12, adjust=False).mean()
    ema26 = adj.ewm(span=26, adjust=False).mean()
    mac = ema12 - ema26
    smoothing = mac.ewm(span=9, adjust=False).mean()

    a = mac.iloc[-1]
    b = smoothing.iloc[-1]
    write_mac(a, b)

    gridsize = (1, 1)
    fig = plt.figure(figsize=(10, 6.5))
    ax1 = plt.subplot2grid(gridsize, (0, 0), colspan=1, rowspan=1)

    fig.set_facecolor('#333333')
    ax1.plot(smoothing, label="Smoothing", color='#FF4500')
    ax1.plot(mac, label="MACD", color='#259FD9')
    ax1.set_title(f"{sym[0]} Moving Average Convergence Divergence", color='white')
    ax1.grid(True, color='#333333')
    ax1.set_facecolor('#444444')
    ax1.spines['bottom'].set_color('white')
    ax1.spines['top'].set_color('white')
    ax1.spines['left'].set_color('white')
    ax1.spines['right'].set_color('white')
    ax1.xaxis.label.set_color('white')
    ax1.tick_params(axis='x', colors='white')
    ax1.yaxis.label.set_color('white')
    ax1.tick_params(axis='y', colors='white')
    ax1.set_xlabel("Date", color='white')
    ax1.set_ylabel("Price", color='white')
    ax1.legend(loc='lower right')
    ax1.axhline(0.0, color='white',linewidth=1)

    plt.subplots_adjust(bottom=0.20)
    plt.show()


def write_mac(a, b):
    divergence = a-b
    txt_file.write("\n\nMACD: ")
    txt_file.write("{:.2f}".format(a))
    txt_file.write("\nSignal Line: ")
    txt_file.write("{:.2f}".format(b))
    txt_file.write("\nDivergence: ")
    txt_file.write("{:.2f}".format(divergence))
