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
    chat_message = update["message"]["text"].lower()

    commands = {
        "solar": handle_solar,
        "status": handle_status,
        "help": get_help,
        "?": handle_maps
        }

    if chat_obj["username"] in users:
        if chat_message in commands.keys():
            commands[chat_message](api, bot, chat_id, solar_id, site_id, bmv_id)
        else:
            bot.sendMessage(chat_id, "unrecognized command")
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