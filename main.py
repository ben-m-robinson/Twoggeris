import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import random
from quotes import quotes, user_quotes

load_dotenv()
token = os.getenv("DISCORD_TOKEN")

handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

user_IDs = {
    "Moo":132973467212578816,
    "Nev":400291092270022666,
    "Auggeris":117765165138575365,
    "Baqu": 221997493104279552,
    "Sira": 423948915373768734,
    "Holo": 246522885286526986,
    "Kumi": 364496506054508544
}

@bot.event
async def on_ready():
    print(f"I am here to spread evil, {bot.user.name}")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if bot.user in message.mentions:
        possible_quotes = quotes.copy()

        # Add user-specific quotes if they exist
        if message.author.id in user_quotes:
            possible_quotes.extend(user_quotes[message.author.id])

        await message.channel.send(random.choice(possible_quotes))

    await bot.process_commands(message)

bot.run(token, log_handler=handler, log_level=logging.DEBUG)