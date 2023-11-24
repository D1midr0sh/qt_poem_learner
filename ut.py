from difflib import SequenceMatcher
from math import log2


def similar(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()


def divide(lst: list, n: int):
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def algorithm(verses: list) -> list:
    """
    Generates a new list based on the input list of verses.
    """
    ans = []
    for i in range(1, len(verses) + 1):
        verse = verses[i - 1]
        for v in range(0, len(verse) - 1, 2):
            ans.append([verse[v], verse[v + 1]])
            if len(verse) % 2 == 1 and v == len(verse) - 3:
                ans[-1].append(verse[len(verse) - 1])
                continue
        if ans[-1] != verse:
            ans.append(verse)
        if i % 2 == 0:
            print("CHECK")
            to_check = []
            count = int(log2(i))
            if 2**count == i:
                for v in verses[:i]:
                    to_check.extend(v)
            else:
                for v in verses[i - 2**count + 1 : i]:
                    to_check.extend(v)
            ans.append(to_check)
    return ans


def find_mistakes(new: str, original: str) -> (dict, int, int):
    """
    Calculate the differences between two strings and find the mistakes.
    """
    first = new.split()
    second = original.split()
    dif = len(second) - len(first)
    mistakes = 0
    right_wrong = {}
    for i in range(min(len(first), len(second))):
        if first[i] != second[i]:
            if i == 0:
                right_wrong[" ".join(first[:2])] = " ".join(second[:2])
            elif i == min(len(first), len(second)):
                right_wrong[" ".join(first[i - 1 :])] = " ".join(second[i - 1 :])
            else:
                right_wrong[" ".join(first[i - 1 : i + 2])] = " ".join(
                    second[i - 1 : i + 2]
                )
            mistakes += 1
    return right_wrong, mistakes, dif


def number_declination(num: int) -> str:
    """
    Returns the appropriate declination of the word "слово" based on the given number.
    """
    if num % 10 == 1 and num % 100 != 11:
        return "слово"
    if 2 <= num % 10 <= 4:
        return "слова"
    return "слов"
