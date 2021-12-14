from telegram.base import TO
from telegram.ext import Updater, CommandHandler
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext

USAGE = '/greet <name> - Greet me!'


def start(update: Update, context: CallbackContext):
    update.message.reply_text(USAGE)

def greet_command(update: Update, context: CallbackContext):
    update.message.reply_text(f'Hello {context.args[0]}!')

def send_news(update: Update, context: CallbackContext, text: str):
    update.message.reply_text(redact_text(text), parse_mode='Markdown')

def redact_text(text: str):
    return text.replace("**", "***")