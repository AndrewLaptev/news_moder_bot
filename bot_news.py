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
    news_tmp = convert_json(news_pattern, json.loads(query.message.to_json()))

    if query.data == "markup": # ломает ссылки в абстракте, надо поправить
        source = '<strong><a href="' + news_tmp['payload']['pdf_url'] + '">' + news_tmp['payload']['authors'][0] + '</a></strong>\n'
        title = '<b>Title</b>:\n' + news_tmp['payload']['title']
        abstract = '\n\n<b>Abstract</b>:\n' + news_tmp['payload']['abstract']
        query.edit_message_text(source + title + abstract, parse_mode='html')
        keyboard = [[InlineKeyboardButton('Add', callback_data='added'), InlineKeyboardButton('Delete',callback_data='deleted')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_reply_markup(reply_markup=reply_markup)
    
    if query.data == "added":
        clean_src_dict = json.loads(query.message.to_json())
        clean_src_dict['text'] = clean_src_dict['text'].replace("Title:\n", "").replace("\nAbstract:\n", "")
        news = convert_json(news_pattern, clean_src_dict)
        ######### сюда можно вписать
        f = open("test_news.json", "a")
        f.write(json.dumps(news, sort_keys=True, indent=4, ensure_ascii=False) + '\n')
        f.close
        ######### любой нужный метод отправки новости
        query.delete_message()
    
    elif query.data == "deleted":
        query.delete_message()


def main() -> None:
    updater = Updater(BOT_TOKEN)
    updater.dispatcher.add_handler(CallbackQueryHandler(button_handler))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()