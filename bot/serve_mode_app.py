
# from flask import Flask, request as fl_request
# import telepot
import telepot
import urllib3
import traceback
# from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import json

import time
import pickle
import os
from settings import BOT_KEY, PORT
from bot.handlers import FinacialHandler
proxy_url = "http://proxy.server:{}".format(PORT)
telepot.api._pools = {
    'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
}
telepot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))


bot = telepot.Bot(BOT_KEY)

def handle(msg):
    handler = FinacialHandler(msg, bot)
    handler.handle()

def run():

    if os.path.exists('state.pickle'):
            with open('state.pickle', 'rb') as state_pickle:
                state = pickle.load(state_pickle)
                print('load:', state)
    else:
        state = dict(last_id=0)
    while 1:
        
        try:
            
            response = bot.getUpdates()
            for r in response:
                if state['last_id'] >= r['update_id']:
                    continue

                handler = FinacialHandler(r, bot)
                handler.handle()

                state['last_id'] = r['update_id']
                with open('state.pickle', 'wb') as state_pickle:
                    print('dump:', state)
                    pickle.dump(state, state_pickle)
    
        except KeyboardInterrupt:
            print('CLOSE')
            exit()

        time.sleep(3)
    
if __name__ == '__main__':
    run()