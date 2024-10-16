#!/usr/bin/env python

from server import linebot_server 
from service.discord import bot as discord_bot
from threading import Thread

from controller.exness_controller import check_mobile_alive

def run_discord_bot():
    discord_bot.start()

if __name__ == '__main__':
    discord_thread = Thread(target=run_discord_bot)
    discord_thread.start()

    Thread(target=check_mobile_alive).start()

    # [IMPORTANT] If you set debug=False, you should get only one instance of Python per Flask app.
    linebot_server.app.run(host="0.0.0.0", port=5000, debug=False) 