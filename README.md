# final-project

This project was so much fun, I had built this not so great prediction model a few months ago and this made it far more usable and I got to work some new tools with it.

In short, this website allows a user to sign up and create an account from which they can look up computer parts on ebay to see recent sold trends and get a (rough) prediction of where that price will be 30 days from now. They can save their favorite searches, see their recent searches, and also log out! wow!

To run this project, you will need an ebay API key which can be found here: 
https://developer.ebay.com/signin?tab=register

then set the 'api_key' variable to the 'App ID (Client ID)' you generate

The files look something as follows:

base.html: the base of the 3 html pages

login.html: where a user can log in and register for the site

home.html: this page welcomes the user with their username and allows them to choose a recent or saved search, as well as submit a new search. It uses a js file to make sure an empty search is not submitted (it is fine if one is submitted though as the api will just return price data for that category)

search.html: shows a plot generated by matlab and passed to the html page, as well as price average & prediction data. The plot is made using svg and has scripts included with it so that the data can be explored.

views.py: contains the necessary url functions and some helper ones as well. I tried to keep it more modular than I have in past projects

prediction.py: this is where the program talks to the ebay api, parses the output, and plots it. It uses the help of mpld3 to pass the plot along. numpy and pandas are used to intereact with the columns and provide useful data. The ebay api is subsequently called for 3 pages (more calls take longer for the website to load results), these pages typically contain ~100 results each. The results are then all appended together which gives ~300 results to work with. Those outside of a standard deviation are elimanted to keep the results more realistic.

predictor.css: basic styling for the site, including mobile specific. The plot can only be resized so much due to the library not returning something resizable.



Some notes:
The prediction model does better with more data, this has its downside of taking longer
I showed 10 recent search results, but was unable to filter out duplicates due to the .distinct tag only working on postgresql databases and not sqlite.

Windows Subsystem for Linux did not need this but, if on mac you may need to add this fix for the plots to work:
https://stackoverflow.com/questions/31373163/anaconda-runtime-error-python-is-not-installed-as-a-framework/44912322#44912322

Finally, I did get parallel  ebay calls working and this made the website load considerably faster. I would have made it the default way of searching but it requires removing a check from ebaysdk parallel file and I did not want to make it mandatory for the project to work. But! if you would like to see if working:
1. uncomment the parrallel portion of the code in the 'apiCall' function and bring in the commented parallel code.
2. remove (or comment out) the version check in '/ebaysdk/parallel.py' to remove the warning for using a python version newer than 3.0 as noted here: https://github.com/timotheus/ebaysdk-python/issues/280

Hopefully that works and makes the site load a lot faster!

Ebay category id reference: https://www.isoldwhat.com/
