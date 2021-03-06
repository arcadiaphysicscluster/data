'''
-Brian Fridman Capstone:
-Getting Bitcoin Articles using NewsAPI
-This program will divide a date dynamically by the number of nodes
and the dates will be used as a crawling option on every pi to reduce
redundancy of news articles.
-All the headlines will be stored in a file called 'Bitcoin_Headlines.txt'

'''
from mpi4py import MPI
from datetime import datetime
from dateutil import parser
from newsapi import NewsApiClient
import os
import requests

#Initialize node number in order to split date
comm = MPI.COMM_WORLD
rank = comm.rank

#Function to take any date, reform it into ISO-8601 format and split the range date
#with the number of nodes
def date_range(start, end, intv):
    start = datetime.strptime(start,"%Y%m%d")
    end = datetime.strptime(end,"%Y%m%d")
    diff = (end  - start ) / intv
    for i in range(intv):
        date = parser.parse((start + diff * i).strftime("%Y%m%d"))
        yield date.isoformat()
    endDate = parser.parse(end.strftime("%Y%m%d"))
    yield endDate.isoformat()

begin = '20180101'	#begin date
end = '20180322'	#end date
dateRange = list(date_range(begin,end,10))	#10 different dates

#This is to dynamically add the date in the newsAPI url options
#beginDate = str(dateRange[rank])
#endDate = str(dateRange[rank + 1])

#newsAPI url crawler

newsapi = NewsApiClient(api_key = 'e1a07328c78945b1ab26c4d1df03d4f3')
all_articles = newsapi.get_everything(q = 'Bitcoin',
	from_parameter = str(dateRange[rank]),
	to = str(dateRange[rank + 1]),
	sort_by = 'popularity')


#Prints file with data
f = open('/home/pi/cloud/Bitcoin_headlines.txt', 'w')
print >>f, all_articles
