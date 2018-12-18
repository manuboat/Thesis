# -*- coding: utf-8 -*-
"""
Created on Mon Dec  3 14:18:16 2018

@author: manue
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import timeit
from utils import utils_v2
threshold = 0.05
data = pd.read_csv('coinbaseUSD_1-min_data_2014-12-01_to_2018-06-27.csv')

data['timestamp'] = pd.to_datetime(data['Timestamp'],unit='s')
data.drop('Timestamp',axis=1,inplace = True)
data['Date'] = data.timestamp.dt.date

data = data.set_index('timestamp');

date = '2017 Dec 10'
    
stock_series = data.loc[date]['Weighted_Price']

DCA, CPA = utils_v2.get_events(stock_series,threshold = 0.05)

prices = stock_series.values
times = stock_series.index
    
sub_threshold = threshold/4
    

    
Cpoint = DCA[0]
Cevent = 'None'
    
sub_DCA = []
sub_CPA = []
    
subA_DCA = []
subA_CPA = []
    
for i in range(1,len(DCA)):
    sub_DCA = []
    sub_CPA = []
    
    LLpoint = DCA[i-1]
    LHpoint = DCA[i-1]
    
    while Cpoint <= DCA[i]:
        
        if prices[Cpoint] <= prices[LHpoint]*(1-sub_threshold):
            Cevent = 'Down'
            sub_DCA.append(LHpoint)
            sub_CPA.append(Cpoint)
            LLpoint = Cpoint
            Cpoint +=1;
            break
                    
        if prices[Cpoint] >= prices[LLpoint]*(1+sub_threshold):
            Cevent = 'Up'
            sub_DCA.append(LLpoint)
            sub_CPA.append(Cpoint)
            LHpoint = Cpoint
            Cpoint +=1;
            break
                        
        Cpoint += 1
        
            
    while Cpoint <= DCA[i]:    
        
        if Cevent == 'Down':
            if prices[Cpoint] >= prices[LLpoint]*(1+sub_threshold):
                Cevent = 'Up'
                sub_DCA.append(LLpoint)
                sub_CPA.append(Cpoint)
                LHpoint = Cpoint
                
            else:
                if prices[Cpoint] < prices[LLpoint]:
                    LLpoint = Cpoint
                
        else:
            if prices[Cpoint] <= prices[LHpoint]*(1-sub_threshold):
                Cevent = 'Down'
                sub_DCA.append(LHpoint)
                sub_CPA.append(Cpoint)
                LLpoint = Cpoint    
                
            else:
                if prices[Cpoint] > prices[LHpoint]:
                    LHpoint = Cpoint
            
        Cpoint += 1
    sub_DCA.append(DCA[i])
    subA_DCA.append(sub_DCA)
    subA_CPA.append(sub_CPA)
