import telegram
from telegram.ext import CommandHandler
from countryinfo import CountryInfo
import emoji

def start_command(update, context):
    message = "Welcome! Please type '/capital [country]' to get the capital information of a country."
    update.message.reply_text(message)

def capital_command(update, context):
    country_name = ' '.join(context.args)
    try:
        country = CountryInfo(country_name)
        capital = country.capital()
        emoji_flag = emoji.emojize(country.emoji(), use_aliases=True)
        response = f"The capital of {country_name} {emoji_flag} is {capital}."
    except KeyError:
        response = "Sorry, I couldn't find information about that country."

    update.message.reply_text(response)

# Replace 'YOUR_API_TOKEN' with your Telegram bot API token
bot = telegram.Bot(token='6236204817:AAF0TKOdox9lzXUpmV_xhnPUAGvzlcZneQM')
updater = telegram.ext.Updater(bot=bot, use_context=True)

# Add the command handlers
updater.dispatcher.add_handler(CommandHandler('start', start_command))
updater.dispatcher.add_handler(CommandHandler('capital', capital_command))

updater.start_polling()
