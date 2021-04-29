import csv

#Reading the Data from John-Hopkins University showing the daily statistics of Covid 19 for each country in duaration 22-Jan-2020 to 28-April-2020.
#For US, Statewise Covid 19 Statistics are collected.

path = 'C:\Sanjay\Coursera\Python\Course1_assignment\johns-hopkins-covid-19-daily-dashboard-cases-over-time.csv'

f = open(path)
reader = csv.reader(f,delimiter = ',')
header = next(reader)

#Creating dataset containing list of dictionaries
dataset = []

for line in reader:
    d = dict(zip(header,line))
    dataset.append(d)

print(len(dataset))

# Deriving Month and Year in Month_YYYY format from Reporting Date field

import time
for i in range(len(dataset)):
    dataset[i]['month_year'] = time.strftime('%B_%Y',time.strptime(dataset[i]['report_date_string'].strip(),'%Y-%m-%d'))

#Segragting Non-US Countries Data and US data as US data is represented with States

NonUSdata = []
USdata = []

for i in range(len(dataset)):
  if dataset[i]['country_region'] != 'US':
      NonUSdata.append(dataset[i])
  else:
      USdata.append(dataset[i])

#Sorting US data  based on Reporting Date
USdata = sorted(USdata, key=lambda k: (k['report_date_string']))

#Sorting Non-US Countries Data based on Country and Reporting Date
NonUSdata = sorted(NonUSdata, key=lambda k: (k['country_region'], k['report_date_string']))


#Creating new dataset from Non-US countries having data only from last day of each Month
dataset2 = []
prevMonth = None
prevCountry = None

for i in range(len(NonUSdata)):
       if NonUSdata[i]['country_region'] == prevCountry:
           if NonUSdata[i]['month_year'] != prevMonth:
              dataset2.append(NonUSdata[i-1])
       elif NonUSdata[i]['country_region'] != prevCountry:
             dataset2.append(NonUSdata[i-1])
       prevCountry = NonUSdata[i]['country_region']
       prevMonth = NonUSdata[i]['month_year']


#Calculating Monthwise Fatality Rate for each Non-US Country
for i in range(len(dataset2)):
     if int(dataset2[i]['confirmed']) != 0:
         dataset2[i]['fatality_rate'] = (int(dataset2[i]['deaths'])/int(dataset2[i]['confirmed']))*100 
         #print(dataset2[i]['country_region']+' '+dataset2[i]['month_year']+' '+dataset2[i]['confirmed']+' '+dataset2[i]['deaths']+' '+str(dataset2[i]['recovery_rate']))
     else:
         dataset2[i]['fatality_rate'] = 0.0




#Doing Monthwise Summation of all Confirmed Cases and Death Cases for US States and appending this data to Non-US Countries dataset
prevMonth = None
sumConf = 0
sumDeath = 0

for i in range(len(USdata)):
    if USdata[i]['month_year'] != prevMonth:
        if prevMonth == None:
            sumConf = sumConf + int(USdata[i]['confirmed'])
            sumDeath = sumDeath + int(USdata[i]['deaths'])
        else:
            dataset2.append({'country_region':'US','month_year':prevMonth,'confirmed':sumConf,'deaths':sumDeath,'fatality_rate':(sumDeath/sumConf)*100})
            sumConf = int(USdata[i]['confirmed'])
            sumDeath = int(USdata[i]['deaths'])
    elif USdata[i]['month_year'] == prevMonth:
         sumConf = sumConf + int(USdata[i]['confirmed'])
         sumDeath = sumDeath + int(USdata[i]['deaths'])
         if i == (len(USdata)-1):
             dataset2.append({'country_region':'US','month_year':prevMonth,'confirmed':sumConf,'deaths':sumDeath,'fatality_rate':(sumDeath/sumConf)*100})
    prevMonth = USdata[i]['month_year']    
         

# Dataset containing both US and Non-US countires will be sorted based Country and Confirmed Cases
dataset2 = sorted(dataset2, key=lambda k: (k['country_region'],int(k['confirmed'])))
        

#Countries having more than 100000 Confirmed Cases will be considered for Visualization
topCovidAffectedCountry = []   
for i in range(len(dataset2)):
    if int(dataset2[i]['confirmed']) > 100000:
        topCovidAffectedCountry.append(dataset2[i]['country_region'])
        #print(dataset2[i]['country_region']+' '+dataset2[i]['month_year']+' '+str(dataset2[i]['confirmed'])+' '+str(dataset2[i]['deaths'])+' '+str(dataset2[i]['fatality_rate']))


topCovidAffectedCountry = list(set(topCovidAffectedCountry))

print(topCovidAffectedCountry)

#Creating Datatset having Monthly information for Mostly infected Countries
finalDataSet = []

for i in range(len(dataset2)):
     if dataset2[i]['country_region'] in topCovidAffectedCountry:
               finalDataSet.append(dataset2[i])

#Sorting Dataset based on Country Name and Confirmed Cases.This dataset will be used for Visualization
finalDataSet = sorted(finalDataSet, key=lambda k: (k['country_region'],int(k['confirmed'])))

for i in range(len(finalDataSet)):
        print(finalDataSet[i]['country_region']+' '+finalDataSet[i]['month_year']+' '+str(finalDataSet[i]['confirmed'])+' '+str(finalDataSet[i]['deaths'])+' '+str(finalDataSet[i]['fatality_rate']))

#Data Visualization representing Fatality Rate of the Countries which are most affected by Covid 19.
import matplotlib.pyplot as plt

for val in topCovidAffectedCountry:
    xvalue = []
    yvalue = []
    for i in range(len(finalDataSet)):
        if val == finalDataSet[i]['country_region']:
            xvalue.append(finalDataSet[i]['fatality_rate'])
            yvalue.append(finalDataSet[i]['month_year'])
    plt.plot(yvalue, xvalue,label=val)
            
plt.ylabel('Fatality Rate')
plt.xlabel('Month')
plt.legend()
plt.title('Fatality Rate of Countries Mostly Affected by Covid 19')
plt.show()
