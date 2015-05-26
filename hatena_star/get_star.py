import urllib2, urllib, json, redis, time
from datetime import datetime
from collections import defaultdict
from collections import Counter
from requests.exceptions import HTTPError


def get_star(url):
    try:
        response = urllib2.urlopen('http://b.hatena.ne.jp/entry/json/' + url)
    except HTTPError:
        print 'could not download entry json. '+url
        return {}
    response_json = json.loads(response.read())
    eid = response_json['eid']
    star_dict = dict()
    for bookmark in response_json['bookmarks']:
        time.sleep(0.5)
        if bookmark['comment'] != '':
            user = bookmark['user']
            timestamp = bookmark['timestamp']
            print bookmark['user'], bookmark['timestamp'], bookmark['comment']
            bookmark_url = create_bookmark_url(user, timestamp, eid)
            # print 'http://s.hatena.com/entry.json?uri=' + urllib.quote(
            # bookmark_url)
            star_url = 'http://s.hatena.com/entry.json?uri=' + urllib.quote(
                bookmark_url)
            try:
                star = urllib2.urlopen(star_url)
            except HTTPError:
                print 'could not download star json. ' + star_url
                continue

            star_json = json.loads(star.read())
            if len(star_json['entries']) != 0:
                stars = star_json['entries'][0]['stars']
            else:
                print star_json
            star_user_list = defaultdict(int)
            for star in stars:
                star_user_list[star['name']] += 1
            star_dict[user] = star_user_list
    return star_dict


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
    r = open('hotentry_links.txt', 'r')

    for i,url in enumerate(r):
        print i,url
        dic = get_star(url)
        for k, v in dic.items():
            if len(v) != 0:
                hash = defaultdict(int)
                for user, count in red.hgetall(k).items():
                    hash[user] = int(count)
                star_dict = dict(Counter(hash) + Counter(v))
                red.hmset(k, star_dict)



