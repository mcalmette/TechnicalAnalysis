import pandas as pd
import matplotlib.pyplot as plt
from textgen import txt_file


def bollinger(start_date, end_date, sym, name, days):
    dates = pd.date_range(start_date, end_date)
    df1 = pd.DataFrame(index=dates)  # emptyDF

    dfStock = pd.read_csv(f"{sym[0]}.csv", index_col="Date", parse_dates=True, usecols=['Date', 'Adj Close'],
                          na_values=['nan'])

    df1 = df1.join(dfStock, how='inner')

    movingAverage = dfStock.rolling(days).mean()
    standDev = dfStock.rolling(days).std()
    upperBand = movingAverage + (2 * standDev)
    lowerBand = movingAverage - (2 * standDev)

    gridsize = (1, 1)
    fig = plt.figure(figsize=(10, 6.5))
    fig.suptitle(f"{name}", color='white')
    ax1 = plt.subplot2grid(gridsize, (0, 0), colspan=2, rowspan=2)
    fig.set_facecolor('#333333')

    ax1.plot(df1, label=f"{sym[0]}", color='#259FD9')
    ax1.plot(movingAverage, label="Mid", color='#FF4500')
    ax1.plot(lowerBand, label="Low", color='#FFA500')
    ax1.plot(upperBand, label="High", color='#FFA500')

    ax1.set_title(f"{sym[0]} Bollinger Bands", color='white')
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

    x = 0.04
    y = -0.08
    plt.text(x, y, f"{name}", size=10,
             ha="center", va="center",
             bbox=dict(boxstyle="square",
                       ec='b', fc='b'))

    a = df1.iloc[-1, 0]
    b = movingAverage.iloc[-1, 0]
    c = lowerBand.iloc[-1, 0]
    d = upperBand.iloc[-1, 0]
    write_bol(a, b, c, d)

    plt.show()


def write_bol(a, b, c, d):
    txt_file.write("\n\nBollinger Bands ")
    txt_file.write("\nPrice: ")
    txt_file.write("{:.2f}".format(a))
    txt_file.write("\nSMA: ")
    txt_file.write("{:.2f}".format(b))
    txt_file.write("\nNeg STD Dev: ")
    txt_file.write("{:.2f}".format(c))
    txt_file.write("\nPos STD Dev: ")
    txt_file.write("{:.2f}".format(d))