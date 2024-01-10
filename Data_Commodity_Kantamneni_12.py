# -*- coding: utf-8 -*-
'''
Author: venkata varun chowdary kantamneni
File Name: Data_Visualization_kantamneni_12.py
Purpose: Draw a graph for orange sales in chicago and new york
Revision: 00: Read CSV file and process it to make organized data list
          01: Select the data using filter and Draw & show a graph using pyplot
        
'''
#Import All Libraries
import matplotlib.pyplot as plt
import csv
from datetime import datetime 
import matplotlib.ticker as mtick

### Step 1: Announcement
print("Program to draw a graph for orange sales in chicago and new york")
print("---------------------------------------------------------------- \n")


#Read data from csv file and save it in data variable
with open('produce_csv.csv','r') as csvFile: # Open a file with read mode
    reader=csv.reader(csvFile) 
    data=[row for row in reader] # iterate through the reader object and make a list
modData=[] # Create a list to save transformed data
for row in data: # Iterate through data list
    newRow=list() # Create a row to handle each commodities per location
    for item in row:
        if '$' in item: # If a cell data contains $
            newRow.append(float(item.replace("$",""))) #Replace $ with empty string
        elif "/" in item: # if a cell data contains / (means date)
            newRow.append(datetime.strptime(item,'%m/%d/%Y')) #Convert it datetime
        else:
            newRow.append(item)# append item to new row
        modData.append(newRow) # Append new row to list
#Pull locations from first list item (from header)
locations=modData.pop(0)[2:]
records=list() #Create a list to save seggregated data in a more meaning ful way.
for row in modData:
    newRow=row[:2] #fetch commodities and date from list
    for loc,price in zip(locations,row[2:]): # iterate through the locations
        records.append(newRow+[loc,price])# add each items to records list

#Fetch oranges details which are sold out in chicago
fetchRecordsForChicago=list(filter(lambda x:x[0]=='Oranges' and x[2]=="Chicago",records))
datesForChicago=[x[1] for x in fetchRecordsForChicago] #List out the dates of chicago sales
pricesForChicago=[x[3] for x in fetchRecordsForChicago]# List out the prices of chicago sales
#Fetch oranges details which are sold out in New York
fetchRecordsForNY=list(filter(lambda x:x[0]=='Oranges' and x[2]=="New York",records))
datesForNY=[x[1] for x in fetchRecordsForNY] #List out the dates of New York sales
pricesForNY=[x[3] for x in fetchRecordsForNY] # List out the prices of New York sales

fig=plt.figure() # Create a figure
ax=fig.add_subplot(111) #add an axix object to the figure
ax.set_xlabel("date")# Add a label on x-axix
ax.set_ylabel("price in dollars")# Add a lebel on y-Axis
fmt = '${x:,.2f}' # format for dollars w/ 2 decimal places
tick = mtick.StrMethodFormatter(fmt) # define the format
ax.yaxis.set_major_formatter(tick) # establish format for y-axis labels
# Add a title for the graph
plt.suptitle("The Cost of Oranges in Chicago and New York",weight='bold')
# Add a lebel on y-Axis
ax.set_title(f'from {min(datesForChicago).date()} through {max(datesForChicago).date()}', fontsize = 12)
#Create a plot for chicago sales with color green and marker '.'
ax.plot(datesForChicago,pricesForChicago,label="Oranges in Chicago",marker='.',color='green')
#Create another plot for new york sales with color blue and marker '.'
ax.plot(datesForNY,pricesForNY,label="Oranges in New York",marker='.',color='blue')
plt.grid()# Add grid to represent each plot
plt.show() # show the plot


''' Additional code to save organized data records to a new CSV file '''
# open an output file
resultFile = open('result.csv','w')
# instantiate a csv writer for the output file
# change EOL default to prevent blank lines
writer = csv.writer(resultFile,lineterminator='\n')
writer.writerows(records) # write the organized data to the file
resultFile.close() # close the output file
commodities= list(set([x[0] for x in records]))
dates= list(set([x[1] for x in records]))
allLocations= list(set([x[2] for x in records]))
