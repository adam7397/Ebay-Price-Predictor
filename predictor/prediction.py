#from ebaysdk.parallel import Parallel
import matplotlib.pyplot as plt, mpld3
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from ebaysdk.finding import Connection as Finding
from ebaysdk.exception import ConnectionError
import os

# This gets rid of an annoying warning
pd.plotting.register_matplotlib_converters()

def printPlot(df, keyword):
	# So that the x axis does not look terrible
	date_min = np.min(df['times'])
	date_max = np.max(df['times'])

	# Plot the nice data
	fig = plt.figure()
	plt.scatter(df['times'].tolist(), df['prices'])

	prediction = linearReg(df)

	plt.title('Recent Sold Prices: ' + keyword)
	plt.xlabel('Date')
	plt.ylabel('USD')
	plt.xlim(date_min, date_max)

	return mpld3.fig_to_html(fig), prediction

def apiCall(keyword, pages, category):
	# For the range
	pages = pages + 1

	# Initialize the two lists used to store the data
	prices = []
	times = []
	result = []


	# I acknowledge that this is incredibly slow to get data but ebay will only allow 100 items to be returned per page so I have to call multiple pages
	for x in range(1, pages):
		try:
			api = Finding(appid=str(os.environ['api_key']), config_file=None)
			response = api.execute('findCompletedItems', {'keywords': keyword, 'categoryId': category, 'paginationInput': {'pageNumber': x}})
			result = response.dict()['searchResult']['item'] 
		except ConnectionError as e:
			print(e)
			print(e.response.dict())

		for x in result:
			# Add to relevant fields to their respective lists
			prices.append(float(x['sellingStatus']['currentPrice']['value']))
			# Convert the string to datetime object
			times.append(datetime.strptime(x['listingInfo']['endTime'], "%Y-%m-%dT%H:%M:%S.%fZ"))
			
	return prices, times

# Parallel version if you want to have some fun
"""
	try:
		p = Parallel()
		api1 = Finding(appid=str(os.environ['api_key']), config_file=None, parallel=p)
		api1.execute('findCompletedItems', {'keywords': keyword, 'categoryId': category, 'paginationInput': {'pageNumber': 1}})

		api2 = Finding(appid=str(os.environ['api_key']), config_file=None, parallel=p)
		api2.execute('findCompletedItems', {'keywords': keyword, 'categoryId': category, 'paginationInput': {'pageNumber': 2}})        

		api3 = Finding(appid=str(os.environ['api_key']), config_file=None, parallel=p)
		api3.execute('findCompletedItems', {'keywords': keyword, 'categoryId': category, 'paginationInput': {'pageNumber': 3}})        

		api4 = Finding(appid=str(os.environ['api_key']), config_file=None, parallel=p)
		api4.execute('findCompletedItems', {'keywords': keyword, 'categoryId': category, 'paginationInput': {'pageNumber': 4}})

		api5 = Finding(appid=str(os.environ['api_key']), config_file=None, parallel=p)
		api5.execute('findCompletedItems', {'keywords': keyword, 'categoryId': category, 'paginationInput': {'pageNumber': 5}})

		p.wait()

		if p.error():
			raise Exception(p.error())
		
		result.extend(api1.response.dict()['searchResult']['item'])
		result.extend(api2.response.dict()['searchResult']['item'])
		result.extend(api3.response.dict()['searchResult']['item'])
		result.extend(api4.response.dict()['searchResult']['item'])
		result.extend(api5.response.dict()['searchResult']['item'])

		for x in result:
			# Add to relevant fields to their respective lists
			prices.append(float(x['sellingStatus']['currentPrice']['value']))
			# Convert the string to datetime object
			times.append(datetime.strptime(x['listingInfo']['endTime'], "%Y-%m-%dT%H:%M:%S.%fZ"))
			
	except ConnectionError as e:
		raise e

	return prices, times
"""

def createAndFilterDF(prices, times):
	# Helper variables
	median_price = np.median(prices)
	std_price = np.std(prices)

    # Amount of standard deviations for removing outliers
	n = 1

	# Create a dataframe so we can do some nice masking
	dataframe = pd.DataFrame(list(zip(prices, times)), columns=['prices','times'])

	# Convert the full datetime object with times and date: to epoch for linear regression model
	dataframe['epoch'] = (dataframe['times'] - pd.Timestamp("1970-01-01")) // pd.Timedelta('1s')

	# Get rid of some of the outliers so that the data is more representative of the market
	filtered = dataframe[(dataframe['prices'] - median_price < std_price * n) & (median_price - dataframe['prices'] < std_price * n)]

	return filtered

def linearReg(df):
	X_train, X_test, y_train, y_test = train_test_split(df.epoch.values.reshape(-1,1), df.prices, test_size=0.2, random_state = 42)

	regressionModel = LinearRegression()

	regressionModel.fit(X_train, y_train)

	# Just for internal use, accuracy is usually not very high
	print("Train accuracy is %.2f %%" % (regressionModel.score(X_train, y_train)*100))
	print("Test accuracy is %.2f %%" % (regressionModel.score(X_test, y_test)*100))

    # Epoch time 30 days from now
	curTime = np.array([datetime.now().timestamp() + 2592000]).reshape(1, -1)

	# Predict regression & future price
	y_pred = regressionModel.predict(X_test)
	prediction = regressionModel.predict(curTime)

	return prediction

def webcall(keyword, category):
    # Time controls how many pages of results are gathered
    # More pages, better prediction & price data. But at the cost of time
	time = 3
	prices, times = apiCall(keyword, time, category)
	filtered = createAndFilterDF(prices, times)
	plot, prediction = printPlot(filtered, keyword)
	
	return plot, round(prediction[0], 2), round(filtered['prices'].mean(), 2)