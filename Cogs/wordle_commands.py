from discord.ext import commands
from wordle.wordle import WordleGame
from wordle.wordle import QuordleGame

games = {}


def format_game_state(result):
    symbols = {
        "grey": "⬛ ",
        "yellow": "🟨 ",
        "green": "🟩 "
    }

    message = "Score:\n"
    message += "".join(symbols[x] for x in result["score"])

    message += "\n\nLetters used:\n"

    for letter, state in result["letters"].items():
        if state != "unknown":
            message += f"{letter.upper()}: {state}\n"

    message += f"\nGuesses remaining: {result['guesses_remaining']}"

    return message

def format_quordle_state(results):
    symbols = {
        "grey": "⬛",
        "yellow": "🟨",
        "green": "🟩"
    }

    message = ""

    for i, result in enumerate(results):
        message += f"Word {i + 1}\n"
        message += "".join(symbols[x] for x in result["score"])
        message += "\n\n"

    message += f"Guesses remaining: {results[0]['guesses_remaining']}"

    return message


class WordleCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def wordle(self, ctx):
        games[ctx.author.id] = WordleGame(word_length=5)
        await ctx.send("New 5-letter Wordle game started! You have 6 guesses.")


    @commands.command()
    async def wordle6(self, ctx):
        games[ctx.author.id] = WordleGame(word_length=6)
        await ctx.send("New 6-letter Wordle game started! You have 6 guesses.")


    @commands.command()
    async def guess(self, ctx, word):
        if ctx.author.id not in games:
            await ctx.send("Start a game first with !wordle, !wordle6 or !quordle")
            return

        game = games[ctx.author.id]

        result = game.make_guess(word)

        if isinstance(result, str):
            await ctx.send(result)
            return

        if isinstance(game, QuordleGame):
            await ctx.send(format_quordle_state(result))
        else:
            await ctx.send(format_game_state(result))

        if game.game_won:
            await ctx.send("🎉 Congratulations! You won!")
            del games[ctx.author.id]

        elif game.guesses_remaining == 0:
            if isinstance(game, QuordleGame):
                words = ", ".join(game.words)
                await ctx.send(f"You lose! The words were **{words}**")
            else:
                await ctx.send(f"You lose! The word was **{game.word}**")

            del games[ctx.author.id] 

    @commands.command()
    async def quordle(self, ctx):
        games[ctx.author.id] = QuordleGame()
        await ctx.send("New Quordle game started! Solve all 4 words in 9 guesses.")

