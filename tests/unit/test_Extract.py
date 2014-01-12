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

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2013, Nestor Arocha"
__email__ = "nesaro@gmail.com"

import unittest
from pydsl.Extract import extract, extract_alphabet
from pydsl.Grammar import RegularExpression, String
from pydsl.Grammar.Alphabet import Encoding, Choice


class TestGrammarExtract(unittest.TestCase):

    def testRegularExpression(self):
        gd = RegularExpression('^[0123456789]*$')
        expected_result = [(3, 4, '1'), (3, 5, '12'), (3, 6, '123'), (3, 7, '1234'), (4, 5, '2'), (4, 6, '23'), (4, 7, '234'), (5, 6, '3'), (5, 7, '34'), (6, 7, '4')]
        self.assertListEqual(extract(gd,'abc1234abc'), expected_result)
        self.assertRaises(Exception, extract, None)
        self.assertListEqual(extract(gd,''), []) #Empty input


class TestAlphabetExtract(unittest.TestCase):

    def testEncoding(self):
        ad = Encoding('ascii')
        self.assertListEqual(extract(ad,'a£'), [(0,1,'a')])
        self.assertListEqual(extract(ad,''), [])
        self.assertRaises(Exception, extract, None)

    def testChoices(self):
        gd = Choice([String('a'), String('b'), String('c')])
        self.assertListEqual(extract_alphabet(gd,'axbycz'), [(0,1,'a'), (2,3, 'b'), (4,5,'c')])
        self.assertListEqual(extract_alphabet(gd,'xyzabcxyz'), [(3,6,'abc')])
        self.assertListEqual(extract_alphabet(gd,'abcxyz'), [(0,3,'abc')])
        self.assertListEqual(extract_alphabet(gd,'abc'), [(0,3,'abc')])
        self.assertListEqual(extract_alphabet(gd,''), [])
