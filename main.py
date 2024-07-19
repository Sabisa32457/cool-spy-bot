
import discord
import asyncio
import datetime
from plyer import notification
import random
from pystyle import *
from colorama import Fore, Style, init as colorama_init
import colorama
colorama.init()

# Initialize the bot client
intents = discord.Intents.default()
intents.typing = True
intents.message_content = True
client = discord.Client(intents=intents)
forward_server_id = 123456789012345678  # Replace with your server ID

# Function to get the user's role color
def get_user_role_color(user):
    # Find the highest role color that the user has
    if user.roles:
        for role in reversed(user.roles):
            if role.color != discord.Color.default():
                return role.color
    return discord.Color.default()  # Default color if no colored role


current_time = datetime.datetime.now().strftime('%H:%M:%S')

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.invisible, activity=discord.Activity(type=discord.ActivityType.playing, name="discord.py is cool"))
    print(f'We have logged in as {client.user}')
    print('Listening for messages...')

@client.event
async def on_message(message):
    if message.author == client.user:
            return
    await display_message_info(message)

async def display_message_info(message):
    try:
        server_name = message.guild.name
        channel_name = message.channel.name
        user_role_color = get_user_role_color(message.author)

        # Get the colorama color code for the role color
        role_color_code = get_colorama_color(user_role_color)
        a = f"[{current_time}] Server: {server_name} #{channel_name}"
        tiem = Colorate.Diagonal(Colors.rainbow, a)

        formatted_message = (
            f'{(tiem)} '
            f'{role_color_code}{message.author.name} '
            f'{Fore.RESET}sent a message: {message.content}'
        )
        
        # Print the formatted message to the terminal
        print(formatted_message)
    except Exception as e:
        print(f'Error displaying information: {e}')


def get_colorama_color(color): # chach gpt made som of dis cus i to lazy to type it out
    color_map = {
        discord.Color.default(): Fore.RESET,
        discord.Color.teal(): Fore.CYAN,
        discord.Color.dark_teal(): Fore.CYAN,
        discord.Color.green(): Fore.GREEN,
        discord.Color.dark_green(): Fore.GREEN,
        discord.Color.blue(): Fore.BLUE,
        discord.Color.dark_blue(): Fore.BLUE,
        discord.Color.purple(): Fore.MAGENTA,
        discord.Color.dark_purple(): Fore.MAGENTA,
        discord.Color.magenta(): Fore.MAGENTA,
        discord.Color.dark_magenta(): Fore.MAGENTA,
        discord.Color.gold(): Fore.YELLOW,
        discord.Color.dark_gold(): Fore.YELLOW,
        discord.Color.orange(): Fore.LIGHTRED_EX,
        discord.Color.dark_orange(): Fore.LIGHTRED_EX,
        discord.Color.red(): Fore.RED,
        discord.Color.dark_red(): Fore.RED,
        discord.Color.lighter_grey(): Fore.LIGHTBLACK_EX,
        discord.Color.dark_grey(): Fore.BLACK,
        discord.Color.light_grey(): Fore.LIGHTBLACK_EX,
    }
    return color_map.get(color, Fore.RESET)

# Event that occurs when someone starts typing
@client.event
async def on_typing(channel, user, when):
        user_role_color = get_user_role_color(user)

        role_color_code = get_colorama_color(user_role_color)
        a = f"{current_time} #{channel}"
        tiem = Colorate.Diagonal(Colors.rainbow, a)

        formatted_message = (
            f'{(tiem)} '
            f'{role_color_code}{user} '
            f'{Fore.RESET}is typing'
        )
        
        print(formatted_message)

@client.event
async def on_guild_join(guild):
    print(f'Joined new guild: {guild.name}')

    # Send toast notification
    notification_title = f"Joined new guild: {guild.name}"
    notification_text = f"New guild with {guild.member_count} members"
    notification.notify(
        title=notification_title,
        message=notification_text,
        app_name='Spy thing idk'
    )

def run_bot(token):
    client.run(token)

if __name__ == '__main__':
    TOKEN = input("Token ples: ")
    loop = asyncio.get_event_loop()

    bot_task = loop.create_task(run_bot(TOKEN))

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(client.logout())
        bot_task.cancel()
        loop.close()