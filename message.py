import requests
import telegram


def telegram_bot_send_text(bot_message, token, chat_id):
    me = ""

    print("SENDING MESSAGE")

    part1 = 'https://api.telegram.org/bot'
    part2 = '/sendMessage?chat_id='
    part3 = '&parse_mode=Markdown&text='

    send_text = part1 + token + part2 + chat_id + part3 + me + bot_message

    response = requests.get(send_text)

    return response.json()


async def send_photo(photo, token, chat_id):
    bot = telegram.Bot(token=token)
    await bot.send_photo(chat_id=chat_id, photo=photo)


def send_document(file_name, token, chat_id):
    bot = telegram.Bot(token=token)
    with open(file_name, "rb") as file:
        bot.send_document(chat_id=chat_id, document=file, filename=file_name)
