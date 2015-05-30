import urllib2, urllib, json, redis, time
from datetime import datetime
from collections import defaultdict
from collections import Counter
from requests.exceptions import HTTPError
import logging

logging.debug('hello')


def get_star(url):
    try:
        response = urllib2.urlopen('http://b.hatena.ne.jp/entry/json/' + url)
    except HTTPError, e:
        logging.warn('could not download entry page. ' + url + " " + e.reason)
        return {}
    response_json = json.loads(response.read())
    if response_json is None:
        logging.warn('could not download entry page. ' + url)
        return {}

    if 'bookmarks' not in response_json:
        logging.warn('could not get bookmarks. ' + url)
        return {}

    star_dict = dict()
    star_urls = get_star_urls(response_json)
    queries = make_queries(star_urls)
    for query in queries:
        time.sleep(0.5)
        try:
            print query
            star = urllib2.urlopen(query)
        except HTTPError, e:
            logging.warn(
                'could not download star information. ' + query + " " + e.reason)
            continue
        star_json = json.loads(star.read())
        entry_star_info = star_json['entries']

        for star_info in entry_star_info:
            stars=[]
            if 'stars' in star_info:
                stars += star_info['stars']
            if 'colored_stars' in star_info:
                stars += star_info['colored_stars']
            star_user_list = defaultdict(int)
            for star in stars:
                if 'name' in star:
                    star_user_list[star['name']] += 1
            username=star_info['uri'].split('/')[3]
            star_dict[username] = star_user_list
    return star_dict


def get_star_urls(response_json):
    star_urls = []
    eid = response_json['eid']
    print 'download entry information. '+response_json['title']
    for bookmark in response_json['bookmarks']:
        comment = bookmark['comment']
        user = bookmark['user']
        timestamp = bookmark['timestamp']
        if comment != '':
            bookmark_url = create_bookmark_url(user, timestamp, eid)
            star_url = urllib.quote(bookmark_url)
            star_urls.append((user, star_url))
    return star_urls


def make_queries(star_urls):
    query = 'http://s.hatena.com/entry.json?uri='
    count = 0
    for user, star_url in star_urls:
        query = query + star_url + '&uri='
        if count > 40:
            query = query[:-5]
            query += ";http://s.hatena.com/entry.json?uri="
            count=0
        count += 1
    queries = query.split(';')
    return queries


# reference : http://syncer.jp/hatebu-api-matome
def create_bookmark_url(user, timestamp, eid):
    base = 'http://b.hatena.ne.jp/'
    base += user + '/'
    base += datetime.strptime(timestamp, '%Y/%m/%d %H:%M:%S').strftime(
        '%Y%m%d')
    base += '#bookmark-' + eid
    return base


if __name__ == '__main__':
    red = redis.Redis(host='127.0.0.1', port=6379, db=0)
    r = open('hotentry.txt', 'r')

    for i, url in enumerate(r):
        print '---'
        print i, url,
        url=url.split()[1]
        dic = get_star(url)
        for k, v in dic.items():
            if len(v) != 0:
                hash = defaultdict(int)
                for user, count in red.hgetall(k).items():
                    hash[user] = int(count)
                star_dict = dict(Counter(hash) + Counter(v))
                red.hmset(k, star_dict)



