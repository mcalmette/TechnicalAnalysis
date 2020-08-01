# Stock Technical Analysis :chart_with_upwards_trend:

Dear Recruiter: Thank you for taking the time to consider my application. If you would like
to check out the project for yourself, follow the instructions below - if not, scroll to the 
bottom to see screenshots and a gif of how it works! :grin:


## Usage: Python 3.8/Pandas/MatPlotLib


In terminal or in a Python IDE terminal, type: 
```
git clone https://github.com/mcalmette/TechnicalAnalysis.git
```

To ensure that Python3 is installed:
```
python3 --version
```

### Installations:
```
pip install pandas
pip install matplotlib
pip install mplcursors
```


Now you can run main.py with the given csv files (MSFT, PFE, T, SPY). 

To add different stock data, go to yahoo finance and download a stocks csv file with a date range. Include the SPY 
csv file with the same date range (recommend 1 year/ 3 year/ 5 year), and add this to the techncial analysis folder.

<img width="923" alt="Screen Shot 2020-08-01 at 3 52 58 PM" src="https://user-images.githubusercontent.com/56742122/89111817-26df7c80-d40f-11ea-8ae2-52eeb86bce19.png">

Once you have the files in the project folder, go to main.py, and update the start/end date, name and ticker for the csv file.
Note: The chosen stock dates should match the data of the SPY dates to get an accurate alpha/beta calculation. Additionally, the 
sym and symbols variable should match the csv file so that python can extrapulate the data.
For Microsoft, the variables would look like this:

<img width="222" alt="Screen Shot 2020-08-01 at 3 54 47 PM" src="https://user-images.githubusercontent.com/56742122/89111831-5ee6bf80-d40f-11ea-95e4-45d01efa6f4b.png">

Now you are all set! Simply run main.py. For Microsoft, the program generates this:


<img width="996" alt="Screen Shot 2020-08-01 at 4 05 36 PM" src="https://user-images.githubusercontent.com/56742122/89111937-eb45b200-d410-11ea-8cc3-513880039115.png">

<img width="998" alt="Screen Shot 2020-08-01 at 4 09 06 PM" src="https://user-images.githubusercontent.com/56742122/89111964-60b18280-d411-11ea-97fd-acb9ab2f980a.png">


<img width="500" alt="Screen Shot 2020-08-01 at 4 13 07 PM" src="https://user-images.githubusercontent.com/56742122/89112041-55128b80-d412-11ea-8053-2c990a896963.png"> <img width="500" alt="Screen Shot 2020-08-01 at 4 13 17 PM" src="https://user-images.githubusercontent.com/56742122/89112042-58a61280-d412-11ea-92ed-3c5f2641c8c8.png">




After, the program will generate a StockReport.txt with all of the technical values, looking something like this:

<img width="638" alt="Screen Shot 2020-08-01 at 4 18 30 PM" src="https://user-images.githubusercontent.com/56742122/89112102-1d581380-d413-11ea-9a5d-612f4caf83a2.png">





