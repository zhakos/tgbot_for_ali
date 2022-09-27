import config as conf
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters.state import State, StatesGroup

config = conf.load_config("bot.ini")

# Объявление и инициализация объектов бота и диспетчера
bot = Bot(token=config.tg_bot.token)


class printRasp(StatesGroup):
    waiting_for_group = State()


async def start(message: types.message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    buttons = ['Вывести расписание по группе', ]
    keyboard.add(*buttons)
    await message.answer("Выберите кнопку", reply_markup=keyboard)


async def input_group(message: types.message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    keyboard.add('Назад')
    await message.answer("Напишите вашу группу", reply_markup=keyboard)
    await printRasp.waiting_for_group.set()


async def print_raspisanie(message: types.message):
    try:
        await bot.send_document(message.chat.id,
                                open(f'raspisanie/{message.text.lower()}.doc', 'rb'))  # Тип файла укажи

    except:
        await message.answer("Неверно указана группа")


def register_navigate(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start', 'menu'], state="*")
    dp.register_message_handler(start, text='Назад', state="*")
    dp.register_message_handler(input_group, text='Вывести расписание по группе', state="*")
    dp.register_message_handler(print_raspisanie, state=printRasp.waiting_for_group)
