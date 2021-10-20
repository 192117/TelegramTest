import telebot, datetime
from telebot import types

class User:
    def __init__(self, id):
        self.id = id
        self.notes = dict()

def open_token(direction):
    with open(direction, "r") as file:
        return file.read()

data_user = []
send_notes = []

commands = {
    "start"    : "Start use this bot.",
    "help"     : "Show available commands.",
    "info"     : "This is a bot for reminders in telegram's messages at the right time.",
    'add'      : "Add notes in bot."
}

def get_notes_user(uid):
    for user in range(len(data_user)):
        if uid == data_user[user].id:
            return data_user[user].notes
    else:
        new_user = User(id=uid)
        data_user.append(new_user)
        print(f"New user - {uid} - use bot")
        return new_user.notes

def listen_messages(messages):
    for mes in messages:
        if mes.content_type == "text":
            print(str(mes.chat.first_name) + " [" + str(mes.chat.id) + "]: " + mes.text)


yesornoSelect = types.ReplyKeyboardMarkup(one_time_keyboard=True)
yesornoSelect.add('Yes', 'No')
hideBoard = types.ReplyKeyboardRemove()

bot = telebot.TeleBot(open_token("D:\\Users\\Kokoc\\PycharmProjects\\TelegramTest\\token_telegram.txt"))
bot.set_update_listener(listen_messages)

@bot.message_handler(commands=["start"])
def start(message):
    get_notes_user(message.from_user.id)
    print(f"New user - {message.from_user.id} - use bot -- function 'send_welcome'")
    bot.send_message(message.from_user.id, "Welcome!\nI'm RemainderBot. Let's go!")
    command_help(message)

@bot.message_handler(commands=["add"])
def send_welcome(message):
    if get_notes_user(message.from_user.id) == None:
        print(f"New user - {uid} - use bot -- function 'send_welcome'")
    else:
        bot.send_message(message.from_user.id, "I know you. Welcome!")
        print(f"User - {message.from_user.id} - use bot -- function 'send_welcome'")
    bot.send_message(message.from_user.id, "Do you need make a note?", reply_markup=yesornoSelect)
    bot.register_next_step_handler(message, get_answer)

@bot.message_handler(commands=["help"])
def command_help(message):
    help_text = "The following commands are available: \n"
    for key in commands:
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(message.from_user.id, help_text)

@bot.message_handler(commands=["info"])
def command_info(message):
    bot.send_message(message.from_user.id, commands["info"])

def get_answer(message):
    if message.text == "Yes":
        print(f"User {message.from_user.id} want to make a notes")
        bot.send_message(message.from_user.id,
                         f"When should I write to you?\nFormat {str(datetime.datetime.now())[:16]}")
        bot.register_next_step_handler(message, time_answer)
    elif message.text == "No":
        bot.send_message(message.from_user.id, "Bye!")
        print(f"User {message.from_user.id} doesn't make a note.")

def time_answer(message):
    if message.text == "No":
        print(f"User {message.from_user.id} wants to make a new note.")
        bot.send_message(message.from_user.id,
                         f"When should I write to you?\nFormat {str(datetime.datetime.now())[:16]}")
        bot.register_next_step_handler(message, time_answer)
    else:
        get_notes_user(message.from_user.id)[message.text] = None
        print(f"User {message.from_user.id} writes a time = {message.text}")
        bot.send_message(message.chat.id, "What should I remind you of?")
        bot.register_next_step_handler(message, get_note)

def get_note(message):
    for time in get_notes_user(message.from_user.id):
        if get_notes_user(message.from_user.id)[time] == None:
            get_notes_user(message.from_user.id)[time] = message.text
            print(f"User {message.from_user.id} asks to remind {message.text} on {time}")
            bot.send_message(message.from_user.id, "Ok!")
    bot.send_message(message.from_user.id, "Are you finish?", reply_markup=yesornoSelect)
    bot.register_next_step_handler(message, send_make)

def send_make(message):
    if message.text == "Yes":
        print(f"User {message.from_user.id} finish")
        bot.send_message(message.from_user.id,
                         "You can add note\nPlease send message 'Add note'/'Добавить заметку'")
        while True:
            now = str(datetime.datetime.now())[:16]
            for time in get_notes_user(message.from_user.id):
                if time == now:
                    if time not in send_notes:
                        send_notes.append(time)
                        bot.send_message(message.from_user.id, get_notes_user(message.from_user.id)[time])
                        print(f"I send {get_notes_user(message.from_user.id)[time]} to {message.from_user.id} on {time}")
            if len(send_notes) == len(get_notes_user(message.from_user.id).keys()):
                print(f"I finish with {message.from_user.id}")
                print(data_user)
                for user in range(len(data_user)):
                    print(data_user[user])
                    print(data_user[user].id)
                    print(data_user[user].notes)
                break
    elif message.text == "No":
        time_answer(message)
    else:
        bot.send_message(message.from_user.id,
                         "It's wrong!\nYou can send yes/no/да/нет\nThe type of letters isn't important")
        bot.register_next_step_handler(message, send_make)

@bot.message_handler(func=lambda message: True)
def check_note(message):
    if message.text.lower() == "add note" or message.text.lower() == "добавить заметку":
        bot.send_message(message.from_user.id,
                         f"When should I write to you?\nFormat {str(datetime.datetime.now())[:16]}")
        bot.register_next_step_handler(message, time_answer)


bot.polling()