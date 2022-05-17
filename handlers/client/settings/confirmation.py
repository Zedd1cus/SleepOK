from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from src.create_bot import bot
from keyboards.client_kb import kb_verify_client, confirmation_kb_scenario
from src.create_bot import dp

class NotificationFSM(StatesGroup):
	get_up = State()
	yes_no = State()
	sleep = State()
	notifications = State()

@dp.message_handler(commands=['start', 'help'], state=None)
async def send_welcome(message: types.Message):
	await NotificationFSM.get_up.set()
	await message.reply("Привет!  Я бот, который поможет тебе улучшить качество сна =)\n"\
	"Во сколько вы хотели бы просыпаться ? Какова ваша цель?")
	await message.reply('Пожалуйста, введите время в формате "часы:минуты", например "8:05"')

async def time_rule(message):
	await message.reply('Пожалуйста, введите время в формате "часы:минуты", например "8:05"')

hours_1 = None
minutes_1 = None

@dp.message_handler(state=NotificationFSM.get_up)
async def first_data(message: types.Message, state=FSMContext):
	global hours_1
	global minutes_1
	s_mes = message.text.split(':')
	if len(s_mes) == 2:
		try:
			hours_1 = int(s_mes[0])
			minutes_1 = int(s_mes[1])
			if (hours_1 <= 24 and hours_1 >= 0) and (minutes_1 < 60 and minutes_1 >= 0):
				await NotificationFSM.yes_no.set()
				await message.reply(f"вы хотите вставать в {hours_1} часов и {minutes_1} минут?", reply_markup=confirmation_kb_scenario)
				return
			else:
				raise ValueError
		except Exception:
			hours_1 = None
			minutes_1 = None
			await time_rule(message)
			return
	else:
		await time_rule(message)
		return

async def f_yes(message, state=FSMContext):
	async with state.proxy() as data:
		data['hours'] = hours_1
		data['minutes'] = minutes_1
	await NotificationFSM.next()
	await message.reply("А теперь, во сколько вы хотели бы ложиться спать?"\
			"Напишите лучшее для себя время")

#@dp.message_handler(state=NotificationFSM.yes_no)
async def f_yes_no(message: types.Message, state = FSMContext):
	if message.text == '/Yes':
		await NotificationFSM.get_up.set()
		f_yes(message)
	else:
		await NotificationFSM.get_up.set()
		await time_rule(message)

def functions_settings(dp: Dispatcher):
	dp.register_message_handler(send_welcome, commands=['start', 'help'], state=None)
	dp.register_message_handler(state=NotificationFSM.get_up)
	dp.register_message_handler(state=NotificationFSM.yes_no)
'''
keyboard = types.InlineKeyboardMarkup()
key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
keyboard.add(key_yes)
key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
keyboard.add(key_no)


@bot.message_handler(commands=['start', 'help']) # если пользователь ввёл команды /start или /help то выполняем функцию
def send_welcome(message): # выводим сообщение
	bot.reply_to(message, "Привет!  Я бот, который поможет тебе улучшить качество сна =)\n"\
	"Во сколько вы хотели бы просыпаться ? Какова ваша цель?")
	time_rule(message) # выполняем функцию снизу

def time_rule(message):
	bot.send_message(message.chat.id, 'Пожалуйста, введите время в формате "часы:минуты", например "8:05"')

@bot.message_handler(func=lambda message: True) # если пользователь ввёл что-то (в нашем случае время), то выполняем:
def first_message(message):
	global hours_1
	global minutes_1
	if hours_1 != None:  # если время подъема определено идём дальше
		second_answer(message)
		return
	s_mes = message.text.split(':') # проверка корректности данных, дальше не рассписываю, думаю понятно, как проверяется
	if len(s_mes) == 2:
		try:
			hours_1 = int(s_mes[0])
			minutes_1 = int(s_mes[1])
			if (hours_1 <= 24 and hours_1 >= 0) and (minutes_1 < 60 and minutes_1 >= 0):
				bot.send_message(message.chat.id, text=f"вы хотите вставать в {hours_1} часов и {minutes_1} минут?", reply_markup=keyboard)
			else:
				raise ValueError
		except Exception:
			hours_1 = None
			minutes_1 = None
			time_rule(message)
			return
	else:
		time_rule(message)
		return

@bot.callback_query_handler(func=lambda call: True)
def call_back_worker(call):
	if call.data == "yes":
		second_message(call.message)
	else:
		first_message(call.message)

def second_message(message):
	bot.send_message(message.chat.id, "А теперь, во сколько вы хотели бы ложиться спать?"\
			"Напишите лучшее для себя время")
	bot.register_next_step_handler(message, second_answer)

def second_answer(message): # то же самое, что и предыдущая функция, но для сна, а не для подъема
	global hours_2
	global minutes_2
	s_mes = message.text.split(':')
	if len(s_mes) == 2:
		try:
			hours_2 = int(s_mes[0])
			minutes_2 = int(s_mes[1])
			if (hours_2 <= 24 and hours_2 >= 0) and (minutes_2 < 60 and minutes_2 >= 0):
				bot.send_message(message.chat.id, text=f"вы хотите ложиться в {hours_2} часов и {minutes_2} минут?", reply_markup=keyboard)
			else:
				raise ValueError
		except Exception:
			hours_2 = 0
			minutes_2 = 0
			time_rule(message)
			return
	else:
		time_rule(message)
		return

bot.infinity_polling()
'''