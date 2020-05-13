"""
write a small function that ask the user to type a text and then display to the user the statistics of his/her typing.
The statistics should contain the below elements :

1/ The total number of characters inside his/her typing.
2/ The list of characters used inside his/her typing.
3/ A dictionary in which each pair represents a character with its occurrences.
4/ The dictionary in which each pair represents a character with a tuple composed of its attributes above (occurrnces
and parity).
5/ Alternate the position of occurrences and parity while building that latest dictionary.
For the first pair, if you use (occurrence, parity) then for the next you should use (parity, occurrence).

--- Example

+ User input : try to solve that challenge - just get a try 0004.

--- Expected output :

+ number of characters : 50
+ list of characters : ['t', 'r', ' ', 'o', 's', 'l', 'v', 'e', 'h', 'a', 'n', 'g', '-', 'j', 'u', 'y', '0', '4', '.']
+ dictionary of occurrences : {'t':6 , 'r':2, ' ':10, 'o':2, 's':2, 'l':3, 'v':1, 'e':4, 'h':2, 'a':3, 'n':1, 'g':2,
'-':1, 'j':1, 'u':1, 'y':2, '0':3, '4':1, '.':1}
+ dictionary of attributes : {'t':(6, 'even') , 'r':('even',2), ' ':(10, 'even'), 'o':('even',2), 's':(2,'even'),
'l':('odd',3), 'v':(1,'odd'), 'e':('even',4), 'h':(2,'even'), 'a':('odd',3), 'n':(1,'odd'), 'g':('even',2), '-':(1,
'odd'), 'j':('odd',1), 'u':(1,'odd'), 'y':('even',2), '0':(3,'odd'), '4':('odd',1), '.':(1,'odd')}
"""

from collections import Counter, defaultdict
from time import time
from random import choices
from string import ascii_lowercase
from typing import List, Dict, Optional, Callable


def short_solution(target: str) -> None:
    list_of_characters = list(set(target))
    dictionary_of_occurrences = dict(Counter(target))

    # hard to read one-liner: not a good example :-)
    # % is the modulo operator in Python
    # x % 2 is 1 for odd numbers and 0 for even numbers
    # b/c 1 is equivalent to True an 0 is equivalent to False the expression x % 2 evaluates to True for odd values
    # of x.
    # (k, v, 'odd' if v % 2 else 'even') for k, v in dictionary_of_occurrences.items()
    # --> generator expression: generates triples with character, number of occurrences and 'odd' or 'even' where the
    # latter depends on whether the # of occurrences are even
    # enumerate((k, v, 'odd' if v % 2 else 'even') for k, v in dictionary_of_occurrences.items())
    # --> generator: generates a tuple with index (starting with zero) and one of above triples
    # finally the full expression is a dict comprehension creating a dictionary with the character as key and a tuple
    # as value. The tuple has either even/odd followed by the number of occurrences (s, v) or the number of occurrences
    # followed by even/odd. The order alternates.
    dictionary_of_attributes = {k: (v, s) if i % 2 else (s, v) for i, (k, v, s) in enumerate(
        (k, v, 'odd' if v % 2 else 'even') for k, v in dictionary_of_occurrences.items())}

    print(f'number of characters : {len(target)}')
    print(f'list of characters : {list_of_characters}')
    print(f'dictionary of occurrences : {dictionary_of_occurrences}')
    print(f'dictionary of attributes : {dictionary_of_attributes}')


def list_of_characters_using_list(target: str) -> List[str]:
    # initialize as empty list
    list_of_characters = []
    for i in range(len(target)):
        c = target[i]
        if c not in list_of_characters:
            list_of_characters.append(c)
    return list_of_characters


def list_of_characters_using_list_no_for(target: str) -> List[str]:
    # initialize as empty list
    list_of_characters = []
    for c in target:
        if c not in list_of_characters:
            list_of_characters.append(c)
    return list_of_characters


def list_of_characters_using_list_avoid_in(target: str) -> List[str]:
    # initialize as empty dict
    list_of_characters = {}
    for c in target:
        list_of_characters[c] = ''
    return list(list_of_characters)


def dictionary_of_occurrences_direct(target: str) -> Dict[str, int]:
    # initialize as empty dict
    dictionary_of_occurrences = {}
    for c in target:
        if c in dictionary_of_occurrences:
            dictionary_of_occurrences[c] += 1
        else:
            dictionary_of_occurrences[c] = 1
    return dictionary_of_occurrences


def dictionary_of_occurrences_direct_try(target: str) -> Dict[str, int]:
    # initialize as empty dict
    dictionary_of_occurrences = {}
    for c in target:
        try:
            dictionary_of_occurrences[c] += 1
        except KeyError:
            dictionary_of_occurrences[c] = 1
    return dictionary_of_occurrences


