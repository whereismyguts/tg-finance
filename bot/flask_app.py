from flask import Flask, request as fl_request
import telepot
import urllib3
import traceback
from trello_parser import get_status
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import json
from settings import *
from to_implement.handlers import FinacialHandler

proxy_url = "http://proxy.server:{}".format(PORT)
telepot.api._pools = {
    'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
}
telepot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))

bot = telepot.Bot(BOT_KEY)
bot.setWebhook("https://whereismyguts.pythonanywhere.com/{}".format(FLASK_SECRET), max_connections=5)

app = Flask(__name__)

# from to_implement.handlers import FinacialHandler

@app.route('/{}'.format(FLASK_SECRET), methods=["POST"])
def telegram_webhook():
    handler = FinacialHandler(fl_request.get_json(), bot)
    return handler.handle()