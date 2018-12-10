import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def get_events(stock_series, threshold):
    
    prices = stock_series.values
    times = stock_series.index
    
    LLpoint = 0
    LHpoint = 0
    
    Cpoint = 1
    Cevent = 'None'
    
    DCA = []
    CPA = []
    
    while Cpoint <= len(prices)-1:
    
        if prices[Cpoint] <= prices[LHpoint]*(1-threshold):
            Cevent = 'Down'
            DCA.append(LHpoint)
            CPA.append(Cpoint)
            LLpoint = Cpoint
            Cpoint +=1;
            break
                
        if prices[Cpoint] >= prices[LLpoint]*(1+threshold):
            Cevent = 'Up'
            DCA.append(LLpoint)
            CPA.append(Cpoint)
            LHpoint = Cpoint
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

    return DCA, CPA

def get_sub_events(stock_series, DCA, CPA, threshold):
    
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
       #sub_DCA.append(DCA[i])
        subA_DCA.append(sub_DCA)
        subA_CPA.append(sub_CPA)
    return subA_DCA, subA_CPA


def plot_events(stock_series,DCA,CPA):
    
    prices = stock_series.values
    times = stock_series.index
    
    plt.rcParams['figure.figsize'] = [15,5]
    plt.plot(stock_series,'y');
    
    if len(CPA) % 2 != 0:
        for i in range(0,len(CPA),2):
            plt.plot([times[DCA[i]],times[CPA[i]]],[prices[DCA[i]],prices[CPA[i]]],'ro-')
            if i == len(CPA)-1 :
                break
            plt.plot([times[CPA[i]],times[DCA[i+1]]],[prices[CPA[i]],prices[DCA[i+1]]],'b--')
            plt.plot([times[DCA[i+1]],times[CPA[i+1]]],[prices[DCA[i+1]],prices[CPA[i+1]]],'go-')
            plt.plot([times[CPA[i+1]],times[DCA[i+2]]],[prices[CPA[i+1]],prices[DCA[i+2]]],'b--')
    
    else:
        for i in range(0,len(CPA),2):
            plt.plot([times[DCA[i]],times[CPA[i]]],[prices[DCA[i]],prices[CPA[i]]],'ro-')
            plt.plot([times[CPA[i]],times[DCA[i+1]]],[prices[CPA[i]],prices[DCA[i+1]]],'b--')
            plt.plot([times[DCA[i+1]],times[CPA[i+1]]],[prices[DCA[i+1]],prices[CPA[i+1]]],'go-')
            if i == len(CPA)-2 :
                break
            plt.plot([times[CPA[i+1]],times[DCA[i+2]]],[prices[CPA[i+1]],prices[DCA[i+2]]],'b--')
            
            
def event_summary(stock_series,DCA,CPA,table,threshold):
       
    prices = stock_series.values
    times = stock_series.index
    
    CPAprices = prices[CPA] 
    DCAprices = prices[DCA]
    
    CPAtime = times[CPA]   
    DCAtime = times[DCA]
    
    NDC = len(DCA)
    
    DDCstar = []
    
    for i in range(NDC):
        if DCAprices[i] > CPAprices[i]:
            DDCstar.append(DCAprices[i] * (1 - threshold))
        else:
            DDCstar.append(DCAprices[i] * (1 + threshold))
            
    DDCstar_time = []

    for i in range(len(DCA)):
        DDCstar_time.append(np.divide(np.multiply(np.subtract(DDCstar[i],
          stock_series[CPA[i]-1]),np.subtract(stock_series.index[CPA[i]],
          stock_series.index[CPA[i]-1])),np.subtract(stock_series[CPA[i]],stock_series[CPA[i]-1]))+stock_series.index[CPA[i]-1])                                                                                         
    
    # OSV(EXT) Overshoot Value at the extreme point
    OSV = []
    TM = []
    T = []
    PC = DCAprices[-1]/DCAprices[0]
    
    for i in range(NDC-1):
        OSV.append(((DCAprices[i+1] - DDCstar[i])/DDCstar[i])/threshold)
        TM.append(((DCAprices[i+1] - DCAprices[i])/DCAprices[i])/threshold)
        T.append(DCAtime[i+1]-DCAtime[i])
    
    LenC = np.sum(np.abs(TM))
    Mean_LenC = np.mean(np.abs(TM))
    
    T_up = []
    T_down = []
      

    if stock_series[DCA[0]] < stock_series[CPA[0]]:
        for i in range(0,len(T)-1,2):
            T_up.append(T[i])
            T_down.append(T[i+1])
    else:
        for i in range(0,len(T)-1,2):
            T_down.append(T[i])
            T_up.append(T[i+1])
            
    Median_T_up = np.median(T_up)
    Median_T_down = np.median(T_down)
    Median_T_overall = np.median(T)
    
    
    TM_up = [value for value in TM if value >= 0]
    TM_down = [value for value in TM if value < 0]
    
    Median_TM_up = np.median(TM_up)
    Median_TM_down = np.median(TM_down)
    Median_TM_overall = np.median(np.abs(TM))
    
    OSV_up = [value for value in OSV if value >= 0]
    OSV_down = [value for value in OSV if value < 0]
    
    Median_OSV_up = np.median(OSV_up)
    Median_OSV_down = np.median(OSV_down)
    Median_OSV_overall = np.median(np.abs(OSV))
    
    # Snapshot Summary of the window
    Tfinal = times[-1]
    Pfinal = prices[-1]
    SPC = prices[-1]/prices[0]
    
    R_DC = []
    
    for i in range(len(T)):
        R_DC.append((np.abs(TM[i])/T[i].seconds)*threshold)
    
    R_DC_up = [value for value in OSV if value >= 0]
    R_DC_down = [value for value in OSV if value < 0]
    
    Median_R_DC_up = np.median(R_DC_up)
    Median_R_DC_down = np.median(R_DC_down)
    Median_R_DC_overall = np.median(np.abs(R_DC))
    
    table = table.append(pd.DataFrame({'NDC':NDC,'PC':PC,'Median_OSV_down':Median_OSV_down,'Median_OSV_up':Median_OSV_up,'Median_OSV_overall':Median_OSV_overall,'Median_TM_overall':Median_TM_overall,'Median_TM_up':Median_TM_up,'Median_TM_down':Median_TM_down,'Median_T_down':Median_T_down,'Median_T_up':Median_T_up,'Median_T_overall':Median_T_overall,'Median_R_DC_down':Median_R_DC_down,'Median_R_DC_up':Median_R_DC_up,'Median_R_DC_overall':Median_R_DC_overall,'Mean_LenC':Mean_LenC,'LenC':LenC},index=[stock_series.index[0].strftime('%Y-%m-%d')]))
        
    return table, OSV, T, TM