def dictionary_of_occurrences_direct_using_get(target: str) -> Dict[str, int]:
    # initialize as empty dict
    dictionary_of_occurrences = {}
    for c in target:
        dictionary_of_occurrences[c] = dictionary_of_occurrences.get(c, 0) + 1
    return dictionary_of_occurrences


def dictionary_of_occurrences_direct_defaultdict(target: str) -> Dict[str, int]:
    # initialize as empty dict
    dictionary_of_occurrences = defaultdict(int)
    for c in target:
        dictionary_of_occurrences[c] += 1
    return dictionary_of_occurrences


def time_it(code: Callable, cycles: Optional[int] = 100000) -> float:
    """
    Execute some code a number of times and measure the time
    :param code: code to execute
    :param cycles: number of cycles
    :return: seconds per execution
    """
    start = time()
    for _ in range(cycles):
        code()
    return (time() - start) / cycles


if __name__ == '__main__':
    """
    Example output generated by below code:
        number of characters : 50
        list of characters : ['h', 't', '.', 'r', 'v', 'a', '0', 'u', 'g', 'c', ' ', 's', '4', 'e', '-', 'o', 'n', 
        'y', 'l', 'j']
        dictionary of occurrences : {'t': 7, 'r': 2, 'y': 2, ' ': 10, 'o': 2, 's': 2, 'l': 3, 'v': 1, 'e': 4, 'h': 2, 
        'a': 3, 'c': 1, 'n': 1, 'g': 2, '-': 1, 'j': 1, 'u': 1, '0': 3, '4': 1, '.': 1}
        dictionary of attributes : {'t': ('odd', 7), 'r': (2, 'even'), 'y': ('even', 2), ' ': (10, 'even'), 
        'o': ('even', 2), 's': (2, 'even'), 'l': ('odd', 3), 'v': (1, 'odd'), 'e': ('even', 4), 'h': (2, 'even'), 
        'a': ('odd', 3), 'c': (1, 'odd'), 'n': ('odd', 1), 'g': (2, 'even'), '-': ('odd', 1), 'j': (1, 'odd'), 
        'u': ('odd', 1), '0': (3, 'odd'), '4': ('odd', 1), '.': (1, 'odd')}
        
        Timing some alternatives...
        list_of_characters_using_lists: 285.922 us
        list_of_characters_using_lists_no_for: 248.089 us
        list_of_characters_using_list_avoid_in: 44.528 us
        list(set(target)): 15.462 us
        
        dictionary_of_occurrences_direct: 99.893 us
        dictionary_of_occurrences_direct_try: 96.650 us
        dictionary_of_occurrences_direct_using_get: 113.266 us
        dictionary_of_occurrences_direct_defaultdict: 83.405 us
        dict(Counter(target)): 53.148 us
    
    Clearly shows:
        * iterating over a string is more efficient than slicign out the individual characters
        * using "in" on a growing list is inefficient
        * implementation of dict access in Python is very efficient
        * exception handling is very efficient; actually in some cases cheaper than explicit error avoidance code
        * tyring to use Python internals (set, Counter, ..) pays off

    """
    # the short solution
    target_str = 'try to solve that challenge - just get a try 0004.'
    short_solution(target=target_str)

    # let's try some variants with a looong random string
    # and time the execution time of each variant
    print()
    print('Timing some alternatives...')
    target_str = ''.join(choices(ascii_lowercase, k=1000))
    print(
        f'list_of_characters_using_lists: '
        f'{time_it(lambda: list_of_characters_using_list(target_str)) * 1000000:.03f} us')
    print(
        f'list_of_characters_using_lists_no_for: '
        f'{time_it(lambda: list_of_characters_using_list_no_for(target_str)) * 1000000:.03f} us')
    print(
        f'list_of_characters_using_list_avoid_in: '
        f'{time_it(lambda: list_of_characters_using_list_avoid_in(target_str)) * 1000000:.03f} us')
    print(
        f'list(set(target)): '
        f'{time_it(lambda: list(set(target_str))) * 1000000:.03f} us')

    print()

    print(
        f'dictionary_of_occurrences_direct: '
        f'{time_it(lambda: dictionary_of_occurrences_direct(target_str)) * 1000000:.03f} us')
    print(
        f'dictionary_of_occurrences_direct_try: '
        f'{time_it(lambda: dictionary_of_occurrences_direct_try(target_str)) * 1000000:.03f} us')
    print(
        f'dictionary_of_occurrences_direct_using_get: '
        f'{time_it(lambda: dictionary_of_occurrences_direct_using_get(target_str)) * 1000000:.03f} us')
    print(
        f'dictionary_of_occurrences_direct_defaultdict: '
        f'{time_it(lambda: dictionary_of_occurrences_direct_defaultdict(target_str)) * 1000000:.03f} us')
    print(
        f'dict(Counter(target)): '
        f'{time_it(lambda: dict(Counter(target_str))) * 1000000:.03f} us')
