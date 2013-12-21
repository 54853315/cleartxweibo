#!/usr/bin/env python
#-*-coding:utf-8-*-
import urllib2
import webbrowser
import re
import json

app_key = ""
app_secret = ""


webbrowser.open("https://open.t.qq.com/cgi-bin/oauth2/authorize?client_id=%s&response_type=code&redirect_uri=http://ashin.sinaapp.com"%(app_key))

code=raw_input("code:")

url = "https://open.t.qq.com/cgi-bin/oauth2/access_token?client_id=%s&client_secret=%s&redirect_uri=http://ashin.sinaapp.com&grant_type=authorization_code&code=%s"%(app_key, app_secret, code)

c = urllib2.urlopen(url).read()
datas = dict([i.split("=") for i in c.split("&")])

access_token = datas["access_token"]
openid = datas["openid"]
clientip = re.search('<td>(\d+\.\d+\.\d+\.\d+)</td>', urllib2.urlopen('http://whois.ipcn.org/').read()).group(1)


def get_weibo_ids():
    c = urllib2.urlopen("http://open.t.qq.com/api/statuses/broadcast_timeline_ids?format=json&pageflag=0&reqnum=199&pagetime=0&lastid=0&type=0&contenttype=0&oauth_consumer_key=%s&access_token=%s&openid=%s&clientip=%s&oauth_version=2.a&scope=all&format=json"%(app_key, access_token, openid, clientip)).read()

    try:
        jsondata = json.loads(c)
    except:
        jsondata = json.loads(unicode(c,'latin1')) #特殊情况，0xe9结尾，latin1
    ids = [i['id'] for i in jsondata['data']['info']]
    return ids

def clear_weibos():
    print 'clearing...waiting...'
    ids = get_weibo_ids()
    while ids:
        for weiboid in ids:
            r = urllib2.Request("https://open.t.qq.com/api/t/del", "oauth_consumer_key=%s&access_token=%s&openid=%s&clientip=%s&oauth_version=2.a&scope=all&format=json&id=%s"%(app_key, access_token, openid, clientip, weiboid))
            urllib2.urlopen(r)
        ids = get_weibo_ids()
        if len(ids) <= 1:
            break
    print "clear over~"

if __name__ == "__main__":
    clear_weibos()

