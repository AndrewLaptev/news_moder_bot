import os
import logging
import json
from datetime import datetime
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup,InlineQueryResultArticle, InputTextMessageContent, ParseMode
from telegram.ext import Updater, CallbackQueryHandler, MessageHandler, Filters, CallbackContext, InlineQueryHandler, ConversationHandler, CommandHandler
from uuid import uuid4
import requests

LOG_FOLDER = "../log/bot_news"
NEWS_PATTERN = "../data/message_patterns/news_pattern.json"

# логируем все в файлик
os.makedirs(LOG_FOLDER, exist_ok=True)
logging.basicConfig(
    filename=LOG_FOLDER + f"/bot_news{datetime.utcnow().strftime('%Y%m%d-%H%M%S%f')}.log",
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)
logger = logging.getLogger(__name__)

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# в качестве шаблона сообщения берется пустой JSON
with open(NEWS_PATTERN) as f:
    news_pattern = json.load(f)

def title_filter(title: str):
    '''
    Фильтрует все ненужные символы в заголовке новости (требует расширения фильтров)
    '''
    for v in title.split(" "):
        if '#' in v:
            title = title.replace(v + ' ', '')
    return title

def convert_json(news_pattern: dict, src_news: dict):
    '''
    Выполняет конвертацию из формата сообщения телеграма в нужный нам формат новости
    '''
    news = news_pattern
    text_split = src_news["text"].split('\n')
    news['payload']['title'] = title_filter(text_split[1])
    news['payload']['authors'] = list([text_split[0]])
    news['payload']['date'] = datetime.utcfromtimestamp(int(src_news['date'])).strftime('%Y-%m-%dT00:00:00')
    news['payload']['pdf_url'] = src_news["entities"][0]["url"]
    news['payload']['abstract'] = '\n'.join(text_split[2::])
    return news

def button_handler(update: Update, context: CallbackContext) -> None:
    '''
    Обработчик кнопок `Markup`, `Add` и `Delete`. Планируется добавить кнопку `Edit`, по возможности
    '''
    query = update.callback_query
    query.answer()
    print(json.dumps(json.loads(query.message.to_json()), sort_keys=True, indent=4, ensure_ascii=False))
    news_tmp = convert_json(news_pattern, json.loads(query.message.to_json()))
    if query.data == "markup": # ломает гиперссылки в абстракте, надо поправить
        # производит автоматическую разметку сообщения на Title и Abstract (поля в требуемом формате новостей news_pattern.json)
        source = '<strong><a href="' + news_tmp['payload']['pdf_url'] + '">' + news_tmp['payload']['authors'][0] + '</a></strong>\n'
        title = '<b>Title</b>:\n' + news_tmp['payload']['title']
        abstract = '\n\n<b>Abstract</b>:\n' + news_tmp['payload']['abstract']
        query.message = query.edit_message_text(source + title + abstract, parse_mode='html')
        keyboard = [[InlineKeyboardButton('Add', callback_data='added'), InlineKeyboardButton('Delete',callback_data='deleted')], 
                    [InlineKeyboardButton('Edit', switch_inline_query_current_chat = str(query.message.message_id) + '\n' + str(query.message.text_html))]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_reply_markup(reply_markup=reply_markup)
    
    if query.data == "added":
        clean_src_dict = json.loads(query.message.to_json())
        print(clean_src_dict['text'])
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

def inlinequery(update: Update, context: CallbackContext) -> None:
    """Handle the inline query."""
    query = update.inline_query.query
    if query == "":
        return
    else:
        results = [
            InlineQueryResultArticle(
                id=str(uuid4()),
                title="Apply",
                input_message_content=InputTextMessageContent(query, parse_mode=ParseMode.HTML),
            ),
            # InlineQueryResultArticle(
            #     id=str(uuid4()),
            #     title="Cancel",
            #     input_message_content=InputTextMessageContent(query, parse_mode=ParseMode.HTML),
            # ),
        ]
    update.inline_query.answer(results)

def edit_message_handler(update: Update, context: CallbackContext) -> None:
    if update.message.via_bot == None:
        return
    elif update.message.via_bot['is_bot'] == True:
        print(update.message.text_html)
        #print(telegram_bot_delete_news(BOT_TOKEN, BOT_CHAT_ID, 708))

def start(update: Update, context: CallbackContext):
    pass


def bot_news_start() -> None:
    updater = Updater(BOT_TOKEN)

    # conv_handler = ConversationHandler(
    #     entry_points=[CommandHandler('start', start)],
    #     states={
    #         FIRST: [
    #             CallbackQueryHandler(one, pattern='^' + str(ONE) + '$'),
    #             CallbackQueryHandler(two, pattern='^' + str(TWO) + '$'),
    #             CallbackQueryHandler(three, pattern='^' + str(THREE) + '$'),
    #             CallbackQueryHandler(four, pattern='^' + str(FOUR) + '$'),
    #         ],
    #         SECOND: [
    #             CallbackQueryHandler(start_over, pattern='^' + str(ONE) + '$'),
    #             CallbackQueryHandler(end, pattern='^' + str(TWO) + '$'),
    #         ],
    #     },
    #     fallbacks=[CommandHandler('start', start)],
    # )

    # updater.dispatcher.add_handler(conv_handler)
    updater.dispatcher.add_handler(CallbackQueryHandler(button_handler))
    updater.dispatcher.add_handler(InlineQueryHandler(inlinequery))
    updater.dispatcher.add_handler(MessageHandler(Filters.all, edit_message_handler))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    bot_news_start()