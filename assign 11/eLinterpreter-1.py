from ast import parse
from random import random, uniform, randint, choice
import string
from syntax import *
# from semantics import *
from semantics_needs_completion import *

import os

PATH = os.getcwd()
# C:\Users\nickf\Dropbox\Classes\CS4700 Spring 2020\lisp interpreter


def readEvalLoop(program, trace=False):
    # program is a list of statements
    grammar = parseGrammar(PATH)
    # print(grammar)
    codeList = [parse(oneStatement) for oneStatement in program]
    for code in codeList:
        if checkSyntax(code, '<statement>', grammar):
            print("Syntax error?")
    answer = evalProgram(codeList, trace=trace)


def runProgram(fileName, trace=False):
    # reads the code in file name, parses it, check each statement, executes each statement
    global Trace
    Trace = trace
    grammar = parseGrammar(PATH)
    program = readInProgram(fileName)
    codeList = parseProgram(program)
    for code in codeList:
        if checkSyntax(code, '<statement>', grammar):
            print("Syntax error?")
    answer = evalProgram(codeList, trace=trace)


def readInProgram(fileName):
    # reads in a eL program, returns as one big string
    print("Reading %s" % (join(PATH, fileName),))
    with open(join(PATH, fileName), 'r') as file:  # Use file to refer to the file object
        lines = [l for l in file.readlines() if not l[0] == '#']
    whole = ""
    for line in lines:
        whole = whole + line
    return whole


fileName = "code.el"
# print(readInProgram(fileName))
runProgram(fileName, True)
