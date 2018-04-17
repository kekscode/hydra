#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import glob
import time
import logging
import itertools
import concurrent.futures

logging.basicConfig(level=os.environ.get("LOGLEVEL", "DEBUG"), format="%(asctime)s;%(levelname)s;%(message)s")
logger = logging.getLogger(sys.argv[0])


def is_anagram(a, b):
    """
    Checks if a and b is an anagram
    :param a: str
    :param b: str
    :return: bool
    """

    a = a.lower()
    b = b.lower()

    if a == b:  # words are identical anyway, so we can bail out early
        return False

    def count_items(sequence):
        """
        Helper function which counts letters in words like:
        {'p': 1, 'u': 1, 'l': 2, 'e': 1, 'd': 1} for "pulled"
        :param sequence: str
        :return: dict
        """
        counts = {}
        for item in sequence:
            counts[item] = counts.get(item, 0) + 1
        return counts

    """
    Compares the letter counts of two words
    If both words have the same letter counts,
    an anagram has been discovered like salt/last:
    {'s': 1, 'a': 1, 'l': 1, 't': 1} == {'l': 1, 'a': 1, 's': 1, 't': 1}
    """
    return count_items(a) == count_items(b)


def parse_file(file):
    """
    Parses a text file, removes non-alphabetical characters and returns a deduplicated set of words
    :param file: file
    :return: set
    """
    with open(file, 'r') as f:
        c = f.read()
        clean = ' '.join(e for e in c.split() if e.isalpha())  # filter special characters

    # Deduplicate words
    w = set(itertools.chain(clean.split()))

    return w


def log_anagrams(words):
    """
    Checks for anagrams in words
    :param words: set
    """
    anagrams = set()
    for word in words:
        for candidate in words:
            if is_anagram(word, candidate):
                anagrams.add(word.lower())  # Add lowercased anagram to global list
                logger.debug(f"Anagram found: {word} | {candidate}")


def normal_execution(files):
    """Execute in current (main) thread"""
    for file in files:
        log_anagrams(parse_file(file))


def threaded_execution(files):
    """Execute in threads"""
    with concurrent.futures.ThreadPoolExecutor() as e:
        for file in files:
            e.submit(log_anagrams, parse_file(file))


def parallel_execution(files, workers):
    """Execute in parallel"""
    with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as e:
        for file in files:
            e.submit(log_anagrams, parse_file(file))


if __name__ == "__main__":
    files = glob.glob("./data/*.txt")

    start_time = time.time()

    normal_execution(files)        # 120.07317686080933 seconds.

    """
    threaded_execution(files)      # 127.38437008857727 seconds.
    parallel_execution(files, 4)   # 61.94759774208069 seconds.
    parallel_execution(files, 8)   # 63.37737989425659 seconds.
    parallel_execution(files, 9)   # 59.63384199142456 seconds.
    parallel_execution(files, 16)  # 64.44105505943298 seconds.
    """

    logger.info(f"Ran for: {(time.time() - start_time)} seconds.")
