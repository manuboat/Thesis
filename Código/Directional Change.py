
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import timeit

from utils import utils
plt.rcParams['figure.figsize'] = (15, 7) 
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


tic=timeit.default_timer()
data = pd.read_csv('coinbaseUSD_1-min_data_2014-12-01_to_2018-06-27.csv')


# In[3]:


data['timestamp'] = pd.to_datetime(data['Timestamp'],unit='s')
data.drop('Timestamp',axis=1,inplace = True)
data['Date'] = data.timestamp.dt.date


# In[4]:


data = data.set_index('timestamp');


# In[5]:


data['Weighted_Price'].plot(figsize=(15, 7));


# In[6]:


date = '2018 Mar'


# In[7]:


price_array = data.loc[date]['Weighted_Price']


# In[8]:


price_array.resample('D').mean().plot(figsize=(15, 7));
sample = price_array.resample('D').mean().index     
for time in sample:
    plt.axvline(x=time,c='k',linewidth=0.5,linestyle='--')
plt.axis(xmin=sample[0] , xmax= sample[-1]);


# In[9]:


utils.plot_resample(price_array,'D');


# In[10]:


DwEvent, UpEvent = utils.event_detector(0.04, price_array)


# In[11]:


utils.plot_event(price_array,DwEvent,UpEvent);


# In[12]:


utils.plot_event(price_array,DwEvent,UpEvent,'D');


# In[13]:


Dw_dc, Up_dc, Dw_shoot, Up_shoot = utils.event_counter(DwEvent, UpEvent);


# In[14]:


table = utils.summary(price_array,'2017 Nov 1',Dw_dc, Up_dc, Dw_shoot, Up_shoot)
for date in pd.date_range(pd.to_datetime('2017 Nov 2'),periods=100,freq='D'):
    price_array = data.loc[str(date).replace(' 00:00:00','')]['Weighted_Price']
    DwEvent, UpEvent = utils.event_detector(0.01, price_array)
    Dw_dc, Up_dc, Dw_shoot, Up_shoot = utils.event_counter(DwEvent, UpEvent);
    table = table.append(utils.summary(price_array,date,Dw_dc, Up_dc, Dw_shoot, Up_shoot));


# In[15]:


table['Up_change'].mean()


# In[16]:


table['Dw_change'].mean()


# In[17]:


table


# In[18]:


toc=timeit.default_timer()
toc - tic

