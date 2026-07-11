from discord.ext import commands
from wordle.wordle import WordleGame

games = {}


class WordleCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def wordle(self, ctx):
        games[ctx.author.id] = WordleGame()
        await ctx.send("New Wordle game started! You have 6 guesses.")

    @commands.command()
    async def guess(self, ctx, word):
        if ctx.author.id not in games:
            await ctx.send("Start a game first with !wordle")
            return

        game = games[ctx.author.id]

        result = game.make_guess(word)

        if isinstance(result, str):
            await ctx.send(result)
            return

        await ctx.send(result)

        if game.game_won:
            await ctx.send("🎉 Congratulations! You won!")
            del games[ctx.author.id]

        elif game.guesses_remaining == 0:
            await ctx.send(f"You lose! The word was **{game.word}**")
            del games[ctx.author.id]