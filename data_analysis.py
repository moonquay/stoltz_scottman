import os
from dotenv import load_dotenv
import quandl
import yfinance
from fbprophet import Prophet
import pandas as pd

load_dotenv()

quandl.ApiConfig.api_key = os.getenv('QUANDL_KEY')

msft_obj = yfinance.Ticker('MSFT')
msft_df = msft_obj.history(period='max')

msft = msft_df.reset_index()[['Date', 'Close']]
msft = msft.rename(columns={'Date': 'ds', 'Close': 'y'})

m = Prophet()
m.fit(msft)

future = m.make_future_dataframe(periods=365)
future.tail()

forecast = m.predict(future)
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()
fig1 = m.plot(forecast)
fig1.show()
