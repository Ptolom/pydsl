#!/usr/bin/python
# -*- coding: utf-8 -*-
from pydsl.Check import checker_factory

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2013, Nestor Arocha"
__email__ = "nesaro@gmail.com"

import unittest
from pydsl.Parser.Backtracing import BacktracingErrorRecursiveDescentParser
from pydsl.File.BNF import load_bnf_file
from pydsl.Config import load


class TestLogicGrammars(unittest.TestCase):
    def setUp(self):
        #tokenlist definition
        self.tokelist5 = "True"

    def testLogicalExp(self):
        productionrulesetlogical = load_bnf_file("pydsl/contrib/grammar/LogicalExpression.bnf")
        #import pdb
        #pdb.set_trace()
        parser = BacktracingErrorRecursiveDescentParser(productionrulesetlogical)
        result = parser.get_trees(self.tokelist5)
        self.assertTrue(result)

    def testTrueFalse(self):
        productionrulesetlogical = load_bnf_file("pydsl/contrib/grammar/TrueFalse.bnf")
        parser = BacktracingErrorRecursiveDescentParser(productionrulesetlogical)
        result = parser.get_trees(self.tokelist5)
        self.assertTrue(result)

    def testLogicalExpression(self):
        productionrulesetlogical = load_bnf_file("pydsl/contrib/grammar/LogicalExpression.bnf")
        parser = BacktracingErrorRecursiveDescentParser(productionrulesetlogical)
        result = parser.get_trees("True&&False")
        self.assertTrue(result)
        result = parser.get_trees("True&|False")
        self.assertFalse(result)



class TestHTMLGrammars(unittest.TestCase):
    def testHTMLTable(self):
        productionrulesetlogical = load_bnf_file("pydsl/contrib/grammar/TrueHTMLTable.bnf")
        parser = BacktracingErrorRecursiveDescentParser(productionrulesetlogical)
        from pydsl.Lex import lex
        lexed = [x[0] for x in lex(productionrulesetlogical.alphabet, "<table><tr><td>1</td></tr></table>")]
        result = parser.get_trees(lexed)
        self.assertTrue(result)
        lexed = [x[0] for x in lex(productionrulesetlogical.alphabet, "<table><td>1</td></tr></table>")]
        result = parser.get_trees(lexed)
        self.assertFalse(result)


class TestLogGrammar(unittest.TestCase):
    def testLogLine(self):
        grammar = load("logline")
        checker = checker_factory(grammar)
        original_string = "1.2.3.4 - - [1/1/2003:11:11:11 +2] \"GET\" 1 1 \"referer\" \"useragent\""
        from pydsl.Lex import lex
        tokenized = [x[0] for x in lex(grammar.alphabet, original_string)]
        self.assertTrue(checker.check(tokenized))
        self.assertFalse(checker.check("1.2.3.4 - - [1/1/2003:11:11:11 +2] \"GOT\" 1 1 \"referer\" \"useragent\""))
