from difflib import SequenceMatcher
from math import log2


def similar(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()


def divide(lst: list, n: int):
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def algorithm(verses: list) -> list:
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
