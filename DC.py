# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv('coinbaseUSD_1-min_data_2014-12-01_to_2018-06-27.csv')

data['timestamp'] = pd.to_datetime(data['Timestamp'],unit='s')
data.drop('Timestamp',axis=1,inplace = True)
data['Date'] = data.timestamp.dt.date

#data.head()

data = data.set_index('timestamp');

#data.loc['2016 Jan 3']['Weighted_Price'].plot(figsize=(16,5));

stock_series = pd.Series(data.loc['2018 Mar 29']['Weighted_Price'])



prices = stock_series.values
times = stock_series.index

LLpoint = 0
LHpoint = 0

Cpoint = 0
Cevent = 'None'

DCA = []
CPA = []

threshold = 0.01

while Cpoint <= len(prices)-1:

    if prices[Cpoint] <= prices[LHpoint]*(1-threshold):
        Cevent = 'Down'
        DCA.append(LHpoint)
        CPA.append(Cpoint)
        Cpoint +=1;
        break
            
    if prices[Cpoint] >= prices[LLpoint]*(1+threshold):
        Cevent = 'Up'
        DCA.append(LLpoint)
        CPA.append(Cpoint)
        Cpoint +=1;
        break
        
    if prices[Cpoint] > prices[LHpoint]:
        LHpoint = Cpoint
            
    if prices[Cpoint] < prices[LLpoint]:
        LLpoint = Cpoint
      
    Cpoint += 1

    
while Cpoint <= len(prices)-1:    

    if Cevent == 'Down':
        if prices[Cpoint] >= prices[LLpoint]*(1+threshold):
            Cevent = 'Up'
            DCA.append(LLpoint)
            CPA.append(Cpoint)
            LHpoint = Cpoint
        
        else:
            if prices[Cpoint] < prices[LLpoint]:
                LLpoint = Cpoint
        
    else:
        if prices[Cpoint] <= prices[LHpoint]*(1-threshold):
            Cevent = 'Down'
            DCA.append(LHpoint)
            CPA.append(Cpoint)
            LLpoint = Cpoint    
        
        else:
            if prices[Cpoint] > prices[LHpoint]:
                LHpoint = Cpoint
    
    Cpoint += 1
