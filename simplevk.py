import logging
import json
import time
from html.parser import HTMLParser
try:
    import requests
except ImportError:
    print('установите библиотеку requests')
import requests



app_id = ''
user_id = ''
access_token = ''
v = '5.64'


def authorize(app_id, login, password, scope, v=v):
    global user_id
    global access_token

    with requests.Session() as vk_session:
        r = vk_session.get('https://oauth.vk.com/authorize?client_id='+app_id+'&display=page&redirect_uri=https://vk.com&scope='+scope+'&response_type=token&v='+v)
        p = vkParser()
        p.feed(r.text)
        p.close()
        p.login_data['email'] = login
        p.login_data['pass'] = password
            
        if p.method == 'get':
            r = vk_session.get(p.url, params=p.login_data)
        elif p.method == 'post':
            r = vk_session.post(p.url, data=p.login_data)
        if r.url.find('access_token=') >= 0:
            access_token = r.url.partition('access_token=')[2].split('&')[0]
            user_id = r.url.partition('user_id=')[2]
        else:
            p = vkParser()
            p.feed(r.text)
            p.close()
            if p.method == 'get':
                r = vk_session.get(p.url)
            if p.method == 'post':
                r = vk_session.post(p.url)
            access_token = r.url.partition('access_token=')[2].split('&')[0]
            user_id = r.url.partition('user_id=')[2]
        if not user_id:
            raise AuthorizationError('Неправильный логин или пароль')
                
                
                
def request(method, params=''):
    access_param = '&access_token='+str(access_token) if access_token else ''
    api_request = requests.get('https://api.vk.com/method/'+method+'?'+params+access_param+'&v='+str(v))
    return api_request.json()


def encode_cyrilic(text):
    return str(text.encode("utf-8")).replace("\\x", "%")[2:-1]
        
        
        
class vkParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.login_data = {}
        self.method = "GET"
        self.url = ""
        
    def handle_starttag(self, tag, atribs):
        attrs = {}
        for attr in atribs:
            attrs[attr[0]] = attr[1]
        if tag == 'form':
            self.url = attrs['action']
            if 'method' in attrs:
                self.method = attrs['method']
        elif tag == 'input' and 'name' in attrs:
            self.login_data[attrs['name']] = attrs['value'] if 'value' in attrs else ""
            
            
            
class AuthorizationError(Exception):
    def __init__(self, value):
        self.value = value


