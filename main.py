# -*- coding: utf-8 -*-
import bottle
bottle.debug(True)

from bottle import *
from commons import *
import datetime

#内部

def _verify_credentials():
    auth = request.get_cookie("jiepangauth", secret='jiepangx@pp')
    if auth:
        user = call_api('v1/account/verify_credentials',{},auth)
        if 'error' in user:
            response.set_cookie("jiepangauth", "", secret='jiepangx@pp',expires=datetime.datetime.utcnow())
        else:
            return user
    return False

#静态文件
from bottle import static_file
@route('/static/:path#.+#')
def server_static(path):
    return static_file(path, root='./static')

#网页

@route('/')
@get('/index')
def index_form():
    if _verify_credentials():
        redirect('/home')
    return mako_template('index')

@post('/index')
def index_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    auth = base64.encodestring('%s:%s' % (username,password))
    user = call_api('v1/account/verify_credentials',{},auth)
    if 'error' in user and user['error'] == 401:
        abort(401, u'Username/Password Error')
    response.set_cookie("jiepangauth", auth, secret='jiepangx@pp')
    redirect("/home?words=1")

@route('/home')
def home():
    userdata = _verify_credentials()
    if not userdata:
        redirect('/')
    user = User(userdata,request.get_cookie("jiepangauth", secret='jiepangx@pp'))
    rlt = []
    words = [item['w'] for item in db.words.find({'u': userdata['id'],'status':1})]
    for feed in user.feeds:
        feed['header'] = types[feed['type']] % (feed['user']['nick'],'location' in feed and feed['location']['name'] or '')
        if request.GET.get('words'):
            toadd = False
            for word in words:
                if word in feed['body']:
                    feed['body'] = feed['body'].replace(word,'<span style="color:%s">%s</span>' % (random.choice(colors),word))
                    toadd = True
            if toadd:
                rlt.append(feed)
        else:
            rlt.append(feed)

    return mako_template('home', nick=user.nick, feeds=rlt)

@route('/voice')
def voice():
    import urllib
    response.content_type = 'audio/mpeg'
    response.body = get_voice()
    #response.body = 'http://translate.google.com/translate_tts?ie=UTF-8&q=%E4%BD%A0%E4%BB%96%E5%A6%88%E7%9A%84&tl=zh-CN'
    return

@route('/logout')
def logout():
    response.set_cookie("jiepangauth", "", secret='jiepangx@pp',expires=datetime.datetime.utcnow())
    redirect('/')

@route('/settings')
def settings():
    userdata = _verify_credentials()
    if not userdata:
        redirect('/')
    words = []
    cursor = db.words.find({'u': userdata['id']})
    for item in cursor:
        print item
        words.append({'word': item['w'], 'status': item['status'], 'created_on': datetime.datetime.strftime(item['c'] + datetime.timedelta(hours=8),'%m/%d %H:%M:%S'), 'id': item['_id']})
    #left panel - 最后在前
    #right panel - 最后三个，最后在后。
    # right = words[-3:]
    # right.reverse()
    return mako_template('settings',left=words)

@route('/settings/add/:word')
def add_word(word):
    word = word.strip()
    userdata = _verify_credentials()
    if not userdata:
        redirect('/')
    if db.words.find_one({'w': word,'u': userdata['id']}):
        return 'false'
    now = datetime.datetime.utcnow()
    db.words.insert({'w': word,'u': userdata['id'],'c': now,'status':1})
    nowstr = datetime.datetime.strftime(now + datetime.timedelta(hours=8),'%m/%d %H:%M:%S')
    return json_encode({'w': word, 'c': nowstr})

@route('/settings/delete/:word')
def delete_word(word):
    word = word.strip()
    userdata = _verify_credentials()
    if not userdata:
        redirect('/')
    if not db.words.find_one({'w': word,'u': userdata['id']}):
        return 'false'
    db.words.remove({'w': word,'u': userdata['id']})
    return 'true'

@route('/settings/update/:word/:status')
def update_word(word,status):
    word = word.strip()
    status = int(status)
    if status != 0:
        status = 1
    print word,status
    userdata = _verify_credentials()
    if not userdata:
        redirect('/')
    if not db.words.find_one({'w': word,'u': userdata['id']}):
        return 'false'
    db.words.update({'w': word,'u': userdata['id']},{'$set':{'status':status}})
    return 'true'

@error(404)
def error404(error):
    return u"You can't find it here, look another way. You can't find it here, try another day."

