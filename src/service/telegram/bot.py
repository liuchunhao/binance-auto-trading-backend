#!/usr/bin/env python
# pylint: disable=C0116,W0613

"""
Simple Bot to send timed Telegram messages.

This Bot uses the Updater class to handle the bot and the JobQueue to send
timed messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Alarm Bot example, sends a message after a set time.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
from dotenv import load_dotenv
import os

from telegram import Update
from telegram.ext import Application
from telegram.ext import Updater, CommandHandler, CallbackContext

logger = logging.getLogger(__name__)
load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')
TOKEN = TOKEN if TOKEN else ""

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
# Best practice would be to replace context with an underscore,
# since context is an unused local variable.
# This being an example and not having context present confusing beginners,
# we decided to have it present as context.



async def start(update: Update, context: CallbackContext) -> None:
    """Sends explanation on how to use the bot."""
    if update.message is not None:
        await update.message.reply_text('Hi! Use /set <seconds> to set a timer')
        logger.info(f'update.message: {update.message}')

from typing import Any, Coroutine

async def alarm(context: CallbackContext) -> None:
    """Send the alarm message."""
    job = context.job
    if job is not None:
        context.bot.send_message(job.context, text='Beep!')
        logger.info(f'job.context: {job.context}')


def remove_job_if_exists(name: str, context: CallbackContext) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    queue = context.job_queue
    if queue is not None:
        current_jobs = queue.get_jobs_by_name(name)
        if current_jobs is not None:
            for job in current_jobs:
                job.schedule_removal()
                logger.info(f'job: {job}')
    return True


async def set_timer(update: Update, context: CallbackContext) -> None:
    """Add a job to the queue."""
    message = update.message
    if message is not None:
        try:
                chat_id = message.chat_id
                # args[0] should contain the time for the timer in seconds
                context.args = context.args if context.args is not None else []
                due = int(context.args[0])
                if due < 0:
                    await message.reply_text('Sorry we can not go back to future!')
                    logger.info(f'due: {due}')
                    return

                job_removed = remove_job_if_exists(str(chat_id), context)
                job_queue = context.job_queue
                if job_queue is not None:
                    job_queue.run_once(alarm, due, chat_id=chat_id, name=str(chat_id))

                text = 'Timer successfully set!'
                if job_removed:
                    text += ' Old one was removed.'
                await message.reply_text(text)
        except (IndexError, ValueError):
            await message.reply_text('Usage: /set <seconds>')


async def unset(update: Update, context: CallbackContext) -> None:
    """Remove the job if the user changed their mind."""
    message = update.message
    if message is not None:
        chat_id = message.chat_id
        job_removed = remove_job_if_exists(str(chat_id), context)
        text = 'Timer successfully cancelled!' if job_removed else 'You have no active timer.'
        await message.reply_text(text)


def run() -> None:
    """Run bot"""
    # Create the Updater and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # Commands
    application.add_handler(CommandHandler(["start", "help"], start))
    application.add_handler(CommandHandler("set", set_timer))
    application.add_handler(CommandHandler("unset", unset))

    # Run bot:
    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    application.run_polling() 


if __name__ == '__main__':
    run()
