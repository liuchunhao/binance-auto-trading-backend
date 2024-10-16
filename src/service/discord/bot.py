import logging
import requests
import json
import dotenv
import os

from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands

from service.discord.groups.exness_cmds import GroupExness

dotenv.load_dotenv()

# Token can be obtained from the Discord Developer Portal
TOKEN = os.getenv('DISCORD_TOKEN', default='YOUR_DISCORD_TOKEN')
CHANNEL_ID = 'YOUR_CHANNEL_ID'

# intents: A list of intents to enable for the connection. If not given, defaults to all but the privileged ones.
bot = commands.Bot(command_prefix = "/", intents = discord.Intents.all())


@bot.event
async def on_ready():
    user = bot.user if bot.user else discord.ClientUser
    logging.info(f"User: {user.name}, ID: {user.id}")    # bot.user 屬性可以取得登入的機器人資訊
    try:
        # Add a group of commands
        bot.tree.add_command(GroupExness())                   

        slash = await bot.tree.sync()
        logging.info(f"載入 {len(slash)} 個斜線指令")
    except Exception as e:
        logging.error(f"Exception: {e}")
    

@bot.tree.command(name="hello", description="Say hello to the bot")
async def hello(interaction: discord.Interaction):
    try:
        await interaction.response.send_message(f"Hi, {interaction.user.mention}! How can I help you?", ephemeral=True) # ephemeral=True means that the message is only visible to the user who invoked the command
    except Exception as e:
        logging.error(f"Exception: {e}")


@bot.tree.command(name="sms", description="get Exness verification code")
async def sms(interaction: discord.Interaction):
    try:
        res = requests.get('http://localhost:5000/api/v1/exness/sms/verificationCode')    
        res = res.json()
        await interaction.response.send_message(json.dumps(res, indent=4), ephemeral=True)
    except Exception as e:
        logging.error(f"Exception: {e}")


@bot.tree.command(name="say")
@app_commands.describe(thing_to_say = "The message to say")
async def say(interaction: discord.Interaction, thing_to_say: str):
    try:
        await interaction.response.send_message(f'{interaction.user.mention} said: {thing_to_say}', ephemeral=True)  
    except Exception as e:
        logging.error(f"Exception: {e}")


def start():
    bot.run(TOKEN)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s|%(levelname)-8s|%(message)s', datefmt='%Y%m%d %H:%M:%S')
    start()

    # [Host your bot for free 24/7 on Lunes Hosting](https://www.youtube.com/watch?v=V1y9l6wcquM)
    # [How to Organize your Application Commands with Groups](https://www.youtube.com/watch?v=jTBN19Nm0h0)
    # [How to use Discord decorators for your slash commands!](https://www.youtube.com/watch?v=bp2D9-4JtIk)

    # [How To Add Autocompletion To Your Discord Slash Commands](https://www.youtube.com/watch?v=zSzFHxOkCfo)




