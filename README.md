# Tourist Prophet

### *A Disrupted Industry*

The pandemic was a very difficult time for the tourism industry. Tourist Prophet allows the user to access historical monthly data on the number of visitors to a country and make a forecast using Facebook’s Prophet. 

### *The App*
Tourist Prophet is a Python app that needs to run on terminal. You will also need the SQL database called 'tourism_data' saved in the Resources folder. 

The user can select one out of five countries:
Iceland
Jamaica
Portugal
Singapore
UK

The available historical data varies by country, the model in Tourist Prophet will use all available data.

The app will ask whether the user wants to create a dummy variable for the pandemic. The dummy will take the value of 1 if the month falls within the pandemic and 0 otherwise. If the user decides to create the variable it will then ask to specify the first and last month of the pandemic. 

Lastly, the user can specify the number of months they want to forecast. We think that about 50 months in the future is the fair forecast given available data, however, the user can enter any number. If the number is too large the program will not run. 

### *Output*

The program will produce four graphs and save a file called 'forecast.csv' in the folder where the app is located. 

<p align='center'> <img src='images/Figure_1.png'></p>
The black dots represent real data. The blue line the forecast made by Tourist Prophet. The blue shaded area is the 95% confidence interval. 

<p align='center'> <img src='images/Figure_2.png'></p>
The top graph shows the trend. The graph in the middle the annual seasonality. The bottom graph the coefficient of the dummy variable. 

<p align='center'> <img src='images/Figure_3.png'></p>
This an image of 'forecast.csv'. yhat is the predicted number of visitors that month. 

### *Requirements*

The user needs to have Facebook's Prophet installed in their environment. They can get it by running this code:

>conda install plotly
>conda install -c conda-forge fbprophet








