import matplotlib.pyplot as plt
import matplotlib.dates as dates
import analytics 

def price_plotter(symbol, timescale, start, end):
    time_range, price_range = analytics.rangeFinder(symbol, timescale, start, end)
    plt.title("Price chart for {0}".format(symbol))
    plt.ylabel("Price ($)")
    plt.plot(time_range, price_range)
    plt.gcf().autofmt_xdate()
    plt.show()

price_plotter("LUNA1-USD", "weeks", 50, 0)