from random import random, randint

import os

# define all the possible operators and how many arguments they take
Operators = ['+', '-', '*', '/', 'if', 'and', 'or', 'not', '>', 'eq']
NumberOfArguments = {}
ArgumentCount = [(1, ['not']), (2, ['+', '-', '*', '/', 'and', 'or', 'eq']), (3, ['if'])]
# fill the mapping from operator to argument count
for (count, operators) in ArgumentCount:
    for op in operators:
        NumberOfArguments[op] = count

############## STARTER CODE ####################################################
# only simple math to start with
Operators = ['+', '-', '*', '/']


def generateRandomExpression(maxDepth=10):
    # generates a string that is a legal sentence in the grammar of our simple lisp language
    if random() < 0.1 or maxDepth < 0:
        return str(randint(0, 100))
    else:
        return "(%s %s %s)" % (Operators[randint(0, 3)],
                               generateRandomExpression(maxDepth - 1),
                               generateRandomExpression(maxDepth - 1))


def atom(token):
    # changes a token to an actual integer 
    if token.isdigit():
        return int(token)
    return token


def genGood():
    # Generate a set of correct random test problems
    with open(PATH + 'correctSyntax.txt', 'w') as file:  # Use file to refer to the file object
        for _ in range(0, 1000):
            file.write(generateRandomExpression(1 + randint(0, 10)) + "\n")


def genBad():
    with open(PATH + 'errorSyntax.txt', 'w') as file:  # Use file to refer to the file object
        for _ in range(0, 1000):
            program = generateBadRandomExpression(1 + randint(0, 10))  # (1 + randint(0,10))
            try:  # try to parse the expression
                parseTree = parse(program)
            # Only if it does not parse then we save
            except Exception as error:
                file.write(program + "\n")


BadOps = ['_', '=', '(', '%']
BadNumbers = ['1.2344', 'x', 'y']


def generateBadRandomExpression(maxDepth=10):
    # generates a string that is a legal sentence in the grammar of our simple lisp language
    if random() < 0.1 or maxDepth < 0:
        return str(randint(0, 100))
    if random() < 0.05 or maxDepth < 0:
        return str(BadNumbers[randint(0, len(BadNumbers) - 1)])
    elif random() < 0.05:
        return "(%s %s %s" % (Operators[randint(0, 3)],
                              generateBadRandomExpression(maxDepth - 1),
                              generateBadRandomExpression(maxDepth - 1))
    elif random() < 0.05:
        return "%s %s %s)" % (Operators[randint(0, 3)],
                              generateBadRandomExpression(maxDepth - 1),
                              generateBadRandomExpression(maxDepth - 1))
    else:
        return "(%s %s %s)" % (Operators[randint(0, 3)],
                               generateBadRandomExpression(maxDepth - 1),
                               generateBadRandomExpression(maxDepth - 1))


### takes a program string and returns a parse tree
def parse(programStr):
    # returns the input string as a parse tree, represented as either an int or a list of expressions

    tokens = tokenize(programStr)

    if paraCheck(tokens):
        tokens = [x for x in tokens if x != ")"]
        tokens = [y for y in tokens if y != "("]

        tree = createParseTree(tokens)
        return tree

    else:
        raise Exception("Improper Syntax")


def createParseTree(tokens):
    currToken = tokens.pop(0)

    if isinstance(currToken, int):
        return currToken

    elif currToken in Operators:
        try:
            return [currToken, createParseTree(tokens), createParseTree(tokens)]
        except Exception as argError:
            raise Exception("Improper Syntax")


def paraCheck(tokens):
    isPara = False
    paras = []

    for token in tokens:
        if token == "(":
            paras.append(token)
            isPara = True

        elif token == ")":
            isPara = True
            if len(paras) > 0 and (paras[len(paras) - 1] == "("):
                paras.pop()
            else:
                return False

    if len(paras) == 0 and isPara:
        return True
    else:
        return False


### prettyPrint an expression (parsed list of tokens)
def prettyPrintExp(expression, depth=0):
    # takes a parse tree and prints it out so it is easier to read (maybe)
    if isinstance(expression, int):
        print("%s %d" % (' ' * depth, expression))
    else:
        print("%s(%s " % (' ' * depth, expression[0]))
        prettyPrintExp(expression[1], depth + 2)
        prettyPrintExp(expression[2], depth + 2)
        print("%s) " % (' ' * (depth + 1)))


### prettyPrint a list of tokens
def prettyPrint(tokenList, depth=0):
    token = tokenList.pop(0)
    # atom, just print at depth and return

    if isinstance(token, int):
        print("%s%d" % (' ' * depth, token))
    else:
        # compound expression
        operator = tokenList.pop(0)
        print("%s(%s" % (' ' * depth, operator))
        prettyPrint(tokenList, depth + 1)
        prettyPrint(tokenList, depth + 1)
        tokenList.pop(0)  # remove )
        print("%s)" % (' ' * depth,))


### very simple code that just checks whether the number of open parentheses
### is the same as the number of closed parentheses
def checkBalanced(tokenList):
    depth = 0
    while not tokenList == []:
        token = tokenList.pop(0)
        if token == '(':  # consume and add 1 to depth
            depth = depth + 1
        if token == ')':
            depth = depth - 1
    return depth == 0


### takes a string representing an expression in simple lisp and returns a list of tokens
def tokenize(programStr):
    tokens = programStr.replace('(', ' ( ').replace(')', ' ) ').split()
    if all(legalToken(token) for token in tokens):
        return [atom(token) for token in tokens]
    else:
        badTokens = str([token for token in tokens if not legalToken(token)])[1:][:-1]
        raise Exception("Unknown token found %s" % (badTokens,))


### returns True if the token is legal      
def legalToken(token):
    # returns True if legal for our simple lisp
    return token.isdigit() or token in Operators + [')', '(']


filename = input("Please enter the file you want the results printed out for: ")

file = open(filename, "r")

file2 = open("prettyPrintCorrect.txt", "w")
file3 = open("error.txt", "w")

n = 0

for line in file:
    try:  # try to parse the expression
        parseTree = parse(line)
        file2.write(str(n))
        file2.write("\n")
        file2.write(str(prettyPrint(tokenize(line))))
        file2.write("\n")
        file2.write(str(parseTree))
    except Exception as error:
        file3.write(str(n))
        file3.write("\n")
        file3.write(line)
        file3.write("\n")
        file3.write("Parse error: %s" % (error,))

    n += 1

