# Importing modules
from telebot import TeleBot, types
from config import *
from time import sleep

bot = TeleBot(api_token)


# Function for sending chat action
def send_chat_action(message, action: str, time: int = 3) -> None:
    bot.send_chat_action(message.chat.id, action)
    sleep(time)


# Function for getting reply keyboard
def get_reply_keyboard(keyboard_buttons: list,
                       one_time: bool = False,
                       menu_keyboard: bool = False) -> types.ReplyKeyboardMarkup:
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=one_time)

    # Internal function. If keyboard needs for menu
    def get_menu_keyboard() -> None:
        for i in range(len(keyboard_buttons)):
            if i == 1:
                keyboard.add(types.KeyboardButton(text=keyboard_buttons[i]),
                             types.KeyboardButton(text=keyboard_buttons[i + 1]))
            elif i == 2:
                continue
            else:
                keyboard.add(types.KeyboardButton(text=keyboard_buttons[i]))

    if not menu_keyboard:
        for button in keyboard_buttons:
            keyboard.add(types.KeyboardButton(button))
    else:
        get_menu_keyboard()

    return keyboard


# Function for getting primary inline keyboard
def get_primary_inline_keyboard() -> types.InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Романы о семье Алехиных', callback_data='Семья Алехиных'))
    keyboard.add(types.InlineKeyboardButton(text='Трилогия романов о демонах', callback_data='История темного мастера'))
    keyboard.add(types.InlineKeyboardButton(text='Наше счастливое вчера', callback_data='Наше счастливое вчера'))
    keyboard.add(types.InlineKeyboardButton(text='Фантастика', callback_data='Фантастика'))

    return keyboard


# Function for getting secondary inline keyboard
def get_secondary_inline_keyboard(buttons: list, callbacks: list) -> types.InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup()
    for button, callback in zip(buttons, callbacks):
        keyboard.add(types.InlineKeyboardButton(text=button, callback_data=callback))

    return keyboard


# Function for getting inline keyboard to every novel
def get_inline_keyboard_for_novel(novel: str) -> types.InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(types.InlineKeyboardButton(text='Дополнительно', callback_data=f'more {novels.index(novel)}'))
    keyboard.add(types.InlineKeyboardButton(text='О книге', callback_data=f'about {novels.index(novel)}'),
                 types.InlineKeyboardButton(text='Персонажи', callback_data=f'characters {novels.index(novel)}'))
    keyboard.add(types.InlineKeyboardButton(text='Меню', callback_data='menu'))
    return keyboard


# Function for getting username
def get_user(message) -> str:
    user = message.from_user.first_name
    if message.from_user.last_name is not None:
        user += f' {message.from_user.last_name}'
    return user


# Bot commands
@bot.message_handler(commands=['start'])
def start(message):
    user = get_user(message)
    keyboard = get_reply_keyboard(keyboard_buttons=['Меню'], one_time=True)
    send_chat_action(message, 'typing', 2)
    bot.send_message(message.chat.id, f'Рад приветствовать, {user}!\n'
                                      'Для отображения списка команд используй /help'
                                      '\nДля получения информации используй /info\n'
                                      'Чтобы открыть список контактов используй /contacts', reply_markup=keyboard)


@bot.message_handler(commands=['menu'])
def menu(message):
    menu_keyboard = get_reply_keyboard(keyboard_buttons=main_menu_buttons, menu_keyboard=True, one_time=True)
    send_chat_action(message, 'typing', 2)
    bot.send_message(message.chat.id, 'Меню открыто \U00002705', reply_markup=menu_keyboard)


@bot.message_handler(commands=['help'])
def help_list(message):
    keyboard = get_reply_keyboard(keyboard_buttons=['Меню'], one_time=True)
    send_chat_action(message, 'typing', 2)
    bot.send_message(message.chat.id, text=helpList, reply_markup=keyboard)


@bot.message_handler(commands=['contacts'])
def contacts_list(message):
    keyboard = get_reply_keyboard(keyboard_buttons=['Меню'], one_time=True)
    send_chat_action(message, 'typing', 2)
    bot.send_message(message.chat.id, text=contacts, reply_markup=keyboard)


@bot.message_handler(commands=['info'])
def information(message):
    keyboard = get_reply_keyboard(keyboard_buttons=['Меню'], one_time=True)
    send_chat_action(message, 'typing', 2)
    bot.send_message(message.chat.id, text=info, reply_markup=keyboard)


