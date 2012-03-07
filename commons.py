# -*- coding: utf-8 -*-
import urllib2
import urllib
import base64
from simplejson import loads as json_decode
from simplejson import dumps as json_encode
import time
import pymongo
import random

db = pymongo.Connection('localhost',27017)['atapp']

types = {
    u'checkin': u'%s 在 %s 签到',
    u'tip': u'%s 在 %s 发表攻略',
    u'shout': u'%s 说%s',
    u'schedule': u'%s 想要去 %s',
    u'photo': u'%s 在 %s 拍照'
}

colors = ['red','yellow','green','blue','cyan','pink','brown','orange']

def call_api(api,params,auth='',debug=0):
    domain = 'http://api.jiepang.com/'
    params['source'] = '@pp'
    params = urllib.urlencode(params)
    request = urllib2.Request(domain + api + '?' + params)
    if auth:
        request.add_header("Authorization", "Basic %s" % auth)
    request.add_header("Content-Type","application/json")
    opener = urllib2.build_opener(urllib2.HTTPHandler(debuglevel=debug))
    try:
        response = opener.open(request)
        res = json_decode(response.read())
        return res
    except urllib2.HTTPError,e:
        return {'error': e.code}

class User:

    id = None
    nick = None
    feeds = None
    auth = None

    def __init__(self,jiepanguser,auth):
        self.id = jiepanguser['id']
        self.nick = jiepanguser['nick']
        self.auth = auth
        self.load_feeds()

    def load_feeds(self):
        if not self.feeds:
            feeds = db.feeds.find_one({'_id': self.id})
            if not feeds:
                self.reload_feeds()
            else:
                self.feeds = feeds['data']
        last_feed_id = self.feeds[0]['id'] if self.feeds else 0
        params = {'apiver': 3, 'types': 'checkin,tip,shout,schedule,photo'}
        while 1:
            if last_feed_id:
                params['since_id'] = last_feed_id
            res = call_api('events/list',params,self.auth)['items']
            if 'error' not in res:
                break
        res.extend(self.feeds)
        self.feeds = res
        db.feeds.update({'_id': self.id},{'$set': {'data': res}})


    def reload_feeds(self):
        print 'loading feeds'
        max_id = 0
        feeds = []
        page = 1
        params = {'apiver': 3, 'types': 'checkin,tip,shout,schedule,photo'}
        while 1:
            print 'Page:%d' % page
            params['page'] = page
            if max_id:
                params['max_id'] = max_id
            res = call_api('events/list',params,self.auth)['items']
            if 'error' in res:
                time.sleep(1)
                continue
            if not res or page > 20:
                break
            feeds.extend(res)
            max_id = res[-1]['id']
            page+=1

        self.feeds = feeds
        db.feeds.insert({'_id': self.id},{'data': feeds})


def get_voice(text='你妹'):
    request = urllib2.Request('http://translate.google.com/translate_tts?ie=UTF-8&tl=zh-CN&q=' + text, headers={'User-Agent' : "Magic Browser"})
    #opener = urllib2.build_opener(urllib2.HTTPHandler(debuglevel=0))
    #response = opener.open(request)
    try:
    	con = urllib2.urlopen(request)
    except urllib2.HTTPError, e:
        print e.fp.read()
    return con.read()
    #return urllib2.urlopen('http://translate.google.com/translate_tts?ie=UTF-8&q=%E4%BD%A0%E4%BB%96%E5%A6%88%E7%9A%84&tl=zh-CN').read()

# words.append(user['nick'])
# words.append(user['name'])

# while 1:
    # max_id = None
    # feeds = []
    # page = 1
    # while 1:
        # print 'Page:%d' % page
        # params['page'] = page
        # if max_id:
            # params['max_id'] = max_id
        # res = call_api('events/list',params,auth)['items']
        # if not res or page > 20:
            # break
        # feeds.extend(res)
        # max_id = res[-1]['id']
        # page+=1

    # for feed in feeds:
        # if not 'status' in feed:
            # continue
        # body = feed['status']['body']
        # go_deeper = True
        # for word in words:
            # if word in body:
                # go_deeper = False
                # print u'有人发状态提到你：%s' % body
                # break
        # if go_deeper:
            # comments = call_api('comments/list',{'source':'hitme','id':feed['status']['id']},'',0)
            # for comment in comments['items']:
                # for word in words:
                    # if word in comment['body']:
                        # print u'有人发回复时提到你：%s。原文：%s' % (comment['body'],comments['post']['body'])
                        # break

    # print 'sleeping'
    # time.sleep(120)

