from .words import WORDS
import random
from enum import IntEnum

class LetterState(IntEnum):
    UNKNOWN = 0
    GREY = 1
    YELLOW = 2
    GREEN = 3

class WordleGame:
    def __init__(self):
        self.word = random.choice(WORDS)
        self.guesses_remaining = 6
        self.game_won = False
        self.letters = {
        chr(i): LetterState.UNKNOWN
        for i in range(ord("a"), ord("z") + 1)
    }
    
    def make_guess(self, guess):
        guess = guess.lower()
        if len(guess) != 5:
            return "Guess must be 5 letters"
        
        self.guesses_remaining -= 1

        guess_list = list(guess)
        split_word = list(self.word)
        score = [LetterState.GREY] * 5

        for i in range(5):
            if guess_list[i] == split_word[i]:
                score[i] = LetterState.GREEN
                guess_list[i] = None
                split_word[i] = None

        for i in range(5):
            if guess_list[i] is not None and guess_list[i] in split_word:
                score[i] = LetterState.YELLOW
                split_word[split_word.index(guess_list[i])] = None
        
        if score == [LetterState.GREEN] * 5:
            self.game_won = True

        for letter, state in zip(guess, score):
            if state > self.letters[letter]:
                self.letters[letter] = state


        return {
        "score": [state.name.lower() for state in score],
        "letters": {
         letter: state.name.lower()
            for letter, state in self.letters.items()
        },
        "guesses_remaining": self.guesses_remaining,
        "won": self.game_won,
}
