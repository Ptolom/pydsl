#!/usr/bin/python
# -*- coding: utf-8 -*-
#This file is part of pydsl.
#
#pydsl is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#pydsl is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with pydsl.  If not, see <http://www.gnu.org/licenses/>.

"""Test wrapper"""
from pydsl.Config import GLOBALCONFIG
from pydsl.Parser.Parser import parser_factory
from pydsl.Validate import validator_factory
from pydsl.Lex import lex

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2013, Nestor Arocha"
__email__ = "nesaro@gmail.com"

import unittest
from pydsl.File.BNF import load_bnf_file
from pydsl.Grammar import RegularExpression
from pydsl.File.Python import load_python_file

class TestValidate(unittest.TestCase):
    def testBasic(self):
        integer = RegularExpression("^[0123456789]*$")
        date = load_bnf_file("pydsl/contrib/grammar/Date.bnf", {'integer':integer, 'DayOfMonth':load_python_file('pydsl/contrib/grammar/DayOfMonth.py')})
        parser = parser_factory(date, 'descent')
        tokenized = [x[0] for x in lex(date.alphabet, "11/11/2011")]
        self.assertTrue(parser.get_trees(tokenized, True)[0].valid)
        tokenized = [x[0] for x in lex(date.alphabet, "11/11//")]
        self.assertFalse(parser.get_trees(tokenized, True)[0].valid)
        self.assertRaises(Exception, lex, date.alphabet, "11/11/ab")

    def testValidateLoad(self):
        from pydsl.contrib.bnfgrammar import productionset0
        from pydsl.Grammar import String

        validator = validator_factory(productionset0)
        self.assertTrue(validator([String("S"), String("S")]))

    def testEmptyInput(self):
        pass
