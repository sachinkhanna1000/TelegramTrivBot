import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import openai

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = ''

openai.api_key = ''

def ask_question(question):
    chat_history = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": question}
        ]
    )
    return chat_history.choices[0].message.content

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! I'm a trivia bot. Feel free to ask me any question!")

def handle_message(update, context):
    user_input = update.message.text
    try:
        response = ask_question(user_input)
        update.message.reply_text(response)
    except Exception as e:
        print("Error:", e)

def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
