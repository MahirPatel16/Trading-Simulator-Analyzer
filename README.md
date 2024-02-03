# StockWyse 
#### StockWyse - Navigate Markets with Confidence
----
---------
# Main Features of the web application have been listed as follows
---------
## Registration and Login
<img src="/screenshots/registration.jpg" width="400" /> <img src="/screenshots/login.jpg" width="400" />
* The user has to register their username, password, and other details before login.
* On login, enter the correct password.
* Make sure you click the login button "Only Once" after entering the username and password.
---------
## HOME - Dashboard
![Local Image](/screenshots/dashboard.jpg)

------
#### Top Gainers and Top Losers
- This feature is on the left panel of the user dashboard. The web app collects live market prices from the NSE website and calculates the top gainers and losers among the nifty 50 stocks. If the market is closed when the app is run, it uses the closing price of the last market day for calculations. 
- The top 3 gainers and the top 3 losers are displayed on the dashboard. When clicked on any of the stocks among these, the user is redirected to the official NSE website of the particular stock, to know the stock information in detail.
--------
#### Business News
- This feature is present on the right panel of the web application. This collects the latest business news using an external API and displays it on the user dashboard. When clicking on any news headline, the user is directed to the particular news website to find the entire news article.
----------
#### Nifty 50 index
- This is the central graph of the user dashboard. The graph is the plot of the variation of the NIFTY-50 index in the last year. NIFTY 50 is a benchmark Indian stock market index that represents the weighted average of 50 of the largest Indian companies listed on the National Stock Exchange.
------
#### Search stock information individually
![Local Image](/screenshots/dashboardsearch.jpg)
- This section is placed below the graph in the central panel of the dashboard. When searched with a specific stock symbol which is listed on NSE's website, the user can see information related to the individual stock. This acts as a feature to visit specific stocks for the user.
-----------
----------------
## MARKET
![Local Image](/screenshots/market.jpg)
- This is the additional feature that we have added which displays the OPEN, CLOSE, LOW, HIGH, and SERIES TYPE for all the stocks listed on the National Stock Exchange. This feature acts as a way to look into any stock available on the NSE.
- Additionally, every column of the table has an option "More Info", which when pressed redirects the user to the official NSE website of the particular stock for the user to find more details of the stock.
-----------
-----------
## COMPARE STOCKS
![Local Image](/screenshots/comparestocks.jpg)
- This feature is one of the key features of the web application and allows the user to compare the prices and variations of more than one stock simultaneously.
- Enter the stock symbol in the "Stock Symbols" bar. To get the details of more than one stock, enter all the stock symbols that you wish to compare, in the same "Stock Symbols" bar with the "comma separated" format. The stock symbols should be separated by a single ","(comma) and no whitespaces, for example: "SBIN,CIPLA,ONGC,ADANIENT"
- From the "DURATION" dropdown, you can select the time range you want to plot data for. The options available are - 1 week, 1 month, 6 months, 1 year and 5 years. The data plotted is the time range subtracted from the last trading day and to the last trading day.
- From the "DATA" dropdown, you can select the data attribute you want to compare for the stocks from the options - OPEN, CLOSE, HIGH, LOW, LTP, VOLUME, No. of Trades, and Value. 
- On clicking the "Show Graph" button, the graph for the given data input will be generated on the right side of the screen. This graph can be magnified in or out conveniently. Also, from the legend, if you tap on any of the stock symbols' then, that particular stock disappears and the graph resizes with the data of remaining visible stocks.
---------
----------
## FILTER
![Local Image](/screenshots/filter.jpg)
- This is another significant feature that helps sort stocks of a specific category. Here you can enter a personalized range for the OPEN  PRICE, CLOSE PRICE, HIGH, LOW, PREVIOUS CLOSE, and TOTAL TRADES and get the stocks that fulfill the entered criteria.
- Select the data attribute you want to apply a filter on from the "SELECT STOCK" dropdown. Enter the starting price(value) in the "START" bar and the ending price(value) in the "END" bar. Now, click on "SORT ASCENDING" or "SORT DESCENDING" according to your requirements. You will get all the stocks that abide by the given filter and in the necessary sorted manner.
- Click on "RESET" to reset back to the default page with no filters applied.
-------------------
---------------
## User Details
![Local Image](/screenshots/userdetails.jpg)
- When clicked on the username - displayed on the right side in the navigation bar - you will be redirected to the user details page, where you can view your details.
----------
----------
