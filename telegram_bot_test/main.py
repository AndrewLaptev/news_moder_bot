from telegram.ext import Updater, CommandHandler
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext

USAGE = '/greet <name> - Greet me!'


def start(update: Update, context: CallbackContext):
    update.message.reply_text(USAGE)


def greet_command(update: Update, context: CallbackContext):
    update.message.reply_text(f'Hello {context.args[0]}!')

def send_msg(update: Update, context: CallbackContext):
    update.message.reply_text(redact_text(MSG), parse_mode='Markdown')


def main():
    updater = Updater("5003522949:AAEkdzUD9RHnHOPKbTP_l_BhEvH0PlZ8dm0", use_context=True)
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("greet", greet_command))
    dp.add_handler(CommandHandler("msg", send_msg))

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()