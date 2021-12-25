import os
from datetime import datetime
from dotenv import load_dotenv
import requests
import json
import logging
from telethon import TelegramClient, events

# Теперь можно запускать из любой директории проекта, т.к. файлы будут доступны через абсолютные пути
PROJECT_PATH = os.path.abspath(__file__).split("/app", 1)[0]
LOG_FOLDER = f"{PROJECT_PATH}/log/extractor"
CHANNEL_LIST = f"{PROJECT_PATH}/data/channel_list.txt"

# логируем все в файлик
os.makedirs(LOG_FOLDER, exist_ok=True)
logging.basicConfig(
    filename=LOG_FOLDER + f"/extractor{datetime.utcnow().strftime('%Y%m%d-%H%M%S%f')}.log",
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

load_dotenv()
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_CHAT_ID = os.getenv("BOT_CHAT_ID")
client = TelegramClient('session_name', API_ID, API_HASH)
client.parse_mode = 'html'
channel_list = []

with open(CHANNEL_LIST) as f:
    for line in f:
        channel_list.append(line.replace("\n",""))

def telegram_bot_send_news(bot_token: str, bot_chatID: str, news_text):
    '''
    Отправляет сообщение (с кнопками) в чат бота напрямую POST запросом через API_ID и API_HASH
    '''
    text = news_text.replace('"',r'\"')
    headers = {'Content-Type': 'application/json; charset=utf-8',}
    data1 = '{' + f'"chat_id":"{bot_chatID}", "parse_mode":"html", "text":"{text}", "reply_markup": ' + '{'
    data2 = '"inline_keyboard": [[{"text":"Markup", "callback_data": "markup"}]]} }'
    data = data1 + data2
    response = requests.post(f'https://api.telegram.org/bot{bot_token}/sendMessage', headers=headers, data=data.encode('utf-8'))
    return json.dumps(response.json(), sort_keys=True, indent=4, ensure_ascii=False)

@client.on(events.NewMessage(chats = channel_list[0]))
async def news_event_handler(event):
    channel_name = f'<strong><a href="{channel_list[0]}/{event.id}">' + str(event.chat.title) + '</a></strong>\n'
    print(telegram_bot_send_news(BOT_TOKEN, BOT_CHAT_ID, channel_name + event.text))

def extractor_news_start() -> None:
    client.start()
    client.run_until_disconnected()
    print(client.list_event_handlers())

if __name__ == "__main__":
    extractor_news_start()