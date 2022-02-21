#!/usr/bin/env python
# coding: utf-8

# In[1]:


from pandas_datareader import data, wb
import pandas as pd
import numpy as np
import datetime
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


start = datetime.datetime(2006,1,1)
end = datetime.datetime(2016,1,1)


# In[3]:


#Bank of America
BAC = data.DataReader("BAC",'yahoo', start, end)
#CITI Group
C = data.DataReader("C", 'yahoo',start, end)
#Goldman Sachs
GS = data.DataReader("GS",'yahoo',start, end)
#JP Morgan
JPM = data.DataReader("JPM",'yahoo', start, end)
#Morgan Stanely
MS = data.DataReader("MS", 'yahoo', start, end)
#Wells Fargo
WFC = data.DataReader("WFC",'yahoo', start, end)


# In[4]:


tickers = ['BAC','C','GS','JPM','MS','WFC']


# In[5]:


bank_stocks = pd.concat([BAC, C, GS, JPM, MS, WFC], axis=1, keys=tickers)


# In[6]:


bank_stocks.head()


# In[7]:


bank_stocks.columns.names = ['Bank Ticker', 'Stock Info']


# In[8]:


bank_stocks.head()


# In[9]:


#EXPLORATORY DATA ANALYSIS


# In[11]:


#Each banks max close period throughout the time period
# bank_stocks['BAC']['Close'].max()

# for tick in tickers:
#     print(tick, bank_stocks[tick]['Close'].max())
    
#more efficent strategy
bank_stocks.xs(key='Close',axis=1,level='Stock Info').max()


# In[12]:


#returns for each banks stock
returns = pd.DataFrame()


# In[13]:


for tick in tickers:
    returns[tick + ' Return'] = bank_stocks[tick]['Close'].pct_change()


# In[14]:


returns.head()


# In[15]:


sns.set_style('whitegrid')
sns.pairplot(returns[1:])


# In[16]:


#Using the returns dataframe figure out which banks stock had best and worst single day returns


# In[17]:


#greatest loss dates
returns.idxmin()


# In[18]:


#greatest returns dates
returns.idxmax()


# In[19]:


#Riskiest stock over entire time period
#Riskiest stock in 2015
returns.std()


# In[20]:


returns.loc['2015-01-01':'2015-12-31'].std()


# In[21]:


#Distplot for 2015 returns of Morgan Stanley
sns.histplot(returns.loc['2015-01-01':'2015-12-31']['MS Return'],kde=True, color='green',bins=50)


# In[22]:


#2008 Distplot for CitiGroup
sns.histplot(returns.loc['2008-01-01':'2008-12-31']['C Return'],kde=True, color='red',bins=50)


# In[24]:


#imports
import matplotlib.pyplot as plt
sns.set_style('whitegrid')
get_ipython().run_line_magic('matplotlib', 'inline')

import plotly
import cufflinks as cf


# In[25]:


#Line plot that shows close price for each bank during the index of time (for loop method)
for tick in tickers: 
    bank_stocks[tick]['Close'].plot(label=tick, figsize=(12,4))
plt.legend()


# In[26]:


#cross section .xs method
bank_stocks.xs(key='Close', axis=1, level='Stock Info').plot(figsize=(12,4))


# In[27]:


#30-DAY MOVING AVERAGE against closing price of Bank of America's stock in 2008


# In[30]:


plt.figure(figsize=(12,4))
BAC['Close'].loc['2008-01-01':'2009-01-01'].rolling(window=30).mean().plot(label='30 Day Mov Avg.')
BAC['Close'].loc['2008-01-01':'2009-01-01'].plot(label='BAC Close')
plt.legend()


# In[31]:


#Creating a heatmap between the stocks correlation of closing prices


# In[36]:


sns.heatmap(bank_stocks.xs(key='Close', axis=1, level="Stock Info").corr(),annot=True)


# In[37]:


sns.clustermap(bank_stocks.xs(key='Close', axis=1, level="Stock Info").corr(),annot=True)


# In[39]:


close_corr = bank_stocks.xs(key='Close', axis=1, level="Stock Info").corr()
close_corr.iplot(kind='heatmap',colorscale='rdylbu')


# In[ ]:




