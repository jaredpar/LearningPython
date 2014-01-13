import json
import urllib2
import gzip
import time
import calendar
from datetime import date
from datetime import timedelta
from StringIO import StringIO

#tempUrl = 'http://api.stackexchange.com/2.1/users/23283/answers?fromdate=1389312000&order=desc&sort=activity&site=stackoverflow'
#myUrl = 'http://api.stackexchange.com/2.1/users/23282/answers?site=stackoverflow'

# An answer class that is read directly from the json 
class Answer(object):
    def __init__(self, json):
        self.accepted = json['is_accepted']
        self.score = json['score']
        self.createdSeconds = json['creation_date']
        self.created = time.gmtime(json['creation_date'])
        self.id = json['answer_id']
        self.quesionId = json['question_id']

# Convert a date value into seconds since the epoch in UTC
def dateToSecondsUtc(d):
    str = '{0} {1} {2}'.format(d.year, d.month, d.day) 
    t = time.strptime(str, '%Y %m %d')
    t = int(calendar.timegm(t))
    return t

# Return a tuple of start time, end time for the query 
def getTimeRange():
    startTime = time.strptime('2014 1 1', '%Y %m %d')
    startTime = int(calendar.timegm(startTime))
    endTime = dateToSecondsUtc(date.today() + timedelta(days=1))
    return (startTime, endTime)

# Build up the start and end date for the query 
def getApiUrl(startTime, endTime, page):

    # Build up the URL for the query 
    apiUrlFormat = 'http://api.stackexchange.com/2.1/users/23283/answers?page={0}&fromdate={1}&todate={2}&order=desc&sort=activity&site=stackoverflow'
    return apiUrlFormat.format(page, startTime, endTime)

def printStats(startTime, endtime, answerList):
    totalYear = len(answerList)

    # To get the answers today just find any with a time stamp greater than
    # midnight today
    todayStartSeconds = dateToSecondsUtc(date.today())
    totalDay = sum(x.createdSeconds >= todayStartSeconds for x in answerList)

    diff = date.today() - date(2014, 1, 1)
    days = diff.days
    weeks = days / 7.0
    averageDay = float(totalYear) / days
    averageWeek = float(totalYear) / weeks
    print '---'
    print 'Total Year: {0}'.format(totalYear)
    print 'Total Today: {0}'.format(totalDay)
    print 'Average Per Day: {0}'.format(averageDay)
    print 'Average Per Week: {0}'.format(averageWeek)

def getAnswerList(startTime, endTime):
    print 'Range {0} - {1}'.format(startTime, endTime)

    page = 1
    done = False
    answerList = []
    while not done:
        print 'Getting page {0}'.format(page) 
        apiUrl = getApiUrl(dateRange[0], dateRange[1], page)
        response = urllib2.urlopen(apiUrl)
        if response.info().get('Content-Encoding') == 'gzip':
            buffer = StringIO(response.read())
            f = gzip.GzipFile(fileobj=buffer)
            text = f.read()
        else:
            text = f.read()

        j = json.loads(text)
        for e in j['items']:
            answer = Answer(e)
            answerList.append(answer)

        if not j['has_more']:
            done = True
        else:
            page = page + 1

    return answerList

dateRange = getTimeRange()
answerList = getAnswerList(dateRange[0], dateRange[1])
printStats(dateRange[0], dateRange[1], answerList)
