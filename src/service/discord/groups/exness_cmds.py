
import logging
import json
import requests
import discord
from discord import app_commands


# Group :
class GroupExness(app_commands.Group):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'exness'
        self.description = 'Exness API'


    # amount is not a required argument, so it will default to None if not provided
    @app_commands.command(name="balance", description="Update or Get Exness balance")
    async def balance(self, interaction: discord.Interaction, amount: int = 0):
        try:
            if amount is None or amount <= 0:
                # res = requests.get('http://localhost:5100/api/v1/exness/balance')    
                res = {"balance": 1000}
                await interaction.response.send_message(f'Get Exness balance: {json.dumps(res, indent=4)}')
            else:
                # res = requests.post('http://localhost:5100/api/v1/exness/balance', json={"amount": amount})  
                # res = res.json()
                res = {"balance": 1000}
                await interaction.response.send_message(f'Update Exness balance: {json.dumps(res, indent=4)}')
        except Exception as e:
            logging.error(f"Exception: {e}")


    @app_commands.command(name="withdraw", description="Withdraw funds from Exness")
    async def withdraw(self, interaction: discord.Interaction, amount: int):
        try:
            res = requests.post('http://localhost:5100/api/v1/exness/withdraw', json={"amount": amount})  
            await interaction.response.send_message(f'Withdraw {amount} USDT from Exness: {res.json()}')
        except Exception as e:
            logging.error(f"Exception: {e}")


    @app_commands.command(name="deposit", description="Deposit funds into Exness")
    async def deposit(self, interaction: discord.Interaction, amount: int):
        try:
            await interaction.response.send_message(f'Deposit {amount} USDT into Exness')
        except Exception as e:
            logging.error(f"Exception: {e}")


    @app_commands.command(name="help", description="List available commands", nsfw=True) # nsfw=True means that the command can only be used in NSFW channels. NSFW channels are channels that have been marked as not safe for work.
    async def help(self, interaction: discord.Interaction):
        try:
            command_list = [command.name for command in self.commands]
            command_descriptions = [command.description for command in self.commands]
            command_info = '\n'.join([f"`/{command} - {description}`" for command, description in zip(command_list, command_descriptions)])
            embed = discord.Embed(title="Exness Bot Commands", description=command_info, color=0x00ff00)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            logging.error(f"Exception: {e}")


    @app_commands.command(name="ping", description="Ping Exness API")
    async def ping(self, interaction: discord.Interaction):
        try:
            res = requests.get('http://localhost:5000/api/v1/exness/ping')    
            res = res.json()
            await interaction.response.send_message(json.dumps(res, indent=4), ephemeral=True)
        except Exception as e:
            logging.error(f"Exception: {e}")
