#!/usr/bin/env python
# coding: utf-8

# In[3]:


import numpy as np
import pandas as pd
import requests 
import xlsxwriter
import math


# In[4]:


stocks = pd.read_csv('sp_500_stocks.csv')
type(stocks)
stocks


# In[5]:


from holder import IEX_CLOUD_API_TOKEN


# In[6]:


symbol = 'AAPL'
api_url = f'https://sandbox.iexapis.com/stable/stock/{symbol}/quote/?token={IEX_CLOUD_API_TOKEN}'
data = requests.get(api_url).json()
print(data['symbol'])


# In[7]:


price = data['latestPrice']
market_cap = data['marketCap']


# In[8]:


my_cols = ['Ticker', 'Stock Price', 'Market Capitalization', 'Number of Shares to Buy']
final_dataframe = pd.DataFrame(columns = my_cols)
final_dataframe


# In[9]:


final_dataframe.append(
    pd.Series(
    [
       symbol,
        price,
        market_cap,
        "N/A"   
    ],
    index = my_cols
    ),
    ignore_index = True
)


# In[10]:


final_dataframe = pd.DataFrame(columns = my_cols)
for stock in stocks['Ticker'][:5]:
    api_url = f'https://sandbox.iexapis.com/stable/stock/{stock}/quote/?token={IEX_CLOUD_API_TOKEN}'
    data = requests.get(api_url).json()
    final_dataframe = final_dataframe.append(
        pd.Series(
        [
            stock,
            data['latestPrice'],
            data['marketCap'],
            'N/A'
        ],
        index = my_cols),
    ignore_index = True
    )
    


# In[11]:


final_dataframe


# In[12]:


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


# In[13]:


symbol_groups = list(chunks(stocks['Ticker'], 100))
symbol_strings = [] 
for i in range(0, len(symbol_groups)):
    symbol_strings.append(','.join(symbol_groups[i]))
    
final_dataframe = pd.DataFrame(columns = my_cols)

for symbol_string in symbol_strings:
    batch_api_call_url = f'https://sandbox.iexapis.com/stable/stock/market/batch?symbols={symbol_string}&types=quote&token={IEX_CLOUD_API_TOKEN}'
    data = requests.get(batch_api_call_url).json()
    for symbol in symbol_string.split(','):
        final_dataframe = final_dataframe.append(
            pd.Series(
            [
                symbol,
                data[symbol]['quote']['latestPrice'],
                data[symbol]['quote']['marketCap'],
                'N/A'
            ],
            index = my_cols),
            ignore_index = True
        )
    
final_dataframe


# In[ ]:


portfolio_size = input('Enter the value of your portfolio:')
try:
    val = float(portfolio_size)
    print(val)
except ValueError:
    print("That's not a number! \nPlease try again: ")
    portfolio_size = input('Enter the value of your portfolio: ')
    val = float(portfolio_size)


# In[ ]:


position_size = val / len(final_dataframe.index)
for i in range(0, len(final_dataframe.index)):
    final_dataframe.loc[i,'Number of Shares to Buy'] = math.floor(position_size / final_dataframe.loc[i,'Stock Price'])

final_dataframe


# In[ ]:


writer = pd.ExcelWriter('recommended trades.xlsx', engine = 'xlsxwriter')
final_dataframe.to_excel(writer, 'Recommended Trades', index = False)


# In[ ]:


background_color = '#0a0a23'
font_color = 'ffffff'

string_format = writer.book.add_format(
    {
        'font_color': font_color,
        'bg_color': background_color,
        'border': 1
    }
)

dollar_format = writer.book.add_format(
    {
        'num_format': '$0.00',
        'font_color': font_color,
        'bg_color': background_color,
        'border': 1
    }
)

integer_format = writer.book.add_format(
    {
        'num_format': '0',
        'font_color': font_color,
        'bg_color': background_color,
        'border': 1
    }
)


# In[ ]:


writer.sheets['Recommended Trades'].write('A1', 'Ticker', string_format)
writer.sheets['Recommended Trades'].write('B1', 'Stock Price', dollar_format)
writer.sheets['Recommended Trades'].write('C1', 'Market Capitalization', dollar_format)
writer.sheets['Recommended Trades'].write('D1', 'Number of Shares to Buy', integer_format)


# In[ ]:


column_formats = {
    
    'A': ['Ticker', string_format],
    'B': ['Stock Price', dollar_format],
    'C': ['Market Capitalization', dollar_format],
    'D': ['Number of Shares to Buy', integer_format]
}

for column in column_formats.keys():
    writer.sheets['Recommended Trades'].set_column(f'{column}:{column}', 18, column_formats[column][1])
    writer.sheets['Recommended Trades'].write(f'{column}1', column_formats[column][0], column_formats[column][1])


# In[ ]:


writer.save()

