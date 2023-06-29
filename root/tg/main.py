import asyncio
import datetime
import os
import re

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import CallbackQuery
from aiogram.utils.exceptions import ChatNotFound, RetryAfter
from dotenv import load_dotenv, find_dotenv
from sqlalchemy.exc import IntegrityError

from root.logger.config import logger
from root.db.setup import Session
from root.db import models
from . import keyboards, callback_data_models

logger = logger

load_dotenv(find_dotenv())

bot = Bot(os.getenv('TG_API'))
storage = MemoryStorage()

dp = Dispatcher(bot=bot, storage=storage)
chat_id = -936856228


class UserStates(StatesGroup):
    sending_ad = State()


@dp.message_handler(commands=['start'], state='*')
async def start(message: types.Message):
    user_is_member = await message.chat.get_member(message.from_user.id)
    if message.chat.id != -936856228:
        if user_is_member:
            await message.answer('Добро пожаловать в бот MEDIA PARTY!\n\nПока что здесь можно только создать '
                                 'объявление, которое попадет в наш общий чат. Чтобы это сделать, нажми '
                                 '\n-> /create_ad')
        else:
            await message.answer('Вы не состоите в нашей группе')


@dp.message_handler(commands=['create_ad'], state='*')
async def create_ad(message: types.Message):
    if message.chat.id != -936856228:
        await message.answer('Напишите свое объявление в одном следующем сообщении. Оно будет переслано в чат так, '
                             'как Вы его отправите сюда')
        await UserStates.sending_ad.set()


@dp.message_handler(state=UserStates.sending_ad)
async def forward_ad(message: types.Message, state: FSMContext):
    if message.chat.id != -936856228:
        await message.forward(chat_id)
        await bot.send_message(chat_id, f'👆Объявление от {message.from_user.full_name} (@{message.from_user.username})'
                                        f'\n\nЕсли Вы помогли с объявлением, то нажмите на сердечко ниже',
                               reply_markup=keyboards.get_ikb_to_vote_after_helping(0))
        await state.finish()
        await message.answer('Твое сообщение отправлено в группу! Чтобы создать еще одно объявление, '
                             'нажми\n-> /create_ad')


@dp.callback_query_handler(lambda c: c.data == 'i_helped')
async def i_helped(callback_query: types.CallbackQuery):
    session = Session()
    try:
        post_like_obj = session.query(models.UserPostLike).filter(
            models.UserPostLike.tg_id == str(callback_query.from_user.id),
            models.UserPostLike.post_message_id == str(callback_query.message.message_id)
        ).first()
        
        likes_count_query = session.query(models.UserPostLike).filter(
            models.UserPostLike.post_message_id == str(callback_query.message.message_id)
        )
        
        user_points_obj = session.query(models.Points).filter(
            models.Points.tg_id == str(callback_query.from_user.id)
        ).first()
        
        likes_count = likes_count_query.count()
        if post_like_obj:
            session.delete(post_like_obj)
            user_points_obj.score -= 1
            session.commit()
            likes_count -= 1
            await callback_query.answer('Вы отменили действие')
        else:
            new_post_like_obj = models.UserPostLike(tg_id=callback_query.from_user.id,
                                                    post_message_id=callback_query.message.message_id)
            session.add(new_post_like_obj)
            
            if user_points_obj:
                user_points_obj.score += 1
            else:
                new_user_points_obj = models.Points(tg_id=callback_query.from_user.id,
                                                    score=1)
                session.add(new_user_points_obj)
                
            session.commit()
            likes_count += 1
            await callback_query.answer('Еее, так держать!')
    except Exception as x:
        logger.exception(x)
        await callback_query.answer('У нас проблемы с базой данных')
        return
    finally:
        if session.is_active:
            session.close()
    
    await callback_query.message.edit_reply_markup(
        reply_markup=keyboards.get_ikb_to_vote_after_helping(likes_count)
    )


last_3_incoming_messages = []


@dp.message_handler(content_types=['any'])
async def delete_ad(message: types.Message):
    if message.chat.id == -936856228:
        global last_3_incoming_messages
        last_3_incoming_messages.append((message.from_user.id, message.message_id))
        if len(last_3_incoming_messages) > 3:
            last_3_incoming_messages.pop(0)
        
        if message.text == 'реклама':
            deleted_messages_ids = []
            for message_info_tuple in last_3_incoming_messages[::-1]:
                print(message_info_tuple, '111111')
                if message_info_tuple[0] == message.from_user.id:
                    print(message_info_tuple[1], 'удаляем')
                    last_3_incoming_messages.remove(message_info_tuple)
                    deleted_message_obj = await bot.copy_message(chat_id=459471362, from_chat_id=-936856228,
                                                                 message_id=message_info_tuple[1])
                    await bot.delete_message(chat_id=-936856228, message_id=message_info_tuple[1])
                    deleted_messages_ids.append(str(deleted_message_obj.message_id))

            print(deleted_messages_ids)
            deleted_messages_ids_str = '.'.join(deleted_messages_ids)
            await message.answer('Это сообщение похоже на рекламу. Если ты хочешь сделать какой-то анонс '
                                 'или о чем-то попросить, напиши в наш бот @MediaPartyBot. Это займет 10 секунд'
                                 'и пока бесплатно\n\n Если твое сообщение не рекламное, то прости меня и '
                                 'нажми на кнопку под этим сообщением. Но не злоупотребляй моим доверием, '
                                 'тебя могут за это выгнать...',
                                 reply_markup=keyboards.get_ikb_to_restore_message(
                                     deleted_messages_ids_str,
                                     message.from_user.username)
                                 )
        print(last_3_incoming_messages)


@dp.callback_query_handler(callback_data_models.restore_message_cb_data.filter())
async def restore_message(callback_query: types.CallbackQuery, callback_data: dict):
    username = callback_data.get('username')
    if callback_query.message.chat.id == -936856228 and username == callback_query.from_user.username:
        messages_ids = callback_data.get('message_id')
        print(messages_ids)
        
        await callback_query.message.answer(f'Восстановил сообщение от @{username}:')
        await callback_query.message.delete()
        messages_ids = [int(x) for x in messages_ids.split('.')[::-1]]
        for message_id in messages_ids:
            print(message_id)
            await bot.copy_message(chat_id=-936856228, from_chat_id=459471362, message_id=message_id)
        await callback_query.answer('Сообщение восстановлено, извини еще раз:)', show_alert=True)
    else:
        await callback_query.answer('Ты не писал это сообщение, не обманывай меня!', show_alert=True)


@dp.errors_handler(exception=RetryAfter)
async def exception_handler(update: types.Update, exception: RetryAfter):
    await update.callback_query.answer(f'Вы делаете слишком много запросов. Остановитель или будете забанены. '
                                       f'Следующее действие возможно только через {exception.timeout} секунд',
                                       show_alert=True)
    return True


async def send_and_copy_message(receiver_id, message, extra_message=None, reply_markup=None, divider=True):
    if extra_message:
        await bot.send_message(receiver_id, extra_message)
    copied_message = await bot.copy_message(chat_id=receiver_id, from_chat_id=message.chat.id,
                                            message_id=message.message_id,
                                            reply_markup=reply_markup)
    if divider:
        await bot.send_message(receiver_id, '------------------------------------')
    
    return copied_message


if __name__ == '__main__':
    with logger.catch():
        executor.start_polling(dispatcher=dp, skip_updates=True)
