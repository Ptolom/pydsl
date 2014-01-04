#!/usr/bin/python
# -*- coding: utf-8 -*-
# This file is part of pydsl.
#
# pydsl is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
# pydsl is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pydsl.  If not, see <http://www.gnu.org/licenses/>.

"""Base Lexer classes"""

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2013, Nestor Arocha"
__email__ = "nesaro@gmail.com"

from pydsl.Grammar.Alphabet import Encoding
from pydsl.Check import checker_factory


class EncodingLexer(object):

    """Special Lexer that encodes from a string a reads a string"""

    def __init__(self, encoding):
        self.encoding = encoding

    def __call__(self, string):
        for x in string:
            yield x

    def lexer_generator(self, target):
        next(target)
        buffer = ""
        while True:
            element = (yield)
            buffer += element  # Asumes string
            for x in buffer:
                target.send(x)

class GeneralLexer(object):
    def __init__(self, alphabet, base):
        self.alphabetchain = alphabetchain

    def __call__(self, data, include_gd=False):
        if include_gd:
            for alphabet in self.alphabetchain:
                lexer = lexer_factory(alphabet)
                response = lexer(data, include_gd = True)
                data, grammars = zip(*response)
            return zip(data, grammars)
        else:
            for alphabet in self.alphabetchain:
                lexer = lexer_factory(alphabet)
                data = lexer(data, include_gd = False)
            return data



class ChoiceLexer(object):

    """Lexer receives an Alphabet in the initialization (A1).
    Receives an input that belongs to A1 and generates a list of tokens in a different Alphabet A2
    It is always described with a regular grammar"""

    def __init__(self, alphabet):
        self.load(None)
        self.alphabet = alphabet

    def load(self, string):
        self.string = string
        self.index = 0

    def __call__(self, string, include_gd=True):  # -> "TokenList":
        """Tokenizes input, generating a list of tokens"""
        self.load(string)
        result = []
        while True:
            try:
                result.append(self.nextToken(include_gd))
            except:
                break
        return result

    def lexer_generator(self):
        """generator version of the lexer, yields a new token as soon as possible"""
        raise NotImplementedError

    def nextToken(self, include_gd=False):
        from pydsl.Tree import Sequence
        best_right = 0
        best_gd = None
        for gd in self.alphabet:
            checker = checker_factory(gd)
            left = self.index
            for right in range(left +1, len(self.string) +1):
                if checker.check(self.string[left:right]): #TODO: Use match
                    if right > best_right:
                        best_right = right
                        best_gd = gd
        if not best_gd:
            raise Exception("Nothing consumed")
        if include_gd:
            result = self.string[self.index:best_right], best_gd
        else:
            result = self.string[self.index:best_right]
        self.index = right
        return result


class ChoiceBruteForceLexer(object):

    """Attempts to generate the smallest token sequence by evaluating every accepted sequence"""

    def __init__(self, alphabet):
        self.alphabet = alphabet

    @property
    def current(self):
        """Returns the element under the cursor until the end of the string"""
        return self.string[self.index:]

    def __call__(self, string, include_gd=True):  # -> "TokenList":
        """Tokenizes input, generating a list of tokens"""
        self.string = string
        return [x for x in self.nextToken(include_gd)]

    def nextToken(self, include_gd=False):
        from pydsl.Tree import Sequence
        tree = Sequence()  # This is the extract algorithm
        valid_alternatives = []
        for gd in self.alphabet:
            checker = checker_factory(gd)
            for left in range(0, len(self.string)):
                for right in range(left +1, len(self.string) +1 ):
                    if checker.check(self.string[left:right]):
                        valid_alternatives.append((left, right, gd))
        if not valid_alternatives:
            raise Exception("Nothing consumed")
        for left, right, gd in valid_alternatives:
            string = self.string[left:right]
            tree.append(left, right, string, gd, check_position=False)

        right_length_seq = []
        for x in tree.valid_sequences():
            if x[-1]['right'] == len(self.string):
                right_length_seq.append(x)
        if not right_length_seq:
            raise Exception("No sequence found for input %s alphabet %s" % (self.string,self.alphabet))
        for y in sorted(right_length_seq, key=lambda x:len(x))[0]: #Always gets the match with less tokens
            if include_gd:
                yield y['content'], y.get('gd')
            else:
                yield y['content']

    def lexer_generator(self, target):
        next(target)
        buffer = ""
        while True:
            element = (yield)
            buffer += element  # Asumes string
            for x in range(1, len(buffer)):
                currentstr = buffer[:x]
                for gd in self.alphabet:
                    checker = checker_factory(gd)
                    if checker.check(currentstr):
                        buffer = buffer[x:]
                        target.send(currentstr)


class GrammarCollectionLexer(object):
    def __init__(self, alphabet):
        self.alphabet = alphabet

    @property
    def base_alphabet(self):
        return common_ancestor(self.alphabet)

def lexer_factory(alphabet, base = None):
    from pydsl.Grammar.Alphabet import Choice, AlphabetChain, GrammarCollection
    if isinstance(alphabet, Choice) and alphabet.alphabet == base:
        return ChoiceBruteForceLexer(alphabet)
    elif isinstance(alphabet, Encoding):
        if base is not None:
            raise ValueError
        return EncodingLexer(alphabet)
    elif isinstance(alphabet, GrammarCollection) and base == common_ancestor(alphabet):
        return GrammarCollectionLexer(alphabet)
    else:
        return GeneralLexer(alphabet, base)

def lex(alphabet, base, data):
    return lexer_factory(alphabet, base)(data)


def common_ancestor(alphabet):
    """Discovers the alphabet common to every element in the input"""
    expanded_alphabet_list = []
    for gd in alphabet:
        expanded_alphabet_list_entry = []
        from pydsl.Grammar.Alphabet import Alphabet
        if isinstance(gd, Alphabet):
            expanded_alphabet_list_entry.append(gd)
        current_alphabet = gd.alphabet
        while current_alphabet is not None:
            expanded_alphabet_list_entry.append(current_alphabet)
            current_alphabet = current_alphabet.alphabet
        expanded_alphabet_list.append(expanded_alphabet_list_entry)
    flat_alphabet_list = []
    for entry in expanded_alphabet_list:
        for alphabet in entry:
            if alphabet not in flat_alphabet_list:
                flat_alphabet_list.append(alphabet)
    common_alphabets = [x for x in flat_alphabet_list if all((x in y for y in expanded_alphabet_list))]
    if len(common_alphabets) != 1:
        raise NotImplementedError
    return common_alphabets[0]

