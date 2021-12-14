from telethon import TelegramClient, events
from dotenv import load_dotenv
import os
from telethon.events.common import EventCommon
from telethon.tl.custom import Button
import requests
import json

BOT_TOKEN = '5003522949:AAEkdzUD9RHnHOPKbTP_l_BhEvH0PlZ8dm0'
BOT_CHAT_ID = '1034689842'

load_dotenv()
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")

client = TelegramClient('session_name1', api_id, api_hash)

# @client.on(events.NewMessage(chats='test_global_avatar'))
# async def my_event_handler(event):
#     print(event.raw_text)
#     file_name = str(str(time.monotonic()))
#     # await client.send_message("test_global_chat", event.raw_text)
#     await client.send_message("Avatar.NewsMod", 'Welcome', buttons=[
#         Button.text('Thanks!', resize=True, single_use=True),
#         Button.request_phone('Send phone'),
#         Button.request_location('Send location')
#     ])

#     with open("test_global_avatar/test_global_avatar{}.txt".format(file_name), "w") as file:
#         file.write(event.raw_text)
    
#     # events.NewMessage()

# def start_bot(token : str):
#     updater = Updater(token, use_context=True)
#     dp = updater.dispatcher

#     # on different commands - answer in Telegram
#     dp.add_handler(CommandHandler("start", start))
#     dp.add_handler(CommandHandler("greet", greet_command))
#     dp.add_handler(CommandHandler("news", send_news))

#     # Start the Bot
#     updater.start_polling()
#     updater.idle()

def telegram_bot_send_msg(bot_token: str, bot_chatID: str, bot_message: str):
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message.replace("**","***")
    response = requests.get(send_text)
    return json.dumps(response.json(), ensure_ascii=False)


@client.on(events.NewMessage(chats='https://t.me/testglobalavatar'))
async def my_event_handler(event):
    chan_name = '**' + str(event.chat.title).upper() + '**' + '\n\n'
    print(telegram_bot_send_msg(BOT_TOKEN, BOT_CHAT_ID, chan_name + event.text))




if __name__ == "__main__":
    client.start()
    client.run_until_disconnected()
