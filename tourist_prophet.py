# import Libraries

import sqlalchemy as sql
import pandas as pd
from fbprophet import Prophet
from fbprophet.plot import plot_plotly, plot_components_plotly
import questionary
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import csv

#Connect with SQL database
database_connection_string = 'sqlite:///Resources/tourism_data.db'
#Create SQL engine
engine = sql.create_engine(database_connection_string)



print('Welcome to Tourist Prophet')

#user selects the country they want to query
country = questionary.select(
    "What country would you like to analyse?",
    choices=[
        "Jamaica",
        "Iceland",
        "Portugal",
        "UK",
        "Singapore"
    ]).ask()


#query dictionary
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


# query the SQL database by using the query dictionary and the user input
df = pd.read_sql_query(sql_queries[country],engine)
df['ds'] = pd.to_datetime(df['ds'])



print('The pandemic had an enormous effect on tourism')
print('Tourist Prophet allows you to isolate its effect')
print('by creating a regressor that takes the value of 1')
print('if the month falls within the pandemic, or 0 otherwise.')

#ask about the dummy variable
dummy = questionary.select(
    "Would you like to create this variable?",
    choices=[
        "Yes",
        "No",
    ]).ask()

#create regressor

df['regressor'] = 0

# add the 1 in the regressor between the dates chosen by the user
if dummy == 'Yes':
    p_start_month=questionary.text("Enter the first month of the pandemic, use the format YYYY-MM").ask()
    p_end_month=questionary.text("Enter the last month the pandemic, use the format YYYY-MM").ask()
    p_start_month=p_start_month+"-01"
    p_end_month=p_end_month+"-01"
    df.loc[(df['ds'] >= p_start_month) & (df['ds'] <= p_end_month),'regressor'] = 1




#ask number of months to be predicted
number_of_predictions = questionary.text("How many months would you like Tourist Prophet to predict (max 500)?").ask()
number_of_predictions = int(number_of_predictions)

#create Prophet object
model = Prophet()



#add regressor to Prophet object
model.add_regressor('regressor')
#fit model
model.fit(df)

#create dataframe that will hold the prediction
#the dataframe needs to have a projected regressor
df_future = model.make_future_dataframe(periods=number_of_predictions, freq='M')
df_future['regressor'] = 0
if dummy == 'Yes':
    df_future.loc[(df_future['ds'] >= p_start_month) & (df_future['ds'] <= p_end_month),'regressor'] = 1

#create prediction
forecast_data = model.predict(df_future)

#display graphs
model.plot(forecast_data)
model.plot_components(forecast_data)
plt.show()

#create smaller dataframe from the forecast output to print as a csv file
forecast_data2=forecast_data[['ds','yhat','yhat_lower','yhat_upper','regressor', 'trend']]
forecast_data2.to_csv('forecast.csv', index=False)

