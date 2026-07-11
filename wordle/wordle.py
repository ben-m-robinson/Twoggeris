from words import WORDS
import random

class WordleGame:
    def __init__(self):
        self.word = random.choice(WORDS)
        self.guesses_remaining = 6
        self.game_won = False
    
    def make_guess(self, guess):
        guess = guess.lower()
        if len(guess) != 5:
            return "Guess must be 5 letters"
        
        self.guesses_remaining -= 1

        guess_list = list(guess)
        split_word = list(self.word)
        score = ["grey"] * 5

        for i in range(5):
            if guess_list[i] == split_word[i]:
                score[i] = "green"
                guess_list[i] = None
                split_word[i] = None

        for i in range(5):
            if guess_list[i] is not None and guess_list[i] in split_word:
                score[i] = "yellow"
                split_word[split_word.index(guess_list[i])] = None
        
        if score == ["green"] * 5:
            self.game_won = True

        return score