# Processing messages in chat
@bot.message_handler(content_types=['text'])
def check_message(message):
    if message.text == 'Завершить работу \U0001F4A4':
        keyboard = get_reply_keyboard(keyboard_buttons=['СТАРТ'], one_time=True)
        send_chat_action(message, 'typing', 2)
        bot.send_message(message.chat.id,
                         'Было приятно с вами работать!\nВсего доброго\U0001FAE1',
                         reply_markup=keyboard)
    elif message.text == 'Меню':
        keyboard = get_reply_keyboard(keyboard_buttons=main_menu_buttons, menu_keyboard=True, one_time=True)
        send_chat_action(message, 'typing', 2)
        bot.send_message(message.chat.id, 'Выберите, что вы хотите сделать\U0001F607', reply_markup=keyboard)

    elif message.text == 'Выбрать произведение \U0001F4DA':
        keyboard = get_primary_inline_keyboard()
        send_chat_action(message, 'typing', 2)
        bot.send_message(message.chat.id, 'Какое произведение вас интересует?', reply_markup=keyboard)

    elif message.text.lower() == 'старт':
        user = get_user(message)
        keyboard = get_reply_keyboard(keyboard_buttons=['Меню'], one_time=True)
        send_chat_action(message, 'typing', 2)
        bot.send_message(message.chat.id, f'Приветствую, {user}!\nДля открытия меню жми кнопку',
                         reply_markup=keyboard)
    elif message.text == 'Контакты \U0001F4D3':
        keyboard = get_reply_keyboard(keyboard_buttons=['Меню'], one_time=True)
        send_chat_action(message, 'typing', 2)
        bot.send_message(message.chat.id, text=contacts, reply_markup=keyboard)
    elif message.text == 'Информация \U00002139':
        keyboard = get_reply_keyboard(keyboard_buttons=['Меню'], one_time=True)
        send_chat_action(message, 'typing', 2)
        bot.send_message(message.chat.id, text=info, reply_markup=keyboard)
    else:
        keyboard = get_reply_keyboard(keyboard_buttons=['Меню'], one_time=True)
        send_chat_action(message, 'typing', 2)
        bot.send_message(message.chat.id, 'Прости, я не понимаю \U0001F97A\n'
                                          'Используй /help для просмотра списка команд \U0001F9D0\n'
                                          'Или жми на кнопку Меню \U0001F92F', reply_markup=keyboard)


# Processing events in group chat
@bot.message_handler(content_types=['new_chat_members'])
def hello_member(message):
    user = get_user(message)
    send_chat_action(message, 'typing', 2)
    bot.send_message(message.chat.id, text=f'Приветствую, {user}!{hello}')


