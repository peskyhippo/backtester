import nasdaqdatalink
import pandas as pd

nasdaqdatalink.ApiConfig.api_key = "zzqsVRdBdtjuhza59aQf"

class data:
    def __init__(self,ticker=None):
        self.ticker = ticker
       
        data1 = nasdaqdatalink.get(ticker, returns="numpy")
        data2 = pd.DataFrame(data1)
        self.data = data2.to_csv('test_data.csv')
        del data1
        del data2



#    def load_to_file(self):
#        data_file = open("data.py",'w')
#        data_file.write( "data_table = " + "".join([ f"( {       pd.to_datetime(str(record[0])).strftime('%Y-%m-%d')        } , {','.join([str(float(item)) for pos,item in enumerate(record) if pos != 0])} )" for record in self.data]))
#        data_file.close()
#        numpy.savetxt("nasdaq_data.csv", self.data, delimiter=",")

AAPL = data(ticker="WIKI/AAPL")
#AAPL.load_to_file()
print(AAPL.data)
