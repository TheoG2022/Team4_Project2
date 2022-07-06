#!/usr/bin/env python
# coding: utf-8

# # Define Functions

# ### Libraries

# In[1]:


import sqlalchemy as sql
import pandas as pd
from fbprophet import Prophet
from fbprophet.plot import plot_plotly, plot_components_plotly
import questionary
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


# ## Information from Database

# In[2]:


#Database Connection String
database_connection_string = 'sqlite:///Resources/tourism_data.db'
#Create Engine
engine = sql.create_engine(database_connection_string)


# In[3]:
print('Welcome to Turist Prophet')

country = questionary.select(
    "What country would you like to analyse?",
    choices=[
        "Jamaica",
        "Iceland",
        "Portugal",
        "UK",
        "Singapore"
    ]).ask()

sql_queries = { 'Jamaica':
               """
SELECT ds,y FROM tourism_data
WHERE Country = 'Jamaica'
""",
               'Iceland':
               """
SELECT ds,y FROM tourism_data
WHERE Country = 'Iceland'
""",
               'Portugal':
               """
SELECT ds,y FROM tourism_data
WHERE Country = 'Portugal'
""",
               'UK':
               """
SELECT ds,y FROM tourism_data
WHERE Country = 'UK'
""",
               'Singapore':
               """
SELECT ds,y FROM tourism_data
WHERE Country = 'Singapore'
""",
               
              }


# In[ ]:

df = pd.read_sql_query(sql_queries[country],engine)
df['ds'] = pd.to_datetime(df['ds'])


# In[ ]:


#regressor
df['regressor'] = 0
df.loc[(df['ds'] > '2020-01-01') & (df['ds'] < '2022-03-01'),'regressor'] = 1
#df.tail(50)


# In[ ]:


model = Prophet()


# In[ ]:


#With Regressor
model.add_regressor('regressor')
model.fit(df)


# In[ ]:


#with Regressor
df_future = model.make_future_dataframe(periods=24, freq='M')
df_future['regressor'] = 0
df_future.loc[(df_future['ds'] > '2020-01-01') & (df_future['ds'] < '2022-03-01'),'regressor'] = 1


# In[ ]:


forecast_data = model.predict(df_future)





model.plot(forecast_data)
model.plot_components(forecast_data)
plt.show()

