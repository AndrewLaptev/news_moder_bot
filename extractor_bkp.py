import os
from dotenv import load_dotenv
import requests
import json
import logging
from telethon import TelegramClient, events
import telethon

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
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

with open("channel_list.txt") as f:
    for line in f:
        channel_list.append(line.replace("\n",""))

def telegram_bot_send_news(bot_token: str, bot_chatID: str, news_text: str, btn_add_name: str, btn_delete_name: str):
    text = news_text.replace('"',r'\"')
    headers = {'Content-Type': 'application/json; charset=utf-8',}
    data1 = '{' + f'"chat_id":"{bot_chatID}", "parse_mode":"html", "text":"{text}", "reply_markup": ' + '{'
    data2 = '"inline_keyboard": [[' + '{' + f'"text":"{btn_add_name}", "callback_data": "added"' + '},{'
    data3 = f'"text":"{btn_delete_name}", "callback_data": "deleted"' + '}]]} }'
    data = data1 + data2 + data3
    response = requests.post(f'https://api.telegram.org/bot{bot_token}/sendMessage', headers=headers, data=data.replace("**", "***").encode('utf-8'))
    return json.dumps(response.json(), sort_keys=True, indent=4, ensure_ascii=False)

# for link in channel_list:
#"parse_mode":"Markdown"
#     @client.on(events.NewMessage(chats = link))
#     async def news_event_handler(event):
#         channel_name = '[' + str(event.chat.title) + ']' + f"({link}/{event.id})\n\n"
#         print(telegram_bot_send_news(BOT_TOKEN, BOT_CHAT_ID, channel_name + event.text, "Add", "Delete"))

@client.on(events.NewMessage(chats = channel_list[0]))
async def news_event_handler1(event):
    channel_name = f'<strong><a href="{channel_list[0]}/{event.id}">' + str(event.chat.title) + '</a></strong>\n'
    print(telegram_bot_send_news(BOT_TOKEN, BOT_CHAT_ID, channel_name + event.text, "Add", "Delete"))

@client.on(events.NewMessage(chats = channel_list[1]))
async def news_event_handler2(event):
    channel_name = f'<strong><a href="{channel_list[1]}/{event.id}">' + str(event.chat.title) + '</a></strong>\n'
    print(telegram_bot_send_news(BOT_TOKEN, BOT_CHAT_ID, channel_name + event.text, "Add", "Delete"))

@client.on(events.NewMessage(chats = channel_list[2]))
async def news_event_handler3(event):
    channel_name = f'<strong><a href="{channel_list[2]}/{event.id}">' + str(event.chat.title) + '</a></strong>\n'
    print(telegram_bot_send_news(BOT_TOKEN, BOT_CHAT_ID, channel_name + event.text, "Add", "Delete"))

@client.on(events.NewMessage(chats = channel_list[3]))
async def news_event_handler4(event):
    channel_name = f'<strong><a href="{channel_list[3]}/{event.id}">' + str(event.chat.title) + '</a></strong>\n'
    print(telegram_bot_send_news(BOT_TOKEN, BOT_CHAT_ID, channel_name + event.text, "Add", "Delete"))

@client.on(events.NewMessage(chats = channel_list[4]))
async def news_event_handler5(event):
    channel_name = f'<strong><a href="{channel_list[4]}/{event.id}">' + str(event.chat.title) + '</a></strong>\n'
    print(telegram_bot_send_news(BOT_TOKEN, BOT_CHAT_ID, channel_name + event.text, "Add", "Delete"))

@client.on(events.NewMessage(chats = channel_list[5]))
async def news_event_handler6(event):
    channel_name = f'<strong><a href="{channel_list[5]}/{event.id}">' + str(event.chat.title) + '</a></strong>\n'
    print(telegram_bot_send_news(BOT_TOKEN, BOT_CHAT_ID, channel_name + event.text, "Add", "Delete"))

@client.on(events.NewMessage(chats = channel_list[6]))
async def news_event_handler7(event):
    channel_name = f'<strong><a href="{channel_list[6]}/{event.id}">' + str(event.chat.title) + '</a></strong>\n'
    print(telegram_bot_send_news(BOT_TOKEN, BOT_CHAT_ID, channel_name + event.text, "Add", "Delete"))

@client.on(events.NewMessage(chats = channel_list[7]))
async def news_event_handler8(event):
    channel_name = f'<strong><a href="{channel_list[7]}/{event.id}">' + str(event.chat.title) + '</a></strong>\n'
    print(telegram_bot_send_news(BOT_TOKEN, BOT_CHAT_ID, channel_name + event.text, "Add", "Delete"))

@client.on(events.NewMessage(chats = channel_list[8]))
async def news_event_handler9(event):
    channel_name = f'<strong><a href="{channel_list[8]}/{event.id}">' + str(event.chat.title) + '</a></strong>\n'
    print(telegram_bot_send_news(BOT_TOKEN, BOT_CHAT_ID, channel_name + event.text, "Add", "Delete"))

@client.on(events.NewMessage(chats = channel_list[9]))
async def news_event_handler10(event):
    channel_name = f'<strong><a href="{channel_list[9]}/{event.id}">' + str(event.chat.title) + '</a></strong>\n'
    print(telegram_bot_send_news(BOT_TOKEN, BOT_CHAT_ID, channel_name + event.text, "Add", "Delete"))

@client.on(events.NewMessage(chats = channel_list[10]))
async def news_event_handler11(event):
    channel_name = f'<strong><a href="{channel_list[10]}/{event.id}">' + str(event.chat.title) + '</a></strong>\n'
    print(telegram_bot_send_news(BOT_TOKEN, BOT_CHAT_ID, channel_name + event.text, "Add", "Delete"))

@client.on(events.NewMessage(chats = channel_list[11]))
async def news_event_handler12(event):
    channel_name = f'<strong><a href="{channel_list[11]}/{event.id}">' + str(event.chat.title) + '</a></strong>\n'
    print(telegram_bot_send_news(BOT_TOKEN, BOT_CHAT_ID, channel_name + event.text, "Add", "Delete"))

@client.on(events.NewMessage(chats = channel_list[12]))
async def news_event_handler13(event):
    channel_name = f'<strong><a href="{channel_list[12]}/{event.id}">' + str(event.chat.title) + '</a></strong>\n'
    print(telegram_bot_send_news(BOT_TOKEN, BOT_CHAT_ID, channel_name + event.text, "Add", "Delete"))

@client.on(events.NewMessage(chats = channel_list[13]))
async def news_event_handler14(event):
    channel_name = f'<strong><a href="{channel_list[13]}/{event.id}">' + str(event.chat.title) + '</a></strong>\n'
    print(telegram_bot_send_news(BOT_TOKEN, BOT_CHAT_ID, channel_name + event.text, "Add", "Delete"))

@client.on(events.NewMessage(chats = channel_list[14]))
async def news_event_handler15(event):
    channel_name = f'<strong><a href="{channel_list[14]}/{event.id}">' + str(event.chat.title) + '</a></strong>\n'
    print(telegram_bot_send_news(BOT_TOKEN, BOT_CHAT_ID, channel_name + event.text, "Add", "Delete"))

@client.on(events.NewMessage(chats = channel_list[15]))
async def news_event_handler16(event):
    channel_name = f'<strong><a href="{channel_list[15]}/{event.id}">' + str(event.chat.title) + '</a></strong>\n'
    print(telegram_bot_send_news(BOT_TOKEN, BOT_CHAT_ID, channel_name + event.text, "Add", "Delete"))


if __name__ == "__main__":
    client.start()
    client.run_until_disconnected()
    print(client.list_event_handlers())