from telethon import TelegramClient, events, sync
import time
from dotenv import load_dotenv
import os
from telethon.events.common import EventCommon
from telethon.tl.custom import Button

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


@client.on(events.NewMessage(chats='https://t.me/testglobalavatar'))
async def my_event_handler(event):
    print(event.text)
    file_name = str(str(time.monotonic()))
    with open("testglobalavatar/testglobalavatar_{}.txt".format(file_name), "w") as file:
        file.write(event.text)

@client.on(events.NewMessage(chats='https://t.me/lastcallhack'))
async def my_event_handler(event):
    print(event.raw_text)
    file_name = str(str(time.monotonic()))
    with open("lastcallhack/lastcallhack_{}.txt".format(file_name), "w") as file:
        file.write(event.raw_text)


@client.on(events.NewMessage(chats="https://t.me/gamedevjob"))
async def channel3(event):
    print(event.raw_text)
    file_name = str(str(time.monotonic()))
    with open("gamedevjob/gamedevjob_{}.txt".format(file_name), "w") as file:
        file.write(event.raw_text)


@client.on(events.NewMessage(chats="https://t.me/fintech_vacancy"))
async def channel4(event):
    print(event.raw_text)
    file_name = str(str(time.monotonic()))
    with open("fintech_vacancy/fintech_vacancy_{}.txt".format(file_name), "w") as file:
        file.write(event.raw_text)


@client.on(events.NewMessage(chats="https://t.me/habr_com"))
async def channel4(event):
    print(event.raw_text)
    file_name = str(str(time.monotonic()))
    with open("habr_com/habr_com_{}.txt".format(file_name), "w") as file:
        file.write(event.raw_text)



if __name__ == "__main__":
    client.start()
    client.run_until_disconnected()
