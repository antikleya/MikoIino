# -*- coding: utf-8 -*-

from rapidfuzz import fuzz


def is_words_similar(string: str, model: str) -> bool:
    """
    Calculates the Levenshtein distance between two strings
    """

    if fuzz.ratio(string, model, score_cutoff=75, preprocess=False):
        return True

    return False


def is_word_in_list(string: str, word_list: list) -> bool:
    """
    Find the similar word in list of words
    """

    for model in word_list:
        if fuzz.ratio(string, model, score_cutoff=75, preprocess=False):
            return True

    return False


def intersection(lst1: list, lst2: list) -> list:
    """
    Calculates the intersection of two lists
    """
    lst3 = [value for value in lst1 if value in lst2]
    return lst3
