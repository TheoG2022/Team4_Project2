from re import A
import sqlalchemy as sql
import pandas as pd
from fbprophet import Prophet

def addregressor(df,date1,date2):
    df['regressor'] = 0
    df.loc[(df['ds'] >= date1) & (df['ds'] <= date2),'regressor'] = 1
    
    return df

def model_prophet(country,num_periods,pandemic,date1 = None,date2 = None):
    """
    This function will receive a dataframe as input with monthly Tourism information and as output you will get the visualization of the forecast of Tourism data.
    """
    #Database Connection String
    database_connection_string = 'sqlite:///Resources/tourism_data.db'
    #Create Engine
    engine = sql.create_engine(database_connection_string)

    #Query the data
    sql_query = """
        SELECT ds,y FROM tourism_data
        WHERE Country = """ + str(country)
    
    df = pd.read_sql_query(sql_query,engine)
    df['ds'] = pd.to_datetime(df['ds'])

    #Modeling
    model = Prophet()

    if pandemic is True:
        model.add_regressor('regressor')
        df = addregressor(df,date1,date2)
        model.fit(df)
        df_future = model.make_future_dataframe(periods=num_periods, freq='M')
        df_future = addregressor(df_future,date1,date2)
    else:
        model.fit(df)
        df_future = model.make_future_dataframe(periods=num_periods, freq='M')
    
    forecast_data = model.predict(df_future)
    model.plot(forecast_data)
    model.plot_components(forecast_data)

    data_output = forecast_data[['yhat,yhat_lower,yhat_upper','trend','yearly','extra_regressors_additive']]
    return data_output




