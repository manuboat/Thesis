import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def event_detector(threshold,data):   
    current_event = 'none'
    P_h = data[0]
    P_l = data[0]
    t0_dc = data.index[0]
    t1_dc = data.index[0]
    DwEvent = []
    UpEvent = []
    
    for t_c, P_c in data.items():
        if current_event == 'Upturn Event':
            if P_c <= P_h*(1-threshold):
                current_event = 'Downturn Event'
                P_l = P_c
                t1_dc = t_c            
                DwEvent.append((t0_dc, t1_dc))
                t0_dc = t_c
            else:
                if P_c > P_h:
                    P_h = P_c      
                    t0_dc = t_c
       
        if current_event == 'Downturn Event':
            if P_c >= P_l*(1+threshold):
                current_event = 'Upturn Event'
                P_h = P_c
                t1_dc = t_c            
                UpEvent.append((t0_dc, t1_dc))
                t0_dc = t_c
            else:
                if P_c < P_l:
                    P_l = P_c
                    t0_dc = t_c
        if current_event == 'none':
            if P_c <= P_h*(1-threshold):
                current_event = 'Downturn Event'
                t1_dc = t_c            
                DwEvent.append((t0_dc, t1_dc))
            if P_c >= P_l*(1+threshold):
                current_event = 'Upturn Event'
                t1_dc = t_c            
                UpEvent.append((t0_dc, t1_dc))
                
    return DwEvent, UpEvent

def verify_parity(DwEvent, UpEvent):
    
    change_up = 0
    change_dw = 0
    
    if len(UpEvent) == len(DwEvent):
        if UpEvent[0][0] < DwEvent[0][0]:
            change_dw = 1
        else:
            change_up = 1
    return change_dw, change_up


def plot_event(data, DwEvent, UpEvent,freq= 'None'):
    
    plt.rcParams['figure.figsize'] = (15, 7)        
    change_dw, change_up = verify_parity(DwEvent, UpEvent)       
       
    
    plt.plot(data.index, data.values,c='y');
  

    for i in range(len(UpEvent)):
        plt.plot(UpEvent[i],(data.loc[str(UpEvent[i][0])], data.loc[str(UpEvent[i][1])]),'go-');     
    for i in range(len(DwEvent)):    
        plt.plot(DwEvent[i],(data.loc[str(DwEvent[i][0])], data.loc[str(DwEvent[i][1])]),'ro-');
    
    if UpEvent[0][0] < DwEvent[0][0]:
        for i in range(min(len(UpEvent),len(DwEvent))-change_up):
            plt.plot((UpEvent[i][1],DwEvent[i][0]),(data.loc[str(UpEvent[i][1])], data.loc[str(DwEvent[i][0])]),'b--');    
        for i in range(min(len(UpEvent),len(DwEvent))-change_dw):
            plt.plot((DwEvent[i][1],UpEvent[i+1][0]),(data.loc[str(DwEvent[i][1])], data.loc[str(UpEvent[i+1][0])]),'b--');
    else:
        for i in range(min(len(UpEvent),len(DwEvent))-change_dw):
            plt.plot((DwEvent[i][1],UpEvent[i][0]),(data.loc[str(DwEvent[i][1])], data.loc[str(UpEvent[i][0])]),'b--');        
        for i in range(min(len(UpEvent),len(DwEvent))-change_up):
            plt.plot((UpEvent[i][1],DwEvent[i+1][0]),(data.loc[str(UpEvent[i][1])], data.loc[str(DwEvent[i+1][0])]),'b--');    
    
    if freq != 'None':
        sample = data.resample(freq).mean().index;
        plt.plot(data.resample(freq,closed='right',label='right').mean(),'k');
        for time in sample:
            plt.axvline(x=time,c='k',linewidth=0.5,linestyle='--')
        plt.axis(xmin=sample[0] , xmax= sample[-1]);
        
        
def plot_resample(data, freq):
    
    plt.rcParams['figure.figsize'] = (15, 7)  
    
    plt.plot(data.index, data.values,c='y');
    plt.plot(data.resample(freq,closed='right',label='right').mean(),'k');
    
    sample = data.resample(freq).mean().index     
    for time in sample:
        plt.axvline(x=time,c='k',linewidth=0.5,linestyle='--')
    plt.axis(xmin=sample[0] , xmax= sample[-1]);
    
