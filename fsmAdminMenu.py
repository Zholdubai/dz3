from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from config import bot

class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()

async def fsm_start(message:types.Message):
    await FSMAdmin.photo.set()
    await bot.send_message(message.chat.id, f'Privet {message.from_user.full_name} skin fotku')
#foto

async def photo_bludo(message:types.Message,state:FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await FSMAdmin.next()
    await bot.send_message(message.chat.id, "Kak nazivaetsia bludo?")


#  name
async def bludo_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMAdmin.next()
    await bot.send_message(message.chat.id, "Opisanie kak?")


# description
async def description_bludo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['opisanie'] = message.text
    await FSMAdmin.next()
    await bot.send_message(message.chat.id, "skolko stoit (tolko so siframi?")

#price
async def bludo_price(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['price'] = int(message.text)
        await FSMAdmin.next()
        await bot.send_message(message.chat.id, "Spasibo za zakaz")
    except:
        await bot.send_message(message.chat.id, "Ja skazal tolko chislami!!!")


async def cancal_reg(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    else:
        await state.finish()
        await message.reply("ОК")


def register_hendler_fsmAdminGetUser(dp: Dispatcher):
    dp.register_message_handler(cancal_reg, state="*", commands="cancel")
    dp.register_message_handler(cancal_reg, Text(equals='cancel', ignore_case=True), state="*")

    dp.register_message_handler(fsm_start, commands=["register"])
    dp.register_message_handler(photo_bludo, state=FSMAdmin.photo, content_types=["photo"])
    dp.register_message_handler(bludo_name, state=FSMAdmin.name)
    dp.register_message_handler(description_bludo, state=FSMAdmin.description)
    dp.register_message_handler(bludo_price, state=FSMAdmin.price)




