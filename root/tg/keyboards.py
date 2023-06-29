from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from . import callback_data_models


def get_ikb_to_vote_after_helping(likes_count):
    ikb_to_vote_after_helping = InlineKeyboardMarkup(row_width=1)
    b1 = InlineKeyboardButton(text=f'{likes_count} ❤️', callback_data='i_helped')
    ikb_to_vote_after_helping.add(b1)
    return ikb_to_vote_after_helping


def get_ikb_to_restore_message(message_id, username):
    ikb_to_restore_message = InlineKeyboardMarkup(row_width=1)
    b1 = InlineKeyboardButton(text='Восстановить сообщение',
                              callback_data=callback_data_models.restore_message_cb_data.new(message_id,
                                                                                             username))
    ikb_to_restore_message.add(b1)
    return ikb_to_restore_message
