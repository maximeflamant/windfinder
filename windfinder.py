import re
import urllib2

from bs4 import BeautifulSoup

'''
Created on Oct 29, 2013
@author: Maxime Flamant
'''

class WindSpot(object):
    
    def __init__(self, name=None, spotMetrics=None):
        if spotMetrics is None:
            spotMetrics = []
        self.name = name
        self.spotMetrics = spotMetrics
    
    def __str__(self):
        return self.name + '\n' + '\n'.join(str(spotMetric) for spotMetric in self.spotMetrics)
    

class SpotMetrics(object):
    
    def __init__(self, date=None, hour=None, knots=None, direction=None):
        self.date = date
        self.hour = hour
        self.knots = knots
        self.direction = direction
    
    def __str__(self):
        return ' '.join((self.date,self.hour,self.knots,self.direction))

class Windfinder(object):
    
    urlPrefix = 'http://www.windfinder.com/weatherforecast/'

    def parse(self, spot ='hoek_van_holland'):
        
        soup = BeautifulSoup(urllib2.urlopen(Windfinder.urlPrefix+spot).read())
        
        #extract HTML tables
        htmlTables = soup.findAll('table',{'class':'weathertable superfc'})
        tables = [[[(re.sub(r"(?m)\s+", " ", " ".join(td.findAll(text=True)).strip())) for td in (row('th')+row('td'))] for row in htable('tr')] for htable in htmlTables]
        def formatTables(table): table[0] += [table[0][1]] * 23
        map(formatTables,tables)
        
        #rotate
        tables = map(lambda table: zip(*table[::-1]),tables)
        
        #parse HTML tables
        spotName = soup.find('nav',{'class':'breadcrumbs'}).find('ol').contents[-2].find('span').string
        spotMetrics = [SpotMetrics(item[-1],item[-2],item[-4],item[-3]) for table in tables for item in table[1:]]
        return WindSpot(spotName,spotMetrics)
    
if __name__ == '__main__':
    
    windFinderScraper = Windfinder()
    hvo = windFinderScraper.parse('hoek_van_holland');
    oost = windFinderScraper.parse('oostende');
    print hvo 
    print oost 
    pass
        
        