import os
from dotenv import load_dotenv
import requests
import json
import logging
from telethon import TelegramClient, events

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

load_dotenv()
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_CHAT_ID = os.getenv("BOT_CHAT_ID")
client = TelegramClient('session_name1', API_ID, API_HASH)
channel_dict = {
    'test':'https://t.me/testglobalavatar',
    'test1':'https://t.me/tegetge',
}

def telegram_bot_send_news(bot_token: str, bot_chatID: str, news_text: str, button1_name: str, button1_callback_data: str, button2_name: str, button2_callback_data: str):
    headers = {'Content-Type': 'application/json; charset=utf-8',}
    data1 = '{' + f'"chat_id":"{bot_chatID}", "parse_mode":"Markdown", "text":"{news_text}", "reply_markup": ' + '{'
    data2 = '"inline_keyboard": [[' + '{' + f'"text":"{button1_name}", "callback_data": "{button1_callback_data}"' + '},{'
    data3 = f'"text":"{button2_name}", "callback_data": "{button2_callback_data}"' + '}]]} }'
    data = data1 + data2 + data3
    response = requests.post(f'https://api.telegram.org/bot{bot_token}/sendMessage', headers=headers, data=data.replace("**", "***").encode('utf-8'))
    return json.dumps(response.json(), ensure_ascii=False)

@client.on(events.NewMessage(chats = channel_dict.get('test')))
async def news_event_handler(event):
    channel_name = '[' + str(event.chat.title).upper() + ']' + f"({channel_dict.get('test')})\n\n"
    print(telegram_bot_send_news(BOT_TOKEN, BOT_CHAT_ID, channel_name + event.text, "Add", "added", "Delete", "deleted"))

@client.on(events.NewMessage(chats = channel_dict.get('test1')))
async def news_event_handler(event):
    channel_name = '[' + str(event.chat.title).upper() + ']' + f"({channel_dict.get('test1')})\n\n"
    print(telegram_bot_send_news(BOT_TOKEN, BOT_CHAT_ID, channel_name + event.text, "Add", "added", "Delete", "deleted"))


if __name__ == "__main__":
    client.start()
    client.run_until_disconnected()