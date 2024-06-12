import os 
from dotenv import load_dotenv
from telebot import TeleBot, types
import requests


load_dotenv()

bot = TeleBot(token=os.getenv("TOKEN"))

url = "https://v2.jokeapi.dev/joke/Dark"
params = {
    "format": "json",    
    "blacklistFlags": "religious,political,explicit" 
}


@bot.message_handler(commands=['start'])
def greeting(message):
    text = """
Hello! This bot is designed to send `bad` jokes.
Click the `Bad Joke` to get the joke, or `Exit` to leave...
"""
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Bad Joke", callback_data="btn1")
    btn2 = types.InlineKeyboardButton("Exit", callback_data="btn2")
    markup.add(btn1, btn2)
    
    bot.send_message(
        chat_id=message.chat.id, 
        text=text, 
        reply_markup=markup
        )


@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == "btn1":
        response = requests.get(url, params=params)
        if response.status_code == 200:
            joke_data = response.json()
            if joke_data['type'] == 'twopart':

                joke = joke_data['setup']
                answer = joke_data['delivery']
                bot.send_message(call.message.chat.id, f"{joke}\n\n`{answer}`")

            elif joke_data['type'] == 'single':
                joke = joke_data['joke']
                bot.send_message(call.message.chat.id, joke)
            else:
                bot.send_message(call.message.chat.id, "There are no bad jokes :(")
        else:
            bot.send_message(call.message.chat.id, "Something went wrong: ", response.status_code)

    elif call.data == "btn2":
        bot.send_message(call.message.chat.id, "Ok, goodbye...")
        bot.stop_polling()

