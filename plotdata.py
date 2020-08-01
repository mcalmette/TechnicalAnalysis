import pandas as pd  #pip install pandas
import matplotlib.pyplot as plt  #pip install matplotlib
import mplcursors  #pip install mplcursors
from textgen import txt_file
from matplotlib.widgets import Cursor
import matplotlib

props = dict(boxstyle='round', alpha=0.5, color='#FFA500', ec='#FF8C00')
gridsize = (3, 2)
fig = plt.figure(figsize=(10, 6.5))
ax1 = plt.subplot2grid(gridsize, (0, 0), colspan=2, rowspan=2)
ax2 = plt.subplot2grid(gridsize, (2, 0))
ax3 = plt.subplot2grid(gridsize, (2, 1))

def plot_all(start_date, end_date, sym, name):
    dates = pd.date_range(start_date, end_date)
    # Read SPY data into tmp df
    dfSPY = pd.read_csv("SPY.csv", index_col="Date", parse_dates=True, usecols=['Date', 'Adj Close'],
                        na_values=['nan'])
    # Rename 'Adj Close' column to 'SPY' to prevent crash
    dfSPY = dfSPY.rename(columns={'Adj Close': 'SPY'})

    spy_start_price = dfSPY['SPY']
    spy_start_price = spy_start_price[dates[0]]
    spy_end_price = dfSPY['SPY'].iloc[-1]
    spy_percent = ((spy_end_price - spy_start_price) / spy_start_price) * 100

    # Join two dfs
    for symbol in sym:
        df_temp = pd.read_csv("{}.csv".format(symbol), index_col='Date',
                              parse_dates=True, usecols=['Date', 'Adj Close']
                              , na_values=['nan'])

        stock_start_price = df_temp['Adj Close']
        stock_start_price = stock_start_price[dates[0]]
        stock_end_price = df_temp['Adj Close'].iloc[-1]
        stock_percent = ((stock_end_price - stock_start_price) / stock_start_price) * 100
        df_temp = df_temp.rename(columns={'Adj Close': symbol})
        df_vol = pd.read_csv("{}.csv".format(symbol), index_col='Date',
                              parse_dates=True, usecols=['Date', 'Volume']
                              , na_values=['nan'])
        movingAverage = df_vol.rolling(10).mean()
    df2 = df_temp


    ax1.set_title(f"{name}", color='white')
    #ax1.plot(dfSPY, label='SPY', color='#F87060') uncomment to add SPY
    ax1.plot(df2, label=f"{sym[0]}", color='#259FD9')

    fig.set_facecolor('#333333')

    curs = Cursor(ax1, horizOn=False, vertOn=True, color='white')
    mplcursors.cursor(ax1)

    ax1.grid(True, color='#333333')
    ax1.set_facecolor('#444444')
    ax1.spines['bottom'].set_color('white')
    ax1.spines['top'].set_color('white')
    ax1.spines['left'].set_color('white')
    ax1.spines['right'].set_color('white')
    ax1.xaxis.label.set_color('white')
    ax1.tick_params(axis='x', colors='#333333')
    ax1.yaxis.label.set_color('white')
    ax1.tick_params(axis='y', colors='white')
    ax1.margins(0.02)
    ax1.set_ylabel("Price", color='white')
    ax1.legend(loc='lower right')

    ax1.grid(False, color='#333333')
    ax2.set_facecolor('#444444')
    ax2.spines['bottom'].set_color('white')
    ax2.spines['top'].set_color('white')
    ax2.spines['left'].set_color('white')
    ax2.spines['right'].set_color('white')
    ax2.xaxis.label.set_color('white')
    ax2.tick_params(axis='x', colors='white')
    ax2.yaxis.label.set_color('white')
    ax2.tick_params(axis='y', colors='white')
    ax2.bar(df_vol.index, df_vol['Volume'])
    ax2.set_ylabel("Volume")
    ax2.plot(movingAverage, color='#F87060')
    ax2.set_title('Volume', color='w')

    ax3.grid(True, color='#333333')
    ax3.set_facecolor('#444444')
    ax3.spines['bottom'].set_color('white')
    ax3.spines['top'].set_color('white')
    ax3.spines['left'].set_color('white')
    ax3.spines['right'].set_color('white')
    ax3.xaxis.label.set_color('white')
    ax3.tick_params(axis='x', colors='white')
    ax3.yaxis.label.set_color('white')
    ax3.tick_params(axis='y', colors='white')

    ma10 = df2.ewm(span=10, adjust=False).mean()
    ma20 = df2.ewm(span=20, adjust=False).mean()
    ma50 = df2.ewm(span=50, adjust=False).mean()

    a = ma10.iloc[-1, 0]
    b = ma20.iloc[-1, 0]
    c = ma50.iloc[-1, 0]

    ax3.plot(df2)
    ax3.plot(ma10, label='EMA_10')
    ax3.plot(ma20, label='EMA_20')
    ax3.plot(ma50, label='EMA_50')
    ax3.set_title('Exponential Moving Avg', color='w')
    ax3.legend(bbox_to_anchor=(1.0,0.5), loc='center left', borderaxespad=0, prop={'size': 9})

    fig.autofmt_xdate()
    prc = df2.iloc[-1, 0]

    write_plot(sym, start_date, end_date, spy_percent, stock_percent)
    write_EMA(a, b, c, prc, sym)

    plt.connect('motion_notify_event', mouse_move)
    plt.show()


def mouse_move(event):
    if not event.inaxes:
        return
    else:
        x, y = event.xdata, event.ydata
        if y < 10000:
            change = matplotlib.dates.num2date(x).strftime('%Y-%m-%d')
            update_price(change, y)


def update_price(change, y):
    plt.text(0.01, 1.10, f"{change}",  fontsize=14, transform=ax1.transAxes,
            verticalalignment='top', bbox=props)
    plt.text(0.90, 1.10, "${:.2f}".format(y), fontsize=14, transform=ax1.transAxes,
            verticalalignment='top', bbox=props)


def write_plot(symbols,start_date, end_Date,percent,stock_percent):
    if percent >= 0:
        spychange = "outperformed"
        spych = "increased"
    else:
        spychange = "underperformed"
        spych = "decreased"
    if stock_percent >= 0:
        stockchange = "outperformed"
        ch = "increased"
    else:
        stockchange = "underperformed"
        ch = "decreased"

    diff = stock_percent - percent
    if diff > 0:
        d = "outperform"
    else:
        d = "underperform"

    #calculate the % change from the two
    txt_file.write(f"\n\nFrom {start_date} to {end_Date}, {symbols[0]} has {ch} by ")
    txt_file.write("{:.2f}".format(stock_percent))
    txt_file.write(f"% while the \nS&P 500 has {spych} by ")
    txt_file.write("{:.2f}".format(percent))
    txt_file.write(f"%, making {symbols[0]} {d} the S&P 500 \nby ")
    txt_file.write("{:.2f}".format(diff) + "%.")


def write_EMA(a,b,c,prc,sym):
    txt_file.write("\n\nTechnicals:")
    txt_file.write(f"\n{sym[0]} Price: $")
    txt_file.write("{:.2f}".format(prc))
    txt_file.write(f"\n\n10 Day EMA: $")
    txt_file.write("{:.2f}".format(a))
    txt_file.write(f"\n20 Day EMA: $")
    txt_file.write("{:.2f}".format(b))
    txt_file.write(f"\n50 Day EMA: $")
    txt_file.write("{:.2f}".format(c))
