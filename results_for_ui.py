import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from prophet import Prophet
from abc import ABC,abstractmethod
import json
import os
from datetime import datetime
import requests
import time
import yfinance as yf
class FinancialData(ABC):
    def __init__(self):
        #self.options_for_ticker=["AAPL", "NVDA", "ASELS.IS", "TSLA", "ORCL", "INTC", "EREGL.IS", "MSFT", "AMD", "GM", "LMT", "BABA","QNBTR.IS"]
        #self.options_for_currency=["USD","EUR", "GBP" , "JPY" , "CNY","AED","IRR","CAD","RUB","SAR","GEL"]
        self._start_time=datetime(year=2023,month=10,day=12)
        self._end_time=datetime(year=2025,month=10,day=10)
    @abstractmethod
    def instanteneous_calculate_for_stockmarket(self,given_ticker):
        ticker=yf.Ticker(given_ticker)
        price=ticker.fast_info('last_price')
        return price
    @abstractmethod
    def calculate_stockcode_for_average_value(self,given_ticker):
        df=yf.download(tickers=given_ticker,start=self._start_time,end=self._end_time,interval="1d")
        price=df['Close'].iloc[0:30].mean()
        return price
    @abstractmethod
    def calculate_for_prophet(self,given_ticker,given_periods):
        df=yf.download(tickers=given_ticker,start=self._start_time,end=self._end_time,interval="1d")
        df=df[['Close']].reset_index()
        df.columns=["ds,y"]
        df.dropna()
        model=Prophet()
        model.fit(df)
        future=model.make_future_dataframe(periods=given_periods)
        predict=model.predict(future)
        return predict





















































