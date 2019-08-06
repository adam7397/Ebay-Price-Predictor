import matplotlib.pyplot as plt, mpld3
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from ebaysdk.finding import Connection as Finding
from ebaysdk.exception import ConnectionError
import os

pd.plotting.register_matplotlib_converters() #This gets rid of an annoying warning

def printPlot(df, keyword):
	#So that the x axis does not look terrible
	date_min = np.min(df['times'])
	date_max = np.max(df['times'])

	#plot the nice data
	fig = plt.figure()
	plt.scatter(df['times'].tolist(), df['prices'])

	X_test,y_pred,prediction = linearReg(df)
	#plt.plot(X_test,y_pred, color='yellow', linewidth=3)

	plt.title('All Sold Prices: ' + keyword)
	plt.xlabel('Date')
	plt.ylabel('USD')
	plt.xlim(date_min, date_max)

	return mpld3.fig_to_html(fig), prediction

def apiCall(keyword, pages, category):
	pages = pages + 1 #for the range

	#Initialize the two lists used to store the data
	prices = []
	times = []

	#I acknowledge that this is incredibly slow to get data but ebay will only allow 100 items to be returned per page so i have to call multiple pages, essentially o(n^2) but at least n is defined ahead of time
	for x in range(1, pages):
		try:
		    api = Finding(appid=str(os.environ['api_key']), config_file=None)
		    response = api.execute('findCompletedItems', {'keywords': keyword, 'categoryId': category, 'paginationInput': {'pageNumber': x}})
		    result = response.dict()['searchResult']
		except ConnectionError as e:
		    print(e)
		    print(e.response.dict())

		resultlist = result['item'] #cast the series or whatever to a list
		for x in resultlist:
			#Add to relevant fields to their respective lists
			prices.append(float(x['sellingStatus']['currentPrice']['value'])) 
			times.append(datetime.strptime(x['listingInfo']['endTime'], "%Y-%m-%dT%H:%M:%S.%fZ")) #convert the string to datetime object
			#print(x['primaryCategory']['categoryId'], x['primaryCategory']['categoryName'], x['title'])
			#print(x['sellingStatus']['currentPrice']['value'], x['title'])

	return prices, times

def createAndFilterDF(prices, times):
	#helper variables
	minimum_price = np.min(prices)
	maximum_price = np.max(prices)
	average_price = np.mean(prices)
	median_price = np.median(prices)
	std_price = np.std(prices)

	#print("Minimum price: ${}".format(minimum_price)) 
	#print("Maximum price: ${}".format(maximum_price))
	#print("Mean price: ${}".format(average_price))
	#print("Median price ${}".format(median_price))
	#print("Standard deviation of prices: ${}".format(std_price))	

	n = 1 #amount of standard deviations for removing outliers

	#create a dataframe so we can do some nice masking
	dataframe = pd.DataFrame(list(zip(prices, times)), columns=['prices','times'])

	#convert the full datetime object with times and date: to epoch for linear regression model
	dataframe['epoch'] = (dataframe['times'] - pd.Timestamp("1970-01-01")) // pd.Timedelta('1s')
	#print(dataframe['times'], dataframe['epoch'])

	#get rid of some of the outliers so that the data is more representative of the market
	filtered = dataframe[(dataframe['prices'] - median_price < std_price * n) & (median_price - dataframe['prices'] < std_price * n)]

	return filtered


def linearReg(df):
	X_train, X_test, y_train, y_test = train_test_split(df.epoch.values.reshape(-1,1), df.prices, test_size=0.2, random_state = 42)

	regressionModel = LinearRegression()

	regressionModel.fit(X_train, y_train)

	print("Train accuracy is %.2f %%" % (regressionModel.score(X_train, y_train)*100))
	print("Test accuracy is %.2f %%" % (regressionModel.score(X_test, y_test)*100))

	curTime = np.array([datetime.now().timestamp() + 2592000])

	curTime = curTime.reshape(1, -1)

	prediction = regressionModel.predict(curTime)

	#print("price prediction 30 days from now:", regressionModel.predict(curTime))

	#predict regression, plot it too
	y_pred = regressionModel.predict(X_test)
	#fig = plt.figure()
	#plt.scatter(X_test,y_test, color='black')
	#plt.plot(X_test,y_pred, color='blue',linewidth=3)

	#plt.title('Test Data & Linear Regression')
	#plt.xlabel('Time in Epoch')
	#plt.ylabel('USD')
	#plt.show()
	#return mpld3.fig_to_html(fig)

	return X_test,y_pred, prediction

def webcall(keyword, category):
	time = 2
	prices, times = apiCall(keyword, time, category)
	filtered = createAndFilterDF(prices, times)
	plot, prediction = printPlot(filtered, keyword)
	#plot = linearReg(filtered)
	
	return plot, round(prediction[0], 2)
