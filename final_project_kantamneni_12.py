'''
Author: venkata varun chowdary kantamneni
File Name: final_project_kantamneni_12.py
Purpose: Draw a graph for selected commodities in given cities
Revision: 00: Read CSV file and process it to make organized data list
          01: Select the data using filter and Draw & show a graph using plotly
        
'''
#Import All Libraries
import csv
from datetime import datetime 
import plotly.graph_objects as graph
import plotly.offline as py
import re

'''
Function Name: columnPrint
Purpose: To display list of items in a proper structure
Input: list, width and margin
'''
def columnPrint(dataList,wid=20,margin=20):
    s='' # start with an empth string
    for n,item in enumerate(dataList):# Iterate through the list
        # add the item text and number
        s += f'<{" " if (n<9) and len(dataList)>10 else ""}{n+1}> {item:<{margin}}'
        if len(s)>3*(wid+2):
            print(s) # print three columns
            s='' # start the next three columns
    if s:
        print(s) # print leftovers
'''
Function Name: checkUserInputs
Purpose: Checks if user enters a valid index
Input: Actual list and users input
'''
def checkUserInputs(lst,userInput):
    try:
        if len(userInput) ==0:
            return True
        for i in userInput: # Iterate through input string
        #If index is less than '0' and greter than list length
            if int(i)<=0 or int(i)>len(lst):
                return True #Return true if idenx is wrong
    except:
        return True # return true if any exception occurs
    return False # return false if index is correct

### Step 1: Announcement
print("Analysis of Commodity data")
print("-"*27+"\n")


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
# Save all records into an another variable
for row in modData:
    newRow=row[:2] #fetch commodities and date from list
    for loc,price in zip(locations,row[2:]): # iterate through the locations
        records.append(newRow+[loc,price])# add each items to records list
#Get all the commodities to display
uComList=sorted(list(set([i[0] for i in records])))

#Select Products
print("SELECT PRODUCTS BY NUMBER: ")
columnPrint(uComList) # Print all prodcuts
while True:
    #Get commodities index values from user
    userCommodities=input("Enter Product numbers seperated by spaces: ").strip()
    #Remove extra spaces from input string
    userCommodities=re.sub(' +', ' ', userCommodities)
    if(not checkUserInputs(uComList,userCommodities.split())):#check if index are in range
        #Split the input and convert it into product names
        userCommoditiesList=[uComList[int(i)-1] for i in userCommodities.split(" ")]
        #Print selected product names
        print("Selectd Products: "+" ".join(i for i in userCommoditiesList))
        break
    else: #if indexes are out of range
        print("Please enter product numbers with in the range")

# Select dates range and get the input from user
#Get the date from records and change the formate
dateList=[datetime.strftime(i[1],'%Y-%m-%d') for i in records if isinstance(i[1], datetime)]
dateList=sorted(list(set(dateList))) # Remove duplicates and sort the list
print("\nSELECT DATE RANGE BY PRODUCT: ")
columnPrint(dateList,20,15) #print dates in a column
print(f"Earliest available date is: {min(dateList)}")
print(f"Latest available date is {max(dateList)}")
while True:#Check if the input is out of range in dates index
    usersDates=input("Enter start/end date numbers separated by a space: ").strip()
    usersDates=re.sub(' +', ' ', usersDates)#Remove extra spaces from input
    if(len(usersDates.split(" "))>1):#Check if user enter both min and max values    
        if(not checkUserInputs(dateList,usersDates.split())):# Check if input is valid
            #Tranform input indexes to a valid date string
            usersDateList=[dateList[int(i)-1] for i in usersDates.split(" ")]
            fromDate = f'{usersDateList[0]}' if usersDateList[0]<usersDateList[1] else f'{usersDateList[1]}'
            toDate = f'{usersDateList[1]}' if usersDateList[0]<usersDateList[1] else f'{usersDateList[0]}'
            print(f"Dates from {fromDate} to {toDate}")
            break
        else:# if either if the index is out of range
            print("Please enter date numbers with in the range")
    else:# if user skips any input
        print("Please enter min and max dates")
        
#Select Locations
print("\nSELECT LOCATIONS BY NUMBER ...")
#sort the locations
locations=sorted(list(set(locations)))
#Print locations in a table structure
columnPrint(locations,20,70)
while True:
    #Get user input
    userLocations=input("Enter location numbers separated by spaces: ").strip()
    userLocations=re.sub(' +', ' ', userLocations)#Remove extra spaces from input
    if(not checkUserInputs(locations,userLocations.split())):#Validate input
        #Transform indexes to location names
        usersLocationsList=[locations[int(i)-1] for i in userLocations.split(" ")]
        #Print selected locations
        print("Selected locations: "+ " ".join(i for i in usersLocationsList))
        break
    else:#If user input is out of range
        print("Please enter location numbers with in the range")


#Get records on given conditions
fetchRecords = list(filter(lambda x: x[1]>=datetime.strptime(fromDate,'%Y-%m-%d') 
                           and x[1]<=datetime.strptime(toDate,'%Y-%m-%d') 
                           and x[2] in usersLocationsList
                           and x[0] in userCommoditiesList,records))
#Print the total number of records to shown in graph
print(f'{len(fetchRecords)} records have been selected.')
commodityDictionary={} # Create a dictionary to save values
for loc in usersLocationsList:# Iterate through selected locations
    commodityDictionary[loc]={} # set dict with location as a key.
    dictValue={} # Doctinary to save commodity and prices
    for prod in userCommoditiesList:#Iterate through commodities list
        # fetch prices list on basis of commodity and location
        prices=[i[3] for i in fetchRecords if i[0]==prod and i[2]==loc]
        pAvg=round(sum(prices)/len(prices),2) if len(prices) >0 else 0 #Find average
        dictValue.update({prod:pAvg}) #Add it to commodies dictinary
    commodityDictionary[loc]=dictValue# add commodities to cities

tracescomm=[]# Create a trace list 
for k,v in commodityDictionary.items(): # iterate through the dictionary
    #set dict key as name and values to x and y axises
    tracescomm.append(graph.Bar(x=list(v.keys()), y=list(v.values()),
    name=k 
    ))
#calculate width to show a graph
w=len(commodityDictionary)*len(usersLocationsList)*80
#Prepare a layout with title and formats
layout=graph.Layout(barmode="group",yaxis=dict(tickprefix='$',tickformat=".2f",),
                    title=f"Produce prices from {fromDate} through {toDate}",
                    autosize=False,
                    width=w if w>400 else 500,#set width of the graph
                    height=600,
                    )
#Create figure and set layout and traces list
fig=graph.Figure(data=tracescomm, layout=layout)
#Update X and Y axix with titles and font
fig.update_xaxes(
        title_text = "Product",
        title_font = {"size": 20},
        title_standoff = 25)
fig.update_yaxes(
        title_text = "Average Price",
        title_font = {"size": 20},
        title_standoff = 25
         )
#Draw a plot with file name 'grouped-bar.html"
py.plot(fig,filename="grouped-bar.html")


