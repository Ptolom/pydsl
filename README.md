DESCRIPTION
===========

pydsl is an environment for creating and using formal languages. 
The main idea is to allow an easy way to define, use and combine DSLs to create programs.
pydsl support several grammar specification formats:
 * regular expressions
 * pydsl BNF format
 * ANLTR .g format (not supported yet)
 * mongo database query dictionaries

each grammar definition have the following properties:
 * enumerate(gd): yields a list of accepted words
 * first(gd): yields a list of the first accepted subword/char
 * min(gd): length of the smaller accepted word
 * max(gd): length of the biggest accepted word

pydsl offer a set of functionalities that use _grammar definitions_
 * check(gd, input): test the input string against the spec
 * validate(gd, input): test the input string against the spec. In case of failure, it returns a list of errors
 * guess(input, [gd]): returns a list of _grammar definitions_ that are compatible with the input
 * getgroup(gd, input, tag): returns the parts of the input according to a tag
 * extract(gd, input): extract all the slices of the input that are accepted by _grammar definition_
 * distance(gd, input1, input2): returns the distance between two inputs according to _grammar definition_
 * translate(gd, input): generic translator
   * ast(astdefinition, input): creates an abstract syntax tree according to astdefinition


REQUIREMENTS
============
 * python >= 3.0
 * pydsl contrib package ( https://github.com/nesaro/pydsl-contrib )

INSTALLATION
============
python setup.py install

BINARIES
========
Memory Management
-----------------
 * info.py: Retrieves an element from memory and shows a summary
 * search.py: Searchs memory 

Grammars
--------
 * check.py: Checks if input data belongs to a grammar
 * guess:py: Determines input data type
 * validate.py: Perform a validation routine for user data according to a grammar

Functions
---------
 * translate.py: Process user input using a function

HELP
====
 * http://github.com/nesaro/pydsl
 * nesaro@gmail.com

LICENSE
=======
see LICENSE file

ABOUT
=====
pydsl is a formal and natural language framework.
Copyright (C) 2008-2012 Nestor Arocha Rodriguez (nesaro@gmail.com)

