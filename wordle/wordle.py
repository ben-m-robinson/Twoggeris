from .words import WORDS
from .six_letter_words import SIX_LETTER_WORDS
import random
from enum import Enum, IntEnum
from collections import Counter


class LetterState(IntEnum):
    UNKNOWN = 0
    GREY = 1
    YELLOW = 2
    GREEN = 3

class GameMode(Enum):
    NORMAL = "normal"
    HARD = "hard"


class WordleGame:
    def __init__(self, word_length=5, word=None, mode=GameMode.NORMAL):
        self.word_length = word_length
        self.mode = mode

        if word:
            self.word = word

        elif word_length == 5:
            self.word = random.choice(WORDS)

        elif word_length == 6:
            self.word = random.choice(SIX_LETTER_WORDS)

        else:
            raise ValueError("Unsupported word length")

        if self.mode == GameMode.NORMAL:
            self.guesses_remaining = 6
        else: 
            self.guesses_remaining = 8
        self.game_won = False

        self.letters = {
            chr(i): LetterState.UNKNOWN
            for i in range(ord("a"), ord("z") + 1)
        }

    def make_guess(self, guess):
        guess = guess.lower()

        if len(guess) != self.word_length:
            return f"Guess must be {self.word_length} letters"

        self.guesses_remaining -= 1

        guess_list = list(guess)
        split_word = list(self.word)

        score = [LetterState.GREY] * self.word_length


        for i in range(self.word_length):
            if guess_list[i] == split_word[i]:
                score[i] = LetterState.GREEN
                guess_list[i] = None
                split_word[i] = None


        for i in range(self.word_length):
            if guess_list[i] is not None and guess_list[i] in split_word:
                score[i] = LetterState.YELLOW
                split_word[split_word.index(guess_list[i])] = None


        if score == [LetterState.GREEN] * self.word_length:
            self.game_won = True

        for letter, state in zip(guess, score):
            if state > self.letters[letter]:
                self.letters[letter] = state

        if self.mode == GameMode.NORMAL:
            score_output = [state.name.lower() for state in score]
        else:
            counts = Counter(score)
            score_output = (
                f"{counts[LetterState.GREEN]} green{'s' if counts[LetterState.GREEN] != 1 else ''}, "
                f"{counts[LetterState.YELLOW]} yellow{'s' if counts[LetterState.YELLOW] != 1 else ''}, "
                f"{counts[LetterState.GREY]} gre{'ys' if counts[LetterState.GREY] != 1 else 'y'}"
            )    


        return {
            "score": score_output,
            "letters": {
            letter: state.name.lower()
            for letter, state in self.letters.items()
            },
            "guesses_remaining": self.guesses_remaining,
}

class QuordleGame:
    def __init__(self):
        words = random.sample(
        [word for word in WORDS if len(word) == 5],
        4
)

        self.games = [
            WordleGame(word_length=5, word=word)
            for word in words
]
        self.guesses_remaining = 9

    def make_guess(self, word):

        if self.guesses_remaining <= 0:
            return "No guesses remaining"

        results = []
        valid_guess = False

        for game in self.games:

            if game.game_won:
                results.append({
                    "score": ["green"] * game.word_length,
                    "letters": {
                        letter: state.name.lower()
                        for letter, state in game.letters.items()
                    },
                    "guesses_remaining": self.guesses_remaining
                })
                continue

            result = game.make_guess(word)

            if isinstance(result, str):
                continue

            valid_guess = True

            results.append({
                "score": result["score"],
                "letters": dict(result["letters"]),
                "guesses_remaining": self.guesses_remaining
            })

        if valid_guess:
            self.guesses_remaining -= 1

        return results