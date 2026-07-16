import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import random
import asyncio
import unicodedata
from quotes import quotes, user_quotes
from datetime import timedelta
from Cogs.wordle_commands import WordleCommands

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

TRIGGERS = {
    "piss",
    "feet",
    "cuck",
    "6/7",
    "six seven",
    "pee",
    "urine",
    "6 7"
}
CONFUSABLES = str.maketrans({
    "а": "a",
    "е": "e",
    "і": "i",
    "о": "o",
    "р": "p",
    "с": "c",
    "х": "x",
    "у": "y",
})


TRIGGER_RESPONSE = "Right thats it im getting the hose out"

@bot.event
async def on_ready():
    print(f"I am here to spread evil, {bot.user.name}")
    if not hasattr(bot, "bg_task"):
        bot.bg_task = asyncio.create_task(random_messages())


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if bot.user in message.mentions:
        possible_quotes = quotes.copy()

        if message.author.id in user_quotes:
            possible_quotes.extend(user_quotes[message.author.id])

        await message.channel.send(random.choice(possible_quotes))

    content = (
    unicodedata.normalize("NFKC", message.content)
    .casefold()
    .translate(CONFUSABLES)
)

    if any(trigger in content for trigger in TRIGGERS):
        await message.channel.send(
            f"{message.author.mention} {TRIGGER_RESPONSE}"
        )

        try:
            await message.author.timeout(
                timedelta(minutes=2),
                reason="Triggered word filter"
            )
        except (discord.Forbidden, discord.HTTPException):
            await message.channel.send("Missing permissions to timeout users.")

    await bot.process_commands(message)

async def random_messages():
    await bot.wait_until_ready()

    channel = bot.get_channel(1523247225948606474)

    while not bot.is_closed():
        wait_time = random.randint(3600, 36000)
        await asyncio.sleep(wait_time)

        await channel.send("awa")

@bot.command()
async def deathroll(ctx, target: discord.Member = None, start: int = 1000):

    if isinstance(target, int):
        start = target
        target = None

    max_value = start

#fix issues where you cant play the bot with random values
    if target is None:
        player_turn = True 

        await ctx.send(f"💀 You vs Twoggeris deathroll starting at **{start}**")

        while True:
            roll = random.randint(1, max_value)

            if player_turn:
                await ctx.send(f"{ctx.author.mention} rolled **{roll}** (1-{max_value})")
            else:
                await ctx.send(f"🤖 Twoggeris rolled **{roll}** (1-{max_value})")

            if roll == 1:
                loser = ctx.author if player_turn else "🤖 Bot"
                await ctx.send(f"{loser} loses 💀")
                break

            max_value = roll
            player_turn = not player_turn

    else:
        players = [ctx.author, target]
        turn = 0

        await ctx.send(
            f"💀 Deathroll started: {ctx.author.mention} vs {target.mention} at **{start}**"
        )

        while True:
            current_player = players[turn]
            roll = random.randint(1, max_value)

            await ctx.send(f"{current_player.mention} rolled **{roll}** (1-{max_value})")

            if roll == 1:
                await ctx.send(f"{current_player.mention} loses 💀")
                break

            max_value = roll
            turn = 1 - turn


async def main():
    async with bot:
        await bot.add_cog(WordleCommands(bot))
        await bot.start(token)


asyncio.run(main())