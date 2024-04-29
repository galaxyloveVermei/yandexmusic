import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import markdown as md
from yandex_music import Client

API_TOKEN = '6864516273:AAERcEXvkjNAltUUYc9fADy5cUTcw3B7m34'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


class Form(StatesGroup):
    track = State() 


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await Form.track.set()
    await message.reply("Напиши команду /track чтобы узнать что сейчас играет")


@dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await message.reply('OK')
    

@dp.message_handler(commands=['mytrack'])
async def cmd_mytrack(message: types.Message):
    await get_user_current_track(message)
async def get_user_current_track(message: types.Message):
    await bot.send_chat_action(message.from_user.id, 'typing')
    
    client = Client.from_token('y0_AgAAAABy7nEtAAG8XgAAAAD1YduqGJAgnC3TQzqCi0B1ZkfsSPw9v3c')
    current_track = client.tracks([(client.current_track()['id'])])[0]
    
    md_text = md.text(
        md.text('Сейчас у вас играет:'),
        md.hbold(current_track.title),
        md.text('исполнитель:'),
        md.hbold(current_track.artists[0].name),
        sep='\n'
    )
    
    await message.reply(md_text, parse_mode=ParseMode.MARKDOWN)

    
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