def theoretical_CP(stock_series, DCA, CPA, threshold):
    
    DDCstar = []
    DDCstar_time = []     
    for i in range(len(DCA)):
        if stock_series[DCA[i]] > stock_series[CPA[i]]:
            DDCstar.append(stock_series[DCA[i]] * (1 - threshold))
        else:
            DDCstar.append(stock_series[DCA[i]] * (1 + threshold))    
    
        DDCstar_time.append(np.divide(np.multiply(np.subtract(DDCstar[i],stock_series[CPA[i]-1]),
                                                      np.subtract(stock_series.index[CPA[i]],stock_series.index[CPA[i]-1])),
                                          np.subtract(stock_series[CPA[i]],stock_series[CPA[i]-1]))+stock_series.index[CPA[i]-1])
        
    return DDCstar, DDCstar_time



def data_plot(stock_series, DDCstar, DDCstar_time, DCA, CPA):
    values_up = []
    index_up = []

    values_down = []
    index_down = []

    if stock_series[DCA[0]] > DDCstar[0]:
        for i in range(0,len(DCA),2):    
                    values_down.append(stock_series[DCA[i]])
                    values_down.append(DDCstar[i])
                    if i != len(DCA)-2:
                        values_down.append(None)
                    
                    if i != len(DCA)-1: 
                        values_up.append(stock_series[DCA[i+1]])
                        values_up.append(DDCstar[i+1])
                        if i != len(DCA)-2:
                            values_up.append(None)
                        
                    index_down.append(stock_series.index[DCA[i]])
                    index_down.append(DDCstar_time[i])
                    if i != len(DCA)-2:
                        index_down.append(None)
                    
                    if i != len(DCA)-1:
                        index_up.append(stock_series.index[DCA[i+1]])
                        index_up.append(DDCstar_time[i+1])
                        if i != len(DCA)-2:
                            index_up.append(None)
    else:
        for i in range(0,len(DCA),2):    
                    values_up.append(stock_series[DCA[i]])
                    values_up.append(DDCstar[i])
                    if i != len(DCA)-2:
                        values_up.append(None)
                    
                    if i != len(DCA)-1:
                        values_down.append(stock_series[DCA[i+1]])
                        values_down.append(DDCstar[i+1])
                        if i != len(DCA)-2:
                            values_down.append(None)
                        
                    index_up.append(stock_series.index[DCA[i]])
                    index_up.append(DDCstar_time[i])
                    if i != len(DCA)-2:
                        index_up.append(None)
                    
                    if i != len(DCA)-1:
                        index_down.append(stock_series.index[DCA[i+1]])
                        index_down.append(DDCstar_time[i+1])
                        if i != len(DCA)-2:
                            index_down.append(None)
                    

    OS_values = []
    OS_index = []

    for i in range(len(DCA)):    
                if i != len(DCA)-1:
                    OS_values.append(DDCstar[i])
                    OS_values.append(stock_series[DCA[i+1]])
                    if i != len(DCA)-2:
                        OS_values.append(None)
                    
                if i != len(DCA)-1:
                    OS_index.append(DDCstar_time[i])
                    OS_index.append(stock_series.index[DCA[i+1]])
                    if i != len(DCA)-2:
                        OS_index.append(None)
    return values_up,index_up,values_down, index_down, OS_values, OS_index