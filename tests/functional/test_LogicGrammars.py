#!/usr/bin/python
# -*- coding: utf-8 -*-
from pydsl.Check import checker_factory

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2013, Nestor Arocha"
__email__ = "nesaro@gmail.com"

import unittest
from pydsl.Parser.Backtracing import BacktracingErrorRecursiveDescentParser
from pydsl.File.BNF import load_bnf_file
from pydsl.Lex import lex
from pydsl.Grammar import RegularExpression


class TestLogicGrammars(unittest.TestCase):
    def setUp(self):
        #tokenlist definition
        self.tokelist5 = "True"

    def testLogicalExp(self):
        repository = {'TrueFalse':load_bnf_file("pydsl/contrib/grammar/TrueFalse.bnf")}
        productionrulesetlogical = load_bnf_file("pydsl/contrib/grammar/LogicalExpression.bnf", repository)
        parser = BacktracingErrorRecursiveDescentParser(productionrulesetlogical)
        tokens = [x[0] for x in lex(repository['TrueFalse'].alphabet, self.tokelist5)]
        from pydsl.Lex import common_ancestor
        from pydsl.Grammar.Alphabet import Encoding
        self.assertEqual(common_ancestor(productionrulesetlogical.alphabet), Encoding('ascii'))
        tokens = [x[0] for x in lex(productionrulesetlogical.alphabet, tokens)]
        result = parser.get_trees(tokens)
        self.assertTrue(result)

    def testTrueFalse(self):
        productionrulesetlogical = load_bnf_file("pydsl/contrib/grammar/TrueFalse.bnf")
        parser = BacktracingErrorRecursiveDescentParser(productionrulesetlogical)
        tokens = [x[0] for x in lex(productionrulesetlogical.alphabet, self.tokelist5)]
        result = parser.get_trees(tokens)
        self.assertTrue(result)

    def testLogicalExpression(self):
        repository = {'TrueFalse':load_bnf_file("pydsl/contrib/grammar/TrueFalse.bnf")}
        productionrulesetlogical = load_bnf_file("pydsl/contrib/grammar/LogicalExpression.bnf", repository)
        parser = BacktracingErrorRecursiveDescentParser(productionrulesetlogical)
        tokens = [x[0] for x in lex(productionrulesetlogical.alphabet, "True&&False")]
        result = parser.get_trees(tokens)
        self.assertTrue(result)
        result = parser.get_trees("True&|False")
        self.assertFalse(result)



class TestHTMLGrammars(unittest.TestCase):
    def testHTMLTable(self):
        repository = {'integer':RegularExpression("^[0123456789]*$")}
        productionrulesetlogical = load_bnf_file("pydsl/contrib/grammar/TrueHTMLTable.bnf", repository)
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
        repository = {'space':RegularExpression("^ $"), 
                'integer':RegularExpression("^[0123456789]*$"),
                'ipv4':RegularExpression("^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$"),
                'characters':RegularExpression("^[A-z]+$")}
        grammar = load_bnf_file("pydsl/contrib/grammar/logline.bnf", repository)
        checker = checker_factory(grammar)
        original_string = "1.2.3.4 - - [1/1/2003:11:11:11 +2] \"GET\" 1 1 \"referer\" \"useragent\""
        from pydsl.Lex import lex
        tokenized = [x[0] for x in lex(grammar.alphabet, original_string)]
        self.assertTrue(checker.check(tokenized))
        self.assertFalse(checker.check("1.2.3.4 - - [1/1/2003:11:11:11 +2] \"GOT\" 1 1 \"referer\" \"useragent\""))