def plot_event_resample(data, DwEvent, UpEvent, freq):
    
    plt.rcParams['figure.figsize'] = (15, 7)      
    change_dw, change_up = verify_parity(DwEvent, UpEvent)       
        
    plt.plot(data.index, data.values,c='y');
    plt.plot(data.resample(freq,closed='right',label='right').mean(),'k');

    for i in range(len(UpEvent)):
        plt.plot(UpEvent[i],(data.loc[str(UpEvent[i][0])], data.loc[str(UpEvent[i][1])]),'go-');     
    for i in range(len(DwEvent)):    
        plt.plot(DwEvent[i],(data.loc[str(DwEvent[i][0])], data.loc[str(DwEvent[i][1])]),'ro-');
    
    if UpEvent[0][0] < DwEvent[0][0]:
        for i in range(min(len(UpEvent),len(DwEvent))-change_up):
            plt.plot((UpEvent[i][1],DwEvent[i][0]),(data.loc[str(UpEvent[i][1])], data.loc[str(DwEvent[i][0])]),'b--');    
        for i in range(min(len(UpEvent),len(DwEvent))-change_dw):
            plt.plot((DwEvent[i][1],UpEvent[i+1][0]),(data.loc[str(DwEvent[i][1])], data.loc[str(UpEvent[i+1][0])]),'b--');
    else:
        for i in range(min(len(UpEvent),len(DwEvent))-change_dw):
            plt.plot((DwEvent[i][1],UpEvent[i][0]),(data.loc[str(DwEvent[i][1])], data.loc[str(UpEvent[i][0])]),'b--');        
        for i in range(min(len(UpEvent),len(DwEvent))-change_up):
            plt.plot((UpEvent[i][1],DwEvent[i+1][0]),(data.loc[str(UpEvent[i][1])], data.loc[str(DwEvent[i+1][0])]),'b--');
        
def event_counter(DwEvent, UpEvent):
    Dw_shoot = []
    Up_shoot = []
    
    change_dw, change_up = verify_parity(DwEvent, UpEvent)
    
    if UpEvent[0][0] < DwEvent[0][0]:
        for i in range(min(len(UpEvent),len(DwEvent))-change_dw):
            Up_shoot.append((UpEvent[i][1],DwEvent[i][0]))       
        for i in range(min(len(UpEvent),len(DwEvent))-change_dw):
            Dw_shoot.append((DwEvent[i][1],UpEvent[i][0]))
    else:
        for i in range(min(len(UpEvent),len(DwEvent))-change_up):
            Dw_shoot.append((DwEvent[i][1],UpEvent[i][0]))       
        for i in range(min(len(UpEvent),len(DwEvent))-change_up):
            Up_shoot.append((UpEvent[i][1],DwEvent[i][0]))
            
        
    return DwEvent, UpEvent, Dw_shoot, Up_shoot

def summary(data,timestamp,Dw_dc, Up_dc, Dw_shoot, Up_shoot):
    
    Dw_change = round(np.mean([abs(data.loc[Dw_shoot[i][0]]-data.loc[Dw_shoot[i][1]])/data.loc[Dw_shoot[i][0]] for i in range(len(Dw_shoot))]), 4)*100
    Up_change = round(np.mean([abs(data.loc[Up_shoot[i][0]]-data.loc[Up_shoot[i][1]])/data.loc[Up_shoot[i][0]] for i in range(len(Up_shoot))]), 4)*100
    Dw_change_mag = round(np.mean([abs(data.loc[Dw_shoot[i][0]]-data.loc[Dw_shoot[i][1]]) for i in range(len(Dw_shoot))]), 2)
    Up_change_mag = round(np.mean([abs(data.loc[Up_shoot[i][0]]-data.loc[Up_shoot[i][1]]) for i in range(len(Up_shoot))]), 2)
    
    new_row = pd.DataFrame([{'Date':pd.to_datetime(timestamp),'Downturn DC':len(Dw_dc),'Upturn DC':len(Up_dc),'Downturn shoot':len(Dw_shoot),'Upturn shoot':len(Up_shoot),'Dw_change':Dw_change,'Up_change':Up_change,'Dw_change_mag':Dw_change_mag,'Up_change_mag':Up_change_mag}])
    
    return new_row
    
    