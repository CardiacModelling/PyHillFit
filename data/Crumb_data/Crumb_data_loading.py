
# coding: utf-8

# In[ ]:

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#import sys        #(just for version number)
#import matplotlib #(just for version number)
#print('Python version ' + sys.version)
#print('Pandas version ' + pd.__version__)
#print('Matplotlib version ' + matplotlib.__version__)


# In[ ]:

file_name = '../crumb_data.csv'
df = pd.read_csv(file_name, names=['Drug','Channel','Experiment','Concentration','Inhibition'],skiprows=1)
df


# In[ ]:

drug_and_channel = df.loc[(df['Drug'] == 'Amiodarone') & (df['Channel'] == 'Cav1.2'), ['Concentration','Inhibition']]
drug_and_channel
drug_and_channel.values


# In[ ]:

drugs = df.Drug.unique()
print(drugs)


# In[ ]:

channels = df.Channel.unique()
print(channels)


# In[ ]:

for drug in drugs:
    for channel in channels:
        drug_and_channel_values = df.loc[(df['Drug'] == drug) & (df['Channel'] == channel), ['Concentration','Inhibition']]
        print(drug,channel)
        print(drug_and_channel_values)


# In[ ]:





