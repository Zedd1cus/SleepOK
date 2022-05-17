from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from src.create_bot import bot
from keyboards.client_kb import kb_verify_client, confirmation_kb_scenario
from src.create_bot import dp


class NotificationFSM(StatesGroup):
	get_up = State() # состояние ввода времени подъёма
	yes_no_1 = State() # кнопки да/нет для подтверждения предыдущего состояния
	sleep = State() # состояние ввода времени сна
	yes_no_2 = State() # кнопки да/нет для подтверждения предыдущего состояния
	notifications = State() # состояние ввода времени уведомления
	yes_no_3 = State() # кнопки да/нет для подтверждения предыдущего состояния
	end = State() # конец


#@dp.message_handler(commands=['start', 'help'], state=None)
async def send_welcome(message: types.Message):
	await NotificationFSM.get_up.set()
	await bot.send_message(message.from_user.id, "Привет!  Я бот, который поможет тебе улучшить качество сна =)\n"\
	"Во сколько вы хотели бы просыпаться ? Какова ваша цель?")
	await bot.send_message(message.from_user.id, 'Пожалуйста, введите время в формате "часы:минуты", например "8:05"')


async def time_rule(message):
	await bot.send_message(message.from_user.id, 'Пожалуйста, введите время в формате "часы:минуты", например "8:05"')

hours_1 = None # переменная, в которую записываются часы пробуждения
minutes_1 = None # переменная, в которую записываются минуты пробуждения
hours_2 = None # переменная, в которую записываются часы сна
minutes_2 = None # переменная, в которую записываются минуты сна
hours_3 = None # переменная, в которую записываются часы уведомления
minutes_3 = None # переменная, в которую записываются минуты уведомления
notif = [] # список, в который добавляем времена уведомлений
time = None
flag = False


#@dp.message_handler(state=NotificationFSM.get_up)
async def first_data(message: types.Message, state=FSMContext):
	global hours_1
	global minutes_1
	s_mes = message.text.split(':')
	if len(s_mes) == 2:
		try:
			hours_1 = int(s_mes[0])
			minutes_1 = int(s_mes[1])
			if (hours_1 <= 24 and hours_1 >= 0) and (minutes_1 < 60 and minutes_1 >= 0):
				await NotificationFSM.yes_no_1.set()
				await bot.send_message(message.from_user.id, f"вы хотите вставать в {hours_1} часов и {minutes_1} минут?", reply_markup=confirmation_kb_scenario)
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


async def f_yes_1(message, state=FSMContext):
	#async with state.proxy() as data:
		#data['hours'] = hours_1 # вот тут изначально планировалось записать данные в само состояние, но возникает какая-то ошибка
		#data['minutes'] = minutes_1
	await NotificationFSM.sleep.set()
	await bot.send_message(message.from_user.id, "А теперь, во сколько вы хотели бы ложиться спать?"\
			"Напишите лучшее для себя время")


#@dp.message_handler(state=NotificationFSM.yes_no_1)
async def f_yes_no_1(message: types.Message, state = FSMContext):
	if message.text == '/Yes':
		await NotificationFSM.get_up.set()
		await f_yes_1(message)
	else:
		await NotificationFSM.get_up.set()
		await time_rule(message)


#@dp.register_message_handler(state=NotificationFSM.sleep)
async def second_data(message):
	global hours_2
	global minutes_2
	s_mes = message.text.split(':')
	if len(s_mes) == 2:
		try:
			hours_2 = int(s_mes[0])
			minutes_2 = int(s_mes[1])
			if (hours_2 <= 24 and hours_2 >= 0) and (minutes_2 < 60 and minutes_2 >= 0):
				await NotificationFSM.yes_no_2.set()
				await bot.send_message(message.chat.id, f"вы хотите ложиться в {hours_2} часов и {minutes_2} минут?", reply_markup=confirmation_kb_scenario)
				return
			else:
				raise ValueError
		except Exception:
			hours_2 = None
			minutes_2 = None
			await time_rule(message)
			return
	else:
		await time_rule(message)
		return


#@dp.message_handler(state=NotificationFSM.yes_no_2)
async def f_yes_no_2(message: types.Message, state = FSMContext):
	if message.text == '/Yes':
		await NotificationFSM.sleep.set()
		await f_yes_2(message)
	else:
		await NotificationFSM.sleep.set()
		await time_rule(message)


async def f_yes_2(message, state=FSMContext):
	#async with state.proxy() as data:
		#data['hours'] = hours_2
		#data['minutes'] = minutes_2
	await NotificationFSM.notifications.set()
	await notif_rule(message)


async def notif_rule(message):
	await bot.send_message(message.from_user.id, "Пожалуйста, введите время уведомления, в которое будет оцениваться ваше состояние. "\
			"Вводите в том же формате: 'часы:минуты', например '8:05'")


#@dp.register_message_handler(state=NotificationFSM.notifications)
async def notifications_data(message):
	global hours_3
	global minutes_3
	s_mes = message.text.split(':')
	if len(s_mes) == 2:
		try:
			hours_3 = int(s_mes[0])
			minutes_3 = int(s_mes[1])
			if (hours_3 <= 24 and hours_3 >= 0) and (minutes_3 < 60 and minutes_3 >= 0):
				await NotificationFSM.yes_no_3.set()
				await bot.send_message(message.from_user.id, f"вы хотите получать уведомление в {hours_3} часов и {minutes_3} минут?", reply_markup=confirmation_kb_scenario)
				return
			else:
				raise ValueError
		except Exception:
			hours_3 = None
			minutes_3 = None
			await time_rule(message)
			return
	else:
		await time_rule(message)
		return


async def f_yes_3(message, state=FSMContext):
	#async with state.proxy() as data:
		#data['hours'] = hours_1
		#data['minutes'] = minutes_1
	notif.append((hours_3, minutes_3))
	await NotificationFSM.yes_no_3.set()
	global flag
	flag = True
	await bot.send_message(message.from_user.id, "Хотите ли вы добавить ещё одно время уведомления?", reply_markup=confirmation_kb_scenario)


#@dp.message_handler(state=NotificationFSM.yes_no_3)
async def f_yes_no_3(message: types.Message, state = FSMContext):
	global flag
	if message.text == '/Yes':
		if flag:
			flag = False
			await NotificationFSM.notifications.set()
			await notif_rule(message)
		else:
			await NotificationFSM.notifications.set()
			await f_yes_3(message)
	else:
		if flag:
			flag = False
			await NotificationFSM.end.set()
			await bot.send_message(message.from_user.id, "Спасибо за введённые данные!")
		else:
			await NotificationFSM.notifications.set()
			await time_rule(message)


def functions_settings(dp: Dispatcher):
	dp.register_message_handler(send_welcome, commands=['hello', 'help'], state=None)
	dp.register_message_handler(first_data, state=NotificationFSM.get_up)
	dp.register_message_handler(f_yes_no_1, state=NotificationFSM.yes_no_1)
	dp.register_message_handler(f_yes_no_2, state=NotificationFSM.yes_no_2)
	dp.register_message_handler(f_yes_no_3, state=NotificationFSM.yes_no_3)
	dp.register_message_handler(second_data, state=NotificationFSM.sleep)
	dp.register_message_handler(notifications_data, state=NotificationFSM.notifications)
