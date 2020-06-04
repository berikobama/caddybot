import telepot
import time
import os
from logic.vrm import VRM_API
from flask import Flask, request
import telegram
from logic.util import *

global bot
global token

token = os.environ['telegram_token']
vrm_user = os.environ['vrm_user']
vrm_pass = os.environ['vrm_pass']
users = os.environ["users"].split(";")
solar_id = os.environ['solar_id']
bmv_id = os.environ['bmv_id']
site_id = os.environ['site_id']

bot = telegram.Bot(token=token)

app = Flask(__name__)

@app.route('/{}'.format(token), methods=['POST'])
def respond():
    # retrieve the message in JSON and then transform it to Telegram object
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    api = VRM_API(username=vrm_user, password=vrm_pass)
    
    chat_obj = update["message"]["chat"]
    chat_id = chat_obj["id"]
    chat_message = update["message"]["text"]

    if chat_obj["username"] in users:
        if chat_message == "?":
            bot.sendMessage(chat_id, get_google_maps_url(api))
        elif chat_message.lower() == "status":
            val_str = collect_fields(
                api.battery_summary_widget,
                50134,
                bmv_id,
                ["47", "49", "50", "51", "115"])
            bot.sendMessage(chat_id, val_str)
        elif chat_message.lower() == "solar":
            val_str = collect_fields(
                api.solar_charger_summary_widget,
                50134,
                solar_id,
                ["85", "94", "96", "107"])
            bot.sendMessage(chat_id, val_str)
        else:
            bot.sendMessage(chat_id, "Nein, Dill..")
    else:
        print(update)

    return 'ok'

@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.setWebhook('{URL}{HOOK}'.format(URL="https://ecaddybot.herokuapp.com/", HOOK=token))
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"

@app.route('/')
def index():
    return '.'


if __name__ == '__main__':
    app.run(threaded=True)