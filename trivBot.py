import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import countryinfo
import emoji

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Create a dictionary to map country names to emoji flags
COUNTRY_FLAGS = {
    "france": "🇫🇷",
    "germany": "🇩🇪",
    "afghanistan": "🇦🇫",
    "albania": "🇦🇱",
    "algeria": "🇩🇿",
    "andorra": "🇦🇩",
    "angola": "🇦🇴",
    "antigua and barbuda": "🇦🇬",
    "argentina": "🇦🇷",
    "armenia": "🇦🇲",
    "australia": "🇦🇺",
    "austria": "🇦🇹",
    "azerbaijan": "🇦🇿",
    "bahamas": "🇧🇸",
    "bahrain": "🇧🇭",
    "bangladesh": "🇧🇩",
    "barbados": "🇧🇧",
    "belarus": "🇧🇾",
    "belgium": "🇧🇪",
    "belize": "🇧🇿",
    "benin": "🇧🇯",
    "bhutan": "🇧🇹",
    "bolivia": "🇧🇴",
    "bosnia and herzegovina": "🇧🇦",
    "botswana": "🇧🇼",
    "brazil": "🇧🇷",
    "brunei": "🇧🇳",
    "bulgaria": "🇧🇬",
    "burkina faso": "🇧🇫",
    "burundi": "🇧🇮",
    "cabo verde": "🇨🇻",
    "cambodia": "🇰🇭",
    "cameroon": "🇨🇲",
    "canada": "🇨🇦",
    "central african republic": "🇨🇫",
    "chad": "🇹🇩",
    "chile": "🇨🇱",
    "china": "🇨🇳",
    "colombia": "🇨🇴",
    "comoros": "🇰🇲",
    "congo (brazzaville)": "🇨🇬",
    "congo (kinshasa)": "🇨🇩",
    "costa rica": "🇨🇷",
    "croatia": "🇭🇷",
    "cuba": "🇨🇺",
    "cyprus": "🇨🇾",
    "czech republic": "🇨🇿",
    "denmark": "🇩🇰",
    "djibouti": "🇩🇯",
    "dominica": "🇩🇲",
    "dominican republic": "🇩🇴",
    "ecuador": "🇪🇨",
    "egypt": "🇪🇬",
    "el salvador": "🇸🇻",
    "equatorial guinea": "🇬🇶",
    "eritrea": "🇪🇷",
    "estonia": "🇪🇪",
    "eswatini": "🇸🇿",
    "ethiopia": "🇪🇹",
    "fiji": "🇫🇯",
    "finland": "🇫🇮",
    "gabon": "🇬🇦",
    "gambia": "🇬🇲",
    "georgia": "🇬🇪",
    "ghana": "🇬🇭",
    "greece": "🇬🇷",
    "grenada": "🇬🇩",
    "guatemala": "🇬🇹",
    "guinea": "🇬🇳",
    "guinea-bissau": "🇬🇼",
    "guyana": "🇬🇾",
    "haiti": "🇭🇹",
    "honduras": "🇭🇳",
    "hungary": "🇭🇺",
    "iceland": "🇮🇸",
    "india": "🇮🇳",
    "indonesia": "🇮🇩",
    "iran": "🇮🇷",
    "iraq": "🇮🇶",
    "ireland": "🇮🇪",
    "israel": "🇮🇱",
    "italy": "🇮🇹",
    "jamaica": "🇯🇲",
    "japan": "🇯🇵",
    "jordan": "🇯🇴",
    "kazakhstan": "🇰🇿",
    "kenya": "🇰🇪",
    "kiribati": "🇰🇮",
    "north korea": "🇰🇵",
    "south korea": "🇰🇷",
    "kosovo": "🇽🇰",
    "kuwait": "🇰🇼",
    "kyrgyzstan": "🇰🇬",
    "laos": "🇱🇦",
    "latvia": "🇱🇻",
    "lebanon": "🇱🇧",
    "lesotho": "🇱🇸",
    "liberia": "🇱🇷",
    "libya": "🇱🇾",
    "liechtenstein": "🇱🇮",
    "lithuania": "🇱🇹",
    "luxembourg": "🇱🇺",
    "madagascar": "🇲🇬",
    "malawi": "🇲🇼",
    "malaysia": "🇲🇾",
    "maldives": "🇲🇻",
    "mali": "🇲🇱",
    "malta": "🇲🇹",
    "marshall islands": "🇲🇭",
    "mauritania": "🇲🇷",
    "mauritius": "🇲🇺",
    "mexico": "🇲🇽",
    "micronesia": "🇫🇲",
    "moldova": "🇲🇩",
    "monaco": "🇲🇨",
    "mongolia": "🇲🇳",
    "montenegro": "🇲🇪",
    "morocco": "🇲🇦",
    "mozambique": "🇲🇿",
    "myanmar": "🇲🇲",
    "namibia": "🇳🇦",
    "nauru": "🇳🇷",
    "nepal": "🇳🇵",
    "netherlands": "🇳🇱",
    "new zealand": "🇳🇿",
    "nicaragua": "🇳🇮",
    "niger": "🇳🇪",
    "nigeria": "🇳🇬",
    "north macedonia": "🇲🇰",
    "norway": "🇳🇴",
    "oman": "🇴🇲",
    "pakistan": "🇵🇰",
    "palau": "🇵🇼",
    "panama": "🇵🇦",
    "papua new guinea": "🇵🇬",
    "paraguay": "🇵🇾",
    "peru": "🇵🇪",
    "philippines": "🇵🇭",
    "poland": "🇵🇱",
    "portugal": "🇵🇹",
    "qatar": "🇶🇦",
    "romania": "🇷🇴",
    "russia": "🇷🇺",
    "rwanda": "🇷🇼",
    "saint kitts and nevis": "🇰🇳",
    "saint lucia": "🇱🇨",
    "saint vincent and the grenadines": "🇻🇨",
    "samoa": "🇼🇸",
    "san marino": "🇸🇲",
    "sao tome and principe": "🇸🇹",
    "saudi arabia": "🇸🇦",
    "senegal": "🇸🇳",
    "serbia": "🇷🇸",
    "seychelles": "🇸🇨",
    "sierra leone": "🇸🇱",
    "singapore": "🇸🇬",
    "slovakia": "🇸🇰",
    "slovenia": "🇸🇮",
    "solomon islands": "🇸🇧",
    "somalia": "🇸🇴",
    "south africa": "🇿🇦",
    "south sudan": "🇸🇸",
    "spain": "🇪🇸",
    "sri lanka": "🇱🇰",
    "sudan": "🇸🇩",
    "suriname": "🇸🇷",
    "sweden": "🇸🇪",
    "switzerland": "🇨🇭",
    "syria": "🇸🇾",
    "taiwan": "🇹🇼",
    "tajikistan": "🇹🇯",
    "tanzania": "🇹🇿",
    "thailand": "🇹🇭",
    "timor-leste": "🇹🇱",
    "togo": "🇹🇬",
    "tonga": "🇹🇴",
    "trinidad and tobago": "🇹🇹",
    "tunisia": "🇹🇳",
    "turkey": "🇹🇷",
    "turkmenistan": "🇹🇲",
    "tuvalu": "🇹🇻",
    "uganda": "🇺🇬",
    "ukraine": "🇺🇦",
    "united arab emirates": "🇦🇪",
    "united kingdom": "🇬🇧",
    "united states": "🇺🇸",
    "uruguay": "🇺🇾",
    "uzbekistan": "🇺🇿",
    "vanuatu": "🇻🇺",
    "vatican city": "🇻🇦",
    "venezuela": "🇻🇪",
    "vietnam": "🇻🇳",
    "yemen": "🇾🇪",
    "zambia": "🇿🇲",
    "zimbabwe": "🇿🇼",
    # Add more country names and their respective emoji flags here
}

