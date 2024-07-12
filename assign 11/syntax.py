from os.path import join


def parseProgram(programString):
    # takes a string that represents a program, multiple statements
    # returns a list of list of tokens, each a statement
    tokens = programString.replace('(', ' ( ').replace(')', ' ) ').split()
    codeList = []
    while not tokens == []:
        code = createcode(tokens)
        codeList.append(code)
    return codeList


def createcode(tokenList):
    # takes a token list and returns a parse tree
    token = tokenList.pop(0)  # pop off ( or atom
    if token.isdigit() or token[0].isdigit():  # integer
        return int(token)
    if isinstance(token, str) and not token == '(':  # atom
        return token
    # operator = tokenList.pop(0) 
    # if operator.isdigit() or operator[0].isdigit(): #number
    #     operator = int(operator)
    args = []
    while not tokenList[0] == ')':
        args.append(createcode(tokenList))
    tokenList.pop(0)  # pop the ')'
    return args


def checkSyntax(code, grammarWord, grammar):
    # traverses the grammar tree and code tree
    # explores alternative rhs for each rule
    if isinstance(code, int):  # should be an int
        return grammarWord == '<number>'
    if isinstance(code, str):  # could be any non-int atom
        return (grammarWord == code) or grammarWord == '<string>'
    oneTrue = True  # only one rhs has to be true
    for oneRHS in grammar[grammarWord]:  # for all possible rhs
        if not len(code) == len(oneRHS):  # not the same length
            continue
        allTrue = True  # all of this rhs has to be correct
        for i in range(0, len(oneRHS)):  # try each word in the rhs
            allTrue = allTrue and checkSyntax(code[i], oneRHS[i], grammar)
        oneTrue = allTrue or oneTrue  # update for all rhs
        if oneTrue:  # found one that works
            return True
    return False


def readInGrammar(PATH):
    with open(join(PATH, 'eLgrammarDefinition.txt')) as file:  # Use file to refer to the file object
        return file.readlines()


def parseGrammar(PATH):
    grammar = {}
    for line in readInGrammar(PATH):
        if len(line) == 1 or line[0] == '#':
            continue
        rule = line.replace('(', ' ( ').replace(')', ' ) ').replace('|', ' | ').split()
        # map each lhs to a list of alternative rhs
        alternatives = generateAlternatives(rule[2:])
        # for rhs in alternatives:
        #     print("%s => %s" % (rule[0].ljust(20), rhs))
        grammar[rule[0]] = alternatives
    return grammar


def generateAlternatives(rhs, current=[]):
    # splits into alternative definitions
    if not rhs:  # done
        return [current]
    if rhs[0] == '|':  # finish this current alternative and start a new one
        return [current] + generateAlternatives(rhs[1:], [])
        # continue the current alternative
    return generateAlternatives(rhs[1:], current + [rhs[0]])
