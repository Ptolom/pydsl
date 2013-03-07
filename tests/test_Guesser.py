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


class TestGuess(unittest.TestCase):
    def testBasic(self):
        from pydsl.Guesser import Guess
        guesser = Guess()
        self.assertListEqual(guesser.guess('1234'), ['integer','cstring','ascii'])
        self.assertListEqual(guesser.guess_alphabet('1234'), ['ascii'])
        self.assertListEqual(guesser.guess_grammar('1234'), ['integer','cstring'])
        self.assertRaises(guesser.guess(None))

    def testGuessLoad(self):
        gd = None
        from pydsl.Memory.Loader import load_guesser
        guesser = load_guesser(gd)
        self.assertTrue(guesser("input"))

