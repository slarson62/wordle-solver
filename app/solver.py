import csv
import sys
from typing import List, Tuple


class Solver:
    """Class to guess a given word from a large corpus in the fewest tries possible

    Following the popular word game wordle hints as to correct character placement,
    character exists in the word but wrong placement and character does not exist
    in word this class takes a word and corpus of words to guess from and attempts
    to solve in as few tries as possible

    TODO: Weigh Different strategies in guessing the next word
    TODO: Is it better to guess only within the "available" words or whole corpus
    to eliminate the most available candidates for the next round?
    TODO: Add timing and optimize

    """

    def __init__(self, word, words) -> None:
        self.word = word or None
        self.words = words
        self.available_words = words
        self.direct_hits = set()
        self.hits = {}
        self.misses = set()
        self.round = 0

    def is_match(
        self, word: List[str], direct_hits: set, hits: dict, misses: set
    ) -> bool:
        # Determine if the word is a possible match based on known characters

        for m in misses:
            # word must NOT contain char in any position
            if m in word:
                return False
        for dh in direct_hits:
            # word must contain char in positions specified
            if word[dh[1]] != dh[0]:
                return False
        for letter in hits.keys():
            # word must contain char but not in positions specified
            positions = hits[letter]
            if letter not in word:
                return False
            else:
                for p in positions:
                    if word[p] == letter:
                        return False

        return True

    def get_available_words(
        self, direct_hits: set, hits: dict, misses: set
    ) -> List[str]:
        # Narrow the set of available words based on known characters

        av = []
        for word in self.available_words:
            if self.is_match(word, direct_hits, hits, misses):
                av.append(word)
        self.available_words = av if len(av) else self.available_words

        return self.available_words

    def get_best_guess(
        self, best_chars: List[str], available_words: List[List[str]]
    ) -> List[str]:
        # Get best based on the available list
        # Words that have the highest char count per placement
        # score each word

        word_scores = []
        for i in range(0, len(available_words)):
            score = 0
            for j in range(0, len(best_chars)):
                if available_words[i][j] == best_chars[j]:
                    score += 1
            word_scores.append(score)
        max_score = max(word_scores)
        return available_words[word_scores.index(max_score)]

    def get_stats(self, available_words: List[List[str]]) -> List[str]:
        # Get most frequent characters for each position base on statistics
        # from the available word list.
        # TODO: get top X per position with stats

        d = {}
        for i in range(0, len(available_words)):
            for j in range(0, 5):
                if j not in d.keys():
                    d[j] = []
                d[j].append(available_words[i][j])

        return [max(set(x[1]), key=x[1].count) for x in d.items()]

    def make_guess(self, guess: List[str]) -> bool:
        # Submit a guess and recalculate character assertions

        self.round += 1
        if self.word is not None:
            if self.word == guess:
                return True
            else:
                for i in range(0, len(guess)):
                    letter = guess[i]
                    if letter not in self.word:
                        self.misses.add(letter)
                    if guess[i] == self.word[i]:
                        self.direct_hits.add((letter, i))
                    if letter in self.word and guess[i] != self.word[i]:
                        if letter not in self.hits:
                            self.hits[letter] = {i}
                        else:
                            self.hits[letter].add(i)
            return False
        else:
            # TODO: Add logic for playing without knowing the word
            pass

    def _solve(self, tries: int) -> Tuple[int, int, int]:
        # For a given word generate solve statistics

        solved = 0
        for i in range(0, tries):
            aw = self.get_available_words(self.direct_hits, self.hits, self.misses)
            s = self.get_stats(aw)
            g = self.get_best_guess(s, aw)
            m = self.make_guess(g)
            if m:
                solved = 1
                break

        return self.round, len(self.available_words), solved


def load_words(filepath=None):
    words = []
    with open(filepath, newline="") as f:
        reader = csv.reader(f)
        try:
            for row in reader:
                if len(row) == 5:
                    words.append(row)
        except csv.Error as e:
            sys.exit("file {}, line {}: {}".format(filepath, reader.line_num, e))
        return words


if __name__ == "__main__":
    words = load_words("5_letters.csv")
    t = []
    l = []
    s = []
    ns = []
    for word in words:
        solver = Solver(word=word, words=words)
        tries, leftovers, solved = solver._solve(tries=6)
        t.append(tries)
        l.append(leftovers)
        s.append(solved)
        if not solved:
            ns.append("".join(word))

    print("Average Tries:  {:.2f}".format(sum(t) / len(t)))
    print("Average Words:  {:.2f}".format(sum(l) / len(l)))
    print("Percent Solved: {:.2f}".format(sum(s) / len(words)))

    print(ns)
