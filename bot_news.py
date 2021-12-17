import os
import logging
import json
from datetime import datetime
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Updater, CallbackQueryHandler, CallbackContext

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

with open("news_pattern.json") as f:
    news_pattern = json.load(f)


def convert_json(news_pattern: dict, src_news: dict):
    news = news_pattern
    text_split = src_news["text"].split('\n\n')
    news['payload']['title'] = text_split[1]
    news['payload']['authors'] = list([text_split[0]])
    news['payload']['date'] = datetime.utcfromtimestamp(int(src_news['date'])).strftime('%Y-%m-%dT00:00:00')
    news['payload']['pdf_url'] = src_news["entities"][0]["url"]
    news['payload']['abstract'] = '\n\n'.join(text_split[2::])
    return news

def button_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()
    if query.data == "added":
        f = open("test_news.json", "a")
        news = convert_json(news_pattern, json.loads(query.message.to_json()))
        f.write(json.dumps(news, sort_keys=True, indent=4, ensure_ascii=False) + '\n')
        f.close
    query.edit_message_text(text=f"Current news: {query.data}")

def main() -> None:
    # Create the Updater and pass it your bot's token.
    updater = Updater(BOT_TOKEN)
    updater.dispatcher.add_handler(CallbackQueryHandler(button_handler))
    # Start the Bot
    updater.start_polling()
    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()