# Define the capital command handler function
def capital_command(update: Update, context: CallbackContext):
    country_name = ' '.join(context.args)
    if country_name:
        try:
            country = countryinfo.CountryInfo(country_name)
            capital = country.capital()
            
            # Get the emoji flag based on the country name
            emoji_flag = COUNTRY_FLAGS.get(country_name.lower(), "")
            
            response = f"The capital of {country_name} is {capital} {emoji.emojize(emoji_flag, use_aliases=True)}"
        except countryinfo.CountryInfoException:
            response = f"Sorry, I couldn't find information for {country_name}"
    else:
        response = "Please provide a country name"
    
    # Send the response
    context.bot.send_message(chat_id=update.effective_chat.id, text=response)

def start_command(update: Update, context: CallbackContext):
    response = "Hello! I am a bot that can provide information about country capitals. Just type /capital followed by a country name."
    context.bot.send_message(chat_id=update.effective_chat.id, text=response)

def main():
    # Create the Updater and pass in your bot's token
    updater = Updater(token='6236204817:AAF0TKOdox9lzXUpmV_xhnPUAGvzlcZneQM', use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register the capital command handler
    capital_handler = CommandHandler('capital', capital_command)
    dispatcher.add_handler(capital_handler)

    # Register the start command handler
    start_handler = CommandHandler('start', start_command)
    dispatcher.add_handler(start_handler)

    # Start the bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()
