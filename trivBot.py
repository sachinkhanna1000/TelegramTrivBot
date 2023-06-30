import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import openai

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Telegram bot token
TOKEN = '6236204817:AAF0TKOdox9lzXUpmV_xhnPUAGvzlcZneQM'

# OpenAI API Key
openai.api_key = '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'

# Function to ask a question using OpenAI
def ask_question(question):
    chat_history = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": question}
        ]
    )
    return chat_history.choices[0].message.content

# Handler for /start command
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! I'm a trivia bot. Feel free to ask me any question!")

# Handler for regular messages
def handle_message(update, context):
    user_input = update.message.text
    try:
        response = ask_question(user_input)
        update.message.reply_text(response)
    except Exception as e:
        print("Error:", e)

def main():
    # Create the Updater and pass it your bot's token
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Register handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Start the bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()
