# StockData_AutomaticUpdate_WindPyAPI

Use Wind's API in Python to build an automatic update scheme for Mainland Chinese stocks' data
·By running my code per day, you could update:
    1. "base.csv" file: which contains all the basic info such as name, code, company's full name, ipo and delist dates for all stocks;
    2. All the files in "data" folder containing around 30 fields of price, volume and index flag for each stock;
    3. "tradingdays.csv" file: which records the days you have already updated.
·You can automatically execute this scheme at a fixed time everday with help of Task Scheduler and creat basic task on Win platform, and the analogues on other platforms.
