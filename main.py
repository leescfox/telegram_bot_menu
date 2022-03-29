from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Defaults, CallbackQueryHandler
from telegram import Update, ParseMode, MessageEntity, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup
from telegram.ext import CallbackContext
import logging
from typing import Union, List
from telegram import InlineKeyboardButton


def build_menu(
        buttons: List[InlineKeyboardButton],
        n_cols: int,
        header_buttons: Union[InlineKeyboardButton, List[InlineKeyboardButton]] = None,
        footer_buttons: Union[InlineKeyboardButton, List[InlineKeyboardButton]] = None
) -> List[List[InlineKeyboardButton]]:
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons if isinstance(header_buttons, list) else [header_buttons])
    if footer_buttons:
        menu.append(footer_buttons if isinstance(footer_buttons, list) else [footer_buttons])
    return menu


def main():
    TOKEN = "5206805580:AAG_9NXRkinVcLS0PyOnv3ksjvToRyAWIF0"

    logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

    defaults = Defaults(parse_mode=ParseMode.HTML)
    updater = Updater(token=TOKEN, defaults=defaults)
    dispatcher = updater.dispatcher

    def order(update, context):
        menu = [['Burger', 'Nuggets'], ['Coca Cola', 'Lipton']]
        callback = [['burg', 'chicken'], ['cola', 'tea']]
        page = 0
        keyboard = [
            InlineKeyboardButton(menu[0][0], callback_data=callback[0][0]),
            InlineKeyboardButton(menu[0][1], callback_data=callback[0][1])
        ]
        footer = [
            InlineKeyboardButton('<', callback_data=page - 1),
            InlineKeyboardButton('>', callback_data=page + 1)
        ]
        text = f"Страница {page + 1}\n{menu[0][0]}\n{menu[0][1]}"
        reply_markup = InlineKeyboardMarkup(build_menu(buttons=keyboard, n_cols=1, footer_buttons=footer))
        context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=reply_markup)

    def btn_handler(update, context):
        menu = [['Burger', 'Nuggets'], ['Coca Cola', 'Lipton']]
        callback = [['burg', 'chicken'], ['cola', 'tea']]
        query = update.callback_query
        page = int(query.data)
        if page < 0:
            page = 0
        elif page == len(menu):
            page = page - 1
        keyboard = [
            InlineKeyboardButton(menu[page][0], callback_data=callback[page][0]),
            InlineKeyboardButton(menu[page][1], callback_data=callback[page][1])
        ]
        footer = [
            InlineKeyboardButton('<', callback_data=page - 1),
            InlineKeyboardButton('>', callback_data=page + 1)
        ]
        text = f"Страница {page + 1}\n{menu[page][0]}\n{menu[page][1]}"
        reply_markup = InlineKeyboardMarkup(build_menu(buttons=keyboard, n_cols=1, footer_buttons=footer))
        query.edit_message_text(text=text, reply_markup=reply_markup)

    dispatcher.add_handler(CommandHandler('order', order))
    dispatcher.add_handler(CallbackQueryHandler(btn_handler))

    updater.start_polling()


if __name__ == "__main__":
    main()