# Processing callbacks by inline keyboard buttons
@bot.callback_query_handler(func=lambda call: True)
def process_callback(call):
    # Internal function for processing callbacks
    def check_callback() -> None:
        for i, element in enumerate(novels_callback_id):
            if call.data == element:
                file = open(f'data/novels/{novels[i]}.pdf', 'rb')
                keyboard = get_inline_keyboard_for_novel(novels[i])
                send_chat_action(call.message, 'typing', 2)
                bot.edit_message_text('Уже отправляю \U0001F60C', call.message.chat.id, call.message.id)
                send_chat_action(call.message, 'typing', 2)
                bot.send_message(call.message.chat.id, 'Приятного прочтения\U0001F60A')
                send_chat_action(call.message, 'upload_document', 3)
                bot.send_document(call.message.chat.id, document=file, reply_markup=keyboard)

        for i, element in enumerate(characters_callback_id):
            if call.data == element:
                if 'characters' in element:
                    # Delete "if" when all files with characters be in folder
                    if i > 0:
                        bot.delete_message(call.message.chat.id, call.message.id)
                        keyboard = get_reply_keyboard(keyboard_buttons=['Меню'], one_time=True, menu_keyboard=True)
                        send_chat_action(call.message, 'typing', 2)
                        bot.send_message(call.message.chat.id, 'В разработке... \U0001F616',
                                         reply_markup=keyboard)
                    else:
                        file = open(f'data/characters/{novels[i]} персонажи.docx', 'rb')
                        send_chat_action(call.message, 'typing', 2)
                        bot.send_message(call.message.chat.id, 'Все персонажи в файле\U0001F60F')
                        send_chat_action(call.message, 'upload_document', 3)
                        bot.send_document(call.message.chat.id, document=file)

        for i, element in enumerate(about_callback_id):
            # Delete "if" when description will be in folder about
            if call.data == element:
                if not (i >= 0):
                    file = open(f'data/about/{novels[i]} о книге.pdf', 'rb')
                    send_chat_action(call.message, 'typing', 2)
                    bot.send_message(call.message.chat.id, 'Информация о книге в файле\U0001F60C')
                    send_chat_action(call.message, 'upload_document', 3)
                    bot.send_document(call.message.chat.id, document=file)
                else:
                    bot.delete_message(call.message.chat.id, call.message.id)
                    keyboard = get_reply_keyboard(keyboard_buttons=['Меню'], one_time=True, menu_keyboard=True)
                    send_chat_action(call.message, 'typing', 2)
                    bot.send_message(call.message.chat.id, 'В разработке... \U0001F616',
                                     reply_markup=keyboard)

        for i, element in enumerate(more_callback_id):
            if call.data == element:
                if not (i >= 0):
                    file = open(f'data/more/{novels[i]} дополнительно.docx', 'rb')
                    send_chat_action(call.message, 'typing', 2)
                    bot.send_message(call.message.chat.id,
                                     'В файле ниже вы можете ознакомиться '
                                     'с дополнительным контентом по произведению! \U0001F60C')
                    send_chat_action(call.message, 'upload_document', 3)
                    bot.send_document(call.message.chat.id, document=file)
                else:
                    bot.delete_message(call.message.chat.id, call.message.id)
                    keyboard = get_reply_keyboard(keyboard_buttons=['Меню'], one_time=True, menu_keyboard=True)
                    send_chat_action(call.message, 'typing', 2)
                    bot.send_message(call.message.chat.id, 'Мне очень жаль, но данный '
                                                           'раздел пока недоступен \U0001F616',
                                     reply_markup=keyboard)

        if call.data == 'menu':
            keyboard = get_reply_keyboard(keyboard_buttons=main_menu_buttons, menu_keyboard=True, one_time=True)
            send_chat_action(call.message, 'typing', 2)
            bot.send_message(call.message.chat.id, 'Выберите, что вы хотите сделать\U0001F607',
                             reply_markup=keyboard)

        # Processing callbacks from primary keyboard
        if call.data.lower() == 'семья алехиных':
            bot.delete_message(call.message.chat.id, call.message.id)
            send_chat_action(call.message, 'typing')
            bot.send_message(call.message.chat.id, 'Представляю вашему вниманию романы о семье Алехиных\U0001F525',
                             reply_markup=get_secondary_inline_keyboard(novels[1:3], novels_callback_id[1:3]))
        elif call.data.lower() == 'история темного мастера':
            bot.delete_message(call.message.chat.id, call.message.id)
            send_chat_action(call.message, 'typing')
            bot.send_message(call.message.chat.id, 'Представляю вашему вниманию трилогию романов об истории темного '
                                                   'матера\U0001F929 \n\n',
                             reply_markup=get_secondary_inline_keyboard(novels[3:6], novels_callback_id[3:6]))
        elif call.data.lower() == 'наше счастливое вчера':
            bot.delete_message(call.message.chat.id, call.message.id)
            send_chat_action(call.message, 'typing')
            bot.send_message(call.message.chat.id, 'Представляю вашему вниманию увлекательные детективные '
                                                   'романы с завораживающим сюжетом\U0001F631'
                                                   ' \n\nК сожалению, в данный момент вторая часть романа'
                                                   ' находится в стадии написания, но могу уверить '
                                                   'вас, дорогой читатель, что автор вскоре опубликует его\U0001F60A',
                             reply_markup=get_secondary_inline_keyboard([novels[0]], [novels_callback_id[0]]))
        elif call.data.lower() == 'фантастика':
            bot.delete_message(call.message.chat.id, call.message.id)
            send_chat_action(call.message, 'typing')
            bot.send_message(call.message.chat.id,
                             'Представляю вашему вниманию произведения жанра фантастика\U0001F9D0',
                             reply_markup=get_secondary_inline_keyboard([novels[5]], [novels_callback_id[5]]))

    check_callback()
