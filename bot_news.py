import os
import logging
import json
from datetime import datetime
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CallbackQueryHandler, CallbackContext

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

with open("news_pattern.json") as f:
    news_pattern = json.load(f)

def title_filter(title: str):
    for v in title.split(" "):
        if '#' in v:
            title = title.replace(v + ' ', '')
    return title

def convert_json(news_pattern: dict, src_news: dict):
    news = news_pattern
    text_split = src_news["text"].split('\n')
    news['payload']['title'] = title_filter(text_split[1])
    news['payload']['authors'] = list([text_split[0]])
    news['payload']['date'] = datetime.utcfromtimestamp(int(src_news['date'])).strftime('%Y-%m-%dT00:00:00')
    news['payload']['pdf_url'] = src_news["entities"][0]["url"]
    news['payload']['abstract'] = '\n'.join(text_split[2::])
    return news

def button_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    news = convert_json(news_pattern, json.loads(query.message.to_json()))
    if query.data == "markup":
        # news = convert_json(news_pattern, json.loads(query.message.to_json()))
        # print(json.dumps(json.loads(query.message.to_json()), sort_keys=True, indent=4, ensure_ascii=False))
        query.edit_message_text('<b>Title</b>:\n' + news['payload']['title'] + '\n\n<b>Abstract</b>:\n' + news['payload']['abstract'], parse_mode='html')
        # print(query.message.text_html)

        keyboard = [[InlineKeyboardButton('Add',callback_data='added'), InlineKeyboardButton('Delete',callback_data='deleted')], 
                    [InlineKeyboardButton('Edit',callback_data='edit')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_reply_markup(reply_markup=reply_markup)
    if query.data == "added":
        f = open("test_news.json", "a")
        f.write(json.dumps(news, sort_keys=True, indent=4, ensure_ascii=False) + '\n')
        f.close
        query.delete_message()
    elif query.data == "deleted":
        query.delete_message()
    elif query.data == "edit":
        keyboard = [[InlineKeyboardButton('Title',callback_data='title')], [InlineKeyboardButton('Abstract',callback_data='abstract')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_reply_markup(reply_markup=reply_markup)

def main() -> None:
    updater = Updater(BOT_TOKEN)
    updater.dispatcher.add_handler(CallbackQueryHandler(button_handler))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()