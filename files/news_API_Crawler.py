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

begin = '20180301'	#begin date
end = '20180322'	#end date
dateRange = list(date_range(begin,end,10))	#10 different dates

#This is to dynamically add the date in the newsAPI url options
beginDate = 'from=' + dateRange(rank) + '&'
endDate = 'to=' + dateRange(rank + 1) + '&'

#newsAPI url crawler
url = ('https://newsapi.org/v2/everything?'
	'q=Bitcoin&'
	beginDate
	endDate
	'sortBy=popularity&'
	'apiKey=e1a07328c78945b1ab26c4d1df03d4f3')
response = requests.get(url)

#Prints file with data
with open('Bitcoin_Test.txt', 'w') as f:
	print(r.json, Bitcoin_Test.txt, file=f)