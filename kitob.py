from bs4 import BeautifulSoup
import requests
from importlib.resources import path
from inspect import getfile
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

token = '5423620003:AAFpTH-Ruzs4JTk9sKWHiFwKWhANDYxZWg4'

def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_text(
        f'Xush kelibsiz, {user.first_name} \nKitob yoki muallif nomini kiriting.'
    )


def find(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Qidirilmoqda..')

    def find_books(url, page_number):
        next_page = url + str(page_number) + '&language=uz'
        response = requests.get(str(next_page)).text
        soup = BeautifulSoup(response, 'lxml')

        book_name = update.message.text

        ads = soup.find_all('div', class_='col-6 col-xl-3 col-md-4')
        for ad in ads:
            book_title = ad.h5.text.strip()
            book_photo = ad.find('div', class_='product__item-img').img['data-src'].replace('.webp', '')
            price = ad.find('span', class_='product__item-price').text.strip()
            link = 'https://asaxiy.uz/cart/checkout/'
            
            if book_name in book_title:
                #update.message.reply_photo(photo=book_photo, caption=f'{book_title} \nNarxi: {price} \nSotib olish: {link}')
                print(book_photo)
                update.message.reply_photo(book_photo, f'{book_title} \nNarxi: {price} \nSotib olish: {link}')
                #update.message.reply_photo(f'{book_photo}')

        if page_number < 50:
            page_number = page_number + 1
            find_books(url, page_number)

        if page_number == 49:
            update.message.reply_text('Search is finished')

    find_books('https://asaxiy.uz/product/knigi?page=', 1)



def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text, find))



    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
