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
__copyright__ = "Copyright 2008-2014, Nestor Arocha"
__email__ = "nesaro@gmail.com"

from pydsl.Grammar.Alphabet import Encoding
from pydsl.Check import checker_factory
from pydsl.Grammar.Alphabet import Choice, GrammarCollection


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
            buffer += element
            for x in buffer:
                target.send(x)

#Create a graph that connects the base with the target through alphabets
#If every target is connected to any inputs, create the independent paths

#A1 A2
#|  |
#A3 A4
#|  |
#A5 |
#\  /
# A6

#Order is not always unique, as in the previous example A4 could be extracter after or before A3. At the moment the algorithm is to compute elements of the longest path first (extract elements from longest path every single time)


#Check that every element in the input belongs to base

#Call the lexers following the graph

class GeneralLexer(object):
    """Multi level lexer"""
    def __init__(self, alphabet, base):
        if not alphabet:
            raise ValueError
        self.alphabet = alphabet
        self.base = base

    @property
    def graph(self):
        """Creates the alphabet graph"""
        import networkx
        result = networkx.DiGraph()
        current_alphabet = self.alphabet
        if isinstance(current_alphabet, (GrammarCollection,)):
            pending_stack = list(current_alphabet)
        else:
            pending_stack = [current_alphabet]
        while pending_stack:
            current_alphabet = pending_stack.pop()
            if (isinstance(current_alphabet, Encoding) and current_alphabet == self.base) or \
                    (isinstance(current_alphabet, GrammarCollection) and current_alphabet in self.base):
                continue
            if isinstance(current_alphabet, (GrammarCollection,)):
                for element in current_alphabet:
                    result.add_edge(element, element.alphabet)
                    pending_stack.append(element.alphabet)
            else:
                result.add_edge(current_alphabet, current_alphabet.alphabet)
                pending_stack.append(current_alphabet.alphabet)
        #import matplotlib.pyplot as plt
        #plt.figure(figsize=(8,8))
        ## with nodes colored by degree sized by population
        #networkx.draw(result, with_labels=True)
        #plt.savefig("knuth_miles.png")
        return result

    def __call__(self, data, include_gd=False):
        for element in data:
            from pydsl.Check import check
            if not check(self.base, data):
                raise ValueError('Unexpected input grammar')
        graph = self.graph
        solved_elements = {}
        if include_gd:
            for alphabet in self.alphabetchain:
                lexer = lexer_factory(alphabet)
                response = lexer(data, include_gd = True)
                data, grammars = zip(*response)
            return zip(data, grammars)
        else:
            if isinstance(self.base, Encoding):
                self.graph.node[self.base]['data'] = data #Attach data to every element in the graph
                print(self.graph.predecessors(self.base))
                print(data)
            for element in self.alphabet: #FIXME: could be encoding
                print(self.graph.successors(element))

            for alphabet in self.alphabetchain:
                lexer = lexer_factory(alphabet)
                data = lexer(data, include_gd = False)
            return data

def digraph_walker_backwards(graph, element, call_back):
    """Visits every element guaranteeing that the previous elements have been visited before"""
    call_back(graph, element)
    for predecessor in graph.predecessor(element):
        digraph_walker_backwards(graph, predecessor, call_back)



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


def lexer_factory(alphabet, base = None):
    if isinstance(alphabet, Choice) and alphabet.alphabet == base:
        return ChoiceBruteForceLexer(alphabet)
    elif isinstance(alphabet, Encoding):
        if base is not None:
            raise ValueError
        return EncodingLexer(alphabet)
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
            current_alphabet = getattr(current_alphabet,"alphabet", None)
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

def is_ancestor(parent_alphabet, child_alphabet):
    """Tests if parent_alphabet is an ancestor of the child_alphabet"""
    alphabet = parent_alphabet
    while alphabet:
        if child_alphabet == alphabet:
            return True
        alphabet = alphabet.alphabet
    return False
