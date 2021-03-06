#specifies countries that have above 'n' number
n = 500000

#search for a specific country's COVID data from the date specified.
country_to_find = ['India']
value = 'cases'
today = '9/3/20'
#specifies how many days from covid first onset to map linear regression model for country to find
days_from_covid_start = 230


import matplotlib.pyplot as plt 
import pandas as pd
import numpy as np
from datetime import date
import seaborn as sns
from scipy.stats import linregress
from scipy.interpolate import *
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split 

sns.axes_style()

sns.set()

df = pd.read_csv('https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_confirmed_global.csv&filename=time_series_covid19_confirmed_global.csv')
covid = df.groupby('Country/Region', as_index = False).sum()
date_i = covid[(today)]
G = str(date_i.sum())
covid = covid.sort_values((today), ascending=False)

covid.drop(columns=['Lat', 'Long'], inplace=True)
sig_cases = covid[date_i <= n].index
covid.drop(sig_cases, inplace=True)
plt.figure(figsize=(14,7.2))
sns.barplot(y = covid['Country/Region'], x = date_i, data = covid, )



covid = covid.sort_values((today), ascending=True)
x_values = range(len(covid['Country/Region']))
countries = covid['Country/Region'].map(str)


#matplotlib graph, shows the same data as previous seaborn plot

#cases = covid[(today)]

'''plt.figure(figsize=(14,7.2))
sns.set_style("darkgrid")
plt.subplot()
plt.ylabel('Countries')
plt.xlabel('Total Recorded')
plt.title('Covid Cases By Country', size = 10)
group = covid.groupby('Country/Region').sum()
plt.yticks(x_values, countries, rotation= 0, size = 10)
plt.barh(x_values, cases)
plt.grid()'''



covid.sort_values((today), ascending = False, inplace = True)

covid_transposed = covid.transpose()

covid_transposed.columns = covid_transposed.iloc[0]
covid_transposed2 = covid_transposed[1:]

covid_transposed2.to_csv('covid_transposed_new_index.csv', index = False)
covid_transposed2.to_csv('covid_transposed_new.csv')


covid5 = pd.read_csv('covid_transposed_new.csv')
covid5.rename( columns={'Unnamed: 0':'Date'}, inplace=True)


plt.figure(figsize=(14,7.2))
plt.style.use('dark_background')
#sns.set_style("darkgrid")

plt.subplot()

for country in covid5:
    if country in country_to_find:
        slope, intercept, rval, pval, stder = linregress(covid5.index, covid5[country])
        plt.scatter(covid5.index, covid5[country], marker = '.', linestyle = 'None', linewidth = 3)
        y = (slope * days_from_covid_start) + intercept
        plt.plot(covid5.index, (slope * covid5.index) + intercept, color = 'r' )
 

plt.xticks(covid5.index[::30], covid5.Date[::30])
plt.legend(country_to_find, loc=2, prop={'size': 15})
plt.xticks(rotation=32, size = 10)
plt.yticks(size = 10)
plt.title('Covid ' +str(value)+ ' per selected country', size=20)
plt.ylabel('Num ' +str(value), size=10)
plt.xlabel('Date', size=10)
plt.grid(True)

covid4 = pd.read_csv('covid_transposed_new_index.csv')

plt.figure(figsize=(12,7.2))
plt.style.use('dark_background')

#sns.set_style("darkgrid")

plt.subplot()

countries = [country for country in covid4]

prediction = pd.DataFrame(columns=['Country', 'Predicted Cases', 'R Squared', 'P Value', 'Standard Error', today])


for country in covid4:
    plt.plot(covid4.index, covid4[country], marker = ',', linestyle = '-', linewidth = 2)
    #slope, intercept, rval, pval, stder = linregress(covid4.index, covid4[country],)
    y2 = (slope * days_from_covid_start + intercept)
    prediction = prediction.append(pd.DataFrame(data={'Country': country, 'Predicted Cases': y2, 'R Squared': (rval**2), 'P Value': pval, 'Standard Error': stder}, index = [0]), ignore_index = True)


def get_data(x,y):
	for country in covid4:
	return 

TabErroryerror = stder
plt.xticks(covid4.index[::15], covid5.Date[::15])
plt.legend(countries, loc=2, prop={'size': 9})
plt.xticks(rotation=32, size = 10)
plt.yticks(size = 15)
plt.title('Covid ' +str(value)+ ' per selected country', size=15)
plt.ylabel('Num ' +str(value), size=15)
plt.xlabel('Days from first COVID-19 identification', size=15)
plt.grid(False)
plt.savefig('Countries_with_cases_less_than_n.png')

plt.show()

print(str('Total cases as of date ' + str(today) + ' is ')+ G)
prediction.sort_values(by=['Predicted Cases'], ascending = False, inplace = True)
prediction.reset_index(inplace = True)
prediction.to_csv('Covid Prediction.csv')

#x_e = np.array([covid4.index])
    #y_e = np.array([covid4[country]])
    #p1 = np.polyfit(x_e.flatten(), y_e.flatten(), 1)
    #y3 = (p1.slope * days_from_covid_start) + p1.intercept

#print(mymodel)

#print(p1)
