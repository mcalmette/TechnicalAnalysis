from textgen import open_file
from textgen import close_file
from plotdata import plot_all
from momentum import m_analysis
from bollingerbands import bollinger
from alphabeta import alpha
from macd import macd

### SPECIFY DATES AND SYMBOLS HERE ###
start_date = '2019-07-31'
end_date = '2020-07-31'
symbols = "PFE"
name = "Pfizer"
sym = ['PFE']

def analyze():
    open_file(symbols, name)
    plot_all(start_date, end_date, sym, name)
    m_analysis(start_date, end_date, name, sym)
    bollinger(start_date,end_date,sym,name,days=20) #20 day w/ 2 STD
    macd(start_date,end_date,name,sym)
    alpha(start_date,end_date,symbols,sym)
    close_file()


if __name__ == '__main__':
    analyze()