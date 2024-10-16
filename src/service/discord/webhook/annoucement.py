
from discord import SyncWebhook
from discord import Webhook
import os
import dotenv
import logging

dotenv.load_dotenv()   

channel = 'announcement'
url = os.getenv('DISCORD_WEBHOOK_ANNOUNCEMENT', default='')
webhook = SyncWebhook.from_url(url)


def send(msg: str):
    try:
        webhook.send(msg)
        logging.info(f"Discord webhook message sent successfully|#{channel}: {msg}")
    except Exception as e:
        logging.error(f"Exception: {e}")    


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s|%(levelname)-8s|%(message)s', datefmt='%Y%m%d %H:%M:%S')
    send(f'Hello, Discord webhook! This is a test message')
