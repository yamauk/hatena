from bs4 import BeautifulSoup
import datetime
import urllib2
import time


date = datetime.datetime(2014, 01, 01)

while date != datetime.datetime(2015, 05, 01):
    time.sleep(1)
    date_str = date.strftime('%Y%m%d')
    print date_str
    html = urllib2.urlopen(
        "http://b.hatena.ne.jp/hotentry/" + date_str + "?layout=headline")
    soup = BeautifulSoup(html)

    w = open('hotentry.txt', 'a')
    div_box_main = soup.find("div", attrs={"class": "box_main"})
    for link in div_box_main.find_all("a", attrs={"class": "entry-link"}):
        w.write(date_str+" "+link.get('href') + '\n')

    date += datetime.timedelta(days=1)