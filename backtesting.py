import nasdaqdatalink
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt,floor
try:
    from API_Keys import NasDaq_Key
except:
    NasDaq_Key = input("Enter a NasDaq key: ")

nasdaqdatalink.ApiConfig.api_key = NasDaq_Key

# Unused function
def volatility(alist):
    return np.std(alist) * sqrt(len(alist))

def round_money(money):
    return float(floor((money * 100) + 0.5)) / 100

def plot(title,x_label,y_label,x1,y1,color1,x2,y2,color2,x3,y3,color3,x4,y4,color4):
    plt.plot(x1,y1,color=color1)
    plt.plot(x2,y2,color=color2)
    plt.plot(x3,y3,color=color3)
    plt.plot(x4,y4,color=color4)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.grid(True)
    plt.show()

class market_data:
    def __init__(self,ticker=None,filepath=None):
        if filepath != None:
            self.filepath = filepath
            self.data = self.load_from_file(filepath)
        elif ticker != None:
            self.ticker = ticker
            self.data = self.load_from_nasdaq(ticker)
        else:
            raise ValueError("At least one method of retrieving the data must be an argument (either ticker or file, if both then does file)")
    
    def __str__(self):
        return self.data
    
    def load_from_nasdaq(self,ticker):
        self.ticker = ticker
        numpy_format = nasdaqdatalink.get(ticker, returns="numpy")
        self.data = pd.DataFrame(numpy_format)
        self.data.to_csv('test_data.csv')

    def load_from_file(self,filepath):
        self.filepath = filepath
        file = open(filepath,'r')
        file_as_list = [[item for index,item in enumerate(line.split(',')) if index < 6] for line in file]
        file.close()
            # 0 - Index
            # 1 - Date
            # 2 - Open
            # 3 - High
            # 4 - Low
            # 5 - Close
            # 6 - Volume
        return np.asarray(file_as_list)

    def test(self,initital_money,stocks_buy,stocks_sell,days_up,days_down,stop_if_negative = False):
        daily_money = []
        daily_stock_value = []
        daily_total_valuation = []
        daily_past_volatility = []

        days_increasing = 0
        days_decreasing = 0

        past_opens = []

        stocks = 0.0
        money = initital_money
        lowest_money = initital_money

        for record in self.data:
            open = float(record[2])
            close = float(record[5])
            past_opens.append(open)
            if len(past_opens) > 50:
                current_volatility = volatility(past_opens[-50:-1])
            else:
                current_volatility = volatility(past_opens)
            daily_past_volatility.append(current_volatility)
            if open < close:
                days_increasing += 1
                days_decreasing = 0
            elif open > close:
                days_increasing = 0
                days_decreasing += 1
            else:
                days_increasing = 0
                days_decreasing = 0

            if days_increasing >= days_up:
                stocks += stocks_buy / current_volatility
                money -= float( (stocks_buy / current_volatility) * open)
            elif days_decreasing >= days_down:
                if stocks < (stocks_sell / current_volatility):
                    money += float( (stocks_sell / current_volatility) * open)
                    stocks = 0
                else:
                    stocks -= (stocks_sell / current_volatility)
                    money += float( (stocks_sell / current_volatility) * open)
            if stop_if_negative and money < 0:
                money += float(stocks*open)
                stocks = 0
            if money < lowest_money:
                lowest_money = money
            daily_money.append(money)
            daily_stock_value.append(open * stocks)
            daily_total_valuation.append(money + (open * stocks))
        value_of_stocks = float(self.data[-1][2]) * stocks
        overall_profit = float(value_of_stocks) + float(money)
        return money,stocks,value_of_stocks,lowest_money,overall_profit,daily_stock_value,daily_money,daily_total_valuation,daily_past_volatility,max(daily_total_valuation)

AAPL = market_data(filepath="test_data.csv")

while True:
    try:
        investment = float(input("===========================================\n| Enter your investment:\n| >>> ").strip())
        break
    except:
        print("| Enter a number only.")

while True:
    stop_if_negative = input("| Would you like to stop when money reaches negative value (y/n):\n| >>> ").lower().strip()
    match stop_if_negative:
        case 'y':
            stop_if_negative = True
            break
        case 'n':
            stop_if_negative = False
            break
        case _:
            print("Please enter either y or n.")

money,stocks,value_of_stocks,lowest_money,overall_profit,daily_stock_value,daily_money,daily_total_valuation,daily_past_volatility,max_money \
    = AAPL.test(investment, 1500.0, 1500.0, 3, 3, True)
days = [float(num)/365.25 for num in range(len(daily_total_valuation))]

print(f"""
===========================================
| Investment: --- {investment}
| 
|     Money: ---------------------- {round_money(money)}
|     Number of stocks: ----------- {stocks}
|     Value of stocks: ------------ {round_money(value_of_stocks)}
|     Lowest money: --------------- {round_money(lowest_money)}
|     Highest wealth inc. stocks: - {round_money(max_money)}
| 
| Overall profit: {round_money(overall_profit - investment)}
===========================================""")

plot("Money and stock value over the course of the algorithm","Time in years","Value in money",
     days,daily_money,"red",
     days,daily_stock_value,"blue",
     days,daily_total_valuation,"purple",
     days,daily_past_volatility,"green")
