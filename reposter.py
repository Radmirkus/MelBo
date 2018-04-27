import botmemory
import simplevk
import logging
import time



logging.basicConfig(format=u' %(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level=logging.DEBUG, filename='reposter.log')
vk = ""


def start(vk_s):
    global vk
    vk = vk_s
    print('Reposter started')
    while True:
        repostSmthInterest()
        time.sleep(900)


def repostSmthInterest():
    news = vk.request('newsfeed.get','filters=post&source_ids=groups')['response']['items']
    best_post = [0.0, '']
    print("Finding good news..")
    for post in news:
        likes = ""
        views = ""
        try:
            likes = post['likes']['count']
            views = post['views']['count']
        except KeyError:
            continue
        interest_factor = likes/views
        if interest_factor>best_post[0]:
            best_post[1] = 'wall'+str(post['source_id'])+"_"+str(post['post_id'])  #post link
    print("Reposting")
    vk.request('wall.repost', 'object='+best_post[1])