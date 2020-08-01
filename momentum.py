import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from textgen import txt_file


def m_analysis(start_date, end_date,name,sym):
    dates = pd.date_range(start_date,end_date)
    df1 = pd.DataFrame(index=dates)#emptyDF

    dfStock = pd.read_csv(f"{sym[0]}.csv", index_col="Date", parse_dates=True, usecols=['Date', 'Adj Close'],
                          na_values=['nan'])
    df1 = df1.join(dfStock, how='inner')

    adj = df1['Adj Close']
    movingAverageTen = adj.rolling(10).mean()
    movingAverageTwenty = adj.rolling(20).mean()
    movingAverageFifty = adj.rolling(50).mean()
    sma1 = movingAverageTen.iloc[-1]
    sma2 = movingAverageTwenty.iloc[-1]

    sma3 = movingAverageFifty.iloc[-1]

    write_SMA(sma1, sma2, sma3)


    adjClose = df1['Adj Close']
    delta = adjClose.diff()
    delta = delta[1:]

    up, down = delta.copy(), delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0

    window_length = 14

    avg_gain = up.ewm(com=window_length - 1, min_periods=window_length).mean()
    avg_loss = down.ewm(com=window_length - 1, min_periods=window_length).mean()

    df1['avg_gain'] = avg_gain
    df1['avg_loss'] = avg_loss
    diff = avg_gain / avg_loss
    R = 100 - (100 / (1 + abs(diff)))
    rsi_fin = R.iloc[-1]
    write_RSI(rsi_fin)



    #fig, (ax1, ax2, ax3) = plt.subplots(2)
    gridsize = (3, 2) #(3,3)
    fig = plt.figure(figsize=(10, 6.5))
    ax1 = plt.subplot2grid(gridsize, (0, 0), colspan=3, rowspan=2)
    ax2 = plt.subplot2grid(gridsize, (2, 0))
    ax3 = plt.subplot2grid(gridsize, (2, 1))

    norm = normalized_plot(start_date,end_date, sym)
    ax3.plot(norm)

    fig.set_facecolor('#333333')
    ax1.set_facecolor('#444444')
    ax2.set_facecolor('#444444')
    ax3.set_facecolor('#444444')

    ax1.set_title("Simple Moving Average", color='white')
    ax2.set_title("RSI", color='white')
    ax3.set_title("Normalized", color='white')

    fig.suptitle(f"{name}", color='white')
    ax1.plot(movingAverageTen, color='#F87060', label="10 Day SMA")
    ax1.plot(movingAverageTwenty, color='#FFA500', label="20 Day SMA")
    #ax1.plot(movingAverageFifty, label="50 Day SMA") uncomment for 50-day
    ax1.plot(dfStock, label="Stock", color='#259FD9')
    ax1.set_ylabel("Price", color='white')
    ax1.grid(True, color='#333333')
    ax1.legend()

    ax3.legend(('SPY',f"{sym[0]}"))
    b = rsi(start_date,end_date,sym)
    ax2.plot(b, color='#259FD9', label="RSI")

    ax1.spines['bottom'].set_color('white')
    ax1.spines['top'].set_color('white')
    ax1.spines['left'].set_color('white')
    ax1.spines['right'].set_color('white')
    ax1.xaxis.label.set_color('white')
    ax1.tick_params(axis='x', colors='white')
    ax1.yaxis.label.set_color('white')
    ax1.tick_params(axis='y', colors='white')

    ax2.spines['bottom'].set_color('white')
    ax2.spines['top'].set_color('white')
    ax2.spines['left'].set_color('white')
    ax2.spines['right'].set_color('white')
    ax2.xaxis.label.set_color('white')
    ax2.tick_params(axis='x', colors='white')
    ax2.yaxis.label.set_color('white')
    ax2.tick_params(axis='y', colors='white')

    ax2.axhline(70, color='#D62728')
    ax2.axhline(30, color='#2CA02C')
    ax2.axhline(40, color='#333333', linewidth=1)
    ax2.axhline(50, color='#333333', linewidth=1)
    ax2.axhline(60, color='#333333', linewidth=1)

    ax3.spines['bottom'].set_color('white')
    ax3.spines['top'].set_color('white')
    ax3.spines['left'].set_color('white')
    ax3.spines['right'].set_color('white')
    ax3.xaxis.label.set_color('white')
    ax3.tick_params(axis='x', colors='white')
    ax3.yaxis.label.set_color('white')
    ax3.tick_params(axis='y', colors='white')
    ax2.format_xdata = mdates.DateFormatter('%Y-%M-%D')
    fig.autofmt_xdate()

    plt.show()



def rsi(start_date,end_date,sym):
    window_length = 14
    dates = pd.date_range(start_date, end_date)
    df1 = pd.DataFrame(index=dates)  # emptyDF
    dfStock = pd.read_csv(f"{sym[0]}.csv", index_col="Date", parse_dates=True, usecols=['Date', 'Adj Close'],
                          na_values=['nan'])
    df1 = df1.join(dfStock, how='inner')

    adjClose = df1['Adj Close']
    changInPrice = adjClose.diff()
    changeInPrice = changInPrice[1:]

    pos, neg = changeInPrice.copy(), changInPrice.copy()
    pos[pos < 0] = 0
    neg[neg > 0] = 0

    avg_gain = pos.ewm(com= window_length - 1, min_periods=window_length).mean()
    avg_loss = neg.ewm(com=window_length - 1, min_periods=window_length).mean()

    df1['avg_gain'] = avg_gain
    df1['avg_loss'] = avg_loss
    diff = avg_gain/avg_loss
    R = 100 - (100 / (1 + abs(diff)))
    return R


def normalized_plot(start_date,end_date, sym):
    dates = pd.date_range(start_date, end_date)
    #create an empty df
    df1 = pd.DataFrame(index=dates)
    #Read SPY data into tmp df
    dfSPY = pd.read_csv("SPY.csv", index_col="Date", parse_dates=True
                        , usecols=['Date', 'Adj Close'],
                        na_values=['nan'])
    #Renme 'Adj Close' column to 'SPY' to prevent crash
    dfSPY = dfSPY.rename(columns={'Adj Close': 'SPY'})
    #Join two dfs
    df1=df1.join(dfSPY, how='inner')

    #symbols = ['MSFT']
    symbols = sym
    for symbol in symbols:
        df_temp = pd.read_csv("{}.csv".format(symbol), index_col='Date',
                              parse_dates=True, usecols=['Date','Adj Close']
                                                        ,na_values=['nan'])
        df_temp = df_temp.rename(columns={'Adj Close' : symbol})
        df1 = df1.join(df_temp)

    df1 = df1 / df1.iloc[0,:]
    return df1


def write_SMA(sma1,sma2, sma3):
    txt_file.write("\n\n10 Day SMA: $")
    txt_file.write("{:.2f}".format(sma1))
    txt_file.write("\n20 Day SMA: $")
    txt_file.write("{:.2f}".format(sma2))
   # txt_file.write(f"\n50 Day SMA: ${sma3}")


def write_RSI(R):
    txt_file.write("\n\nRSI: ")
    txt_file.write("{:.2f}".format(R))