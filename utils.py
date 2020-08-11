import logging
import os
from statsmodels.tsa.arima_model import ARIMA
import pandas as pd
import yfinance
import pickle

def fetch_data(ticker: str) -> pd.DataFrame:
    """
    Get data from Yahoo finance
    :param ticker: Finance ticker symbol
    :param period: Parameter to pass a yfinance.Ticker object
    :return:
    """
    existing_files = [i[:-4] for i in os.listdir('data')]
    if ticker in existing_files:
        logging.info('Data already exists!')
        data = pd.read_csv(f'data/{ticker}.csv', index_col='Date')
    else:
        logging.info('Fetching new data!')
        ticker_obj = yfinance.Ticker(ticker)
        data = ticker_obj.history(period='max')
        data.to_csv(f'data/{ticker}.csv')
    return data

def build_model(ticker: str):
    """
    Build model for ticker data.
    :param ticker: finance ticker symbol
    :return:
    """
    # Get data or load existing
    ticker_data = fetch_data(ticker)
    existing_files = [i[:-4] for i in os.listdir('models')]
    if ticker in existing_files:
        logging.info('Model already exists!')
        with open(f'models/{ticker}.pkl', 'rb') as f:
            model = pickle.load(f)
        # load pickle
        # model = pd.read_pickle(f'data/{ticker}.pkl')
    else:
        logging.info('No model exists!')
        model_arima = ARIMA(ticker_data['Close'], order=(2, 1, 2))
        model = model_arima.fit()
        with open(f'models/{ticker}.pkl', 'wb') as f:
            pickle.dump(model, f)
    return model