def evalProgram(codeList, trace=False):
    # top level code that takes a list of parsed statements
    global Trace
    Trace = trace
    return evalElBlock(codeList, {}, [])


def evalEl(code, bindings=[], depth=0):
    # evaluates code (parsed statement) with the bindings so far
    # bindings is a list of dictionaries, each with bindings
    # created from : a set statement, a def statement or a user function call
    if Trace or depth == 0:
        print("%sEval %s" % (" " * depth, toString(code)))
    answer = evalElHelp(code, bindings, depth)
    if Trace or depth == 0:
        print("%sAns  %s " % (" " * depth, toString(answer)))
    return answer


def evalElHelp(code, bindings, depth):
    # evaluates a single code statement with current bindings
    if isinstance(code, int):
        return code
    if "True" == code:
        return True
    if "False" == code:
        return False
    if "nil" == code:  # nil is the empty list
        return []
    if isinstance(code, str):  # variable
        return findValue(code, bindings, depth)
    # do all composite code
    fun = code[0]
    # numerical functions
    if fun == '+':
        return evalEl(code[1], bindings, depth + 1) + evalEl(code[2], bindings, depth + 1)
    if fun == '-':
        return evalEl(code[1], bindings, depth + 1) - evalEl(code[2], bindings, depth + 1)
    if fun == '*':
        return evalEl(code[1], bindings, depth + 1) * evalEl(code[2], bindings, depth + 1)
    if fun == '/':
        return evalEl(code[1], bindings, depth + 1) / evalEl(code[2], bindings, depth + 1)
    # control functions
    if fun == 'if':
        if evalEl(code[1], bindings, depth + 1):
            return evalEl(code[2], bindings, depth + 1)
        else:
            return evalEl(code[3], bindings, depth + 1)
    # boolean functions
    if fun == 'not':
        return not evalEl(code[1], bindings, depth + 1)
    if fun == 'and':
        return evalEl(code[1], bindings, depth + 1) and evalEl(code[2], bindings, depth + 1)
    if fun == 'or':
        return evalEl(code[1], bindings, depth + 1) or evalEl(code[2], bindings, depth + 1)
    if fun == 'eq':  # only works between atoms
        return simpleEqual(evalEl(code[1], bindings, depth + 1), evalEl(code[2], bindings, depth + 1))
    if fun == '<':
        return evalEl(code[1], bindings, depth + 1) < evalEl(code[2], bindings, depth + 1)
    if fun == 'atom':
        ans = evalEl(code[1], bindings, depth + 1)
        return isinstance(ans, int) or isinstance(ans, str) or ans == True or ans == False or ans == []
    # data structures
    if fun == 'cons':  # add the first to a list
        return [evalEl(code[1], bindings, depth + 1)] + evalEl(code[2], bindings, depth + 1)
    if fun == 'first':  # eval then return the first
        return evalEl(code[1], bindings, depth + 1)[0]
    if fun == 'rest':  # eval then return the rest
        return evalEl(code[1], bindings, depth + 1)[1:]
    if fun == 'quote':  # stop evaluation
        return code[1]
    if fun == 'evalEl':  # evaluate to get the code, then evaluate the code
        return evalEl(evalEl(code[1], bindings, depth + 1))

    # must be a user function call
    return evalElFun(code[0], code[1:], bindings, depth + 1)


def simpleEqual(a, b):
    # only works on primitives
    if isinstance(a, int) and isinstance(b, int):
        return a == b
    if (a is True and b is True) or (a is False and b is False):
        return True
    if (a == []) and (b == []):
        return True
    return False


def evalElFun(funName, args, bindings, depth):
    ############ COMPLETE THIS CODE
    # Execute a user defined function
    # HERE

    if Trace:
        print(" " * depth + "Calling function %s" % (funName,))

    # lookup the function parameters and block in bindings
    fBindings = None
    for dictionary in bindings:
        if funName in dictionary:
            fBindings = dictionary[funName]

    argNames = fBindings[0]
    block = [fBindings[1]]

    # create a new binding (dictionary) to hold local variables from parameters, sets and defs
    oneBinding = {}

    # add the mapping from parameter names to values
    i = 0

    for argName in argNames:
        oneBinding[argName] = evalEl(args[i], bindings, depth)
        i += 1

    # work through each statement in block
    # block will be from the function definition
    return evalElBlock(block, oneBinding, bindings, depth=depth + 1)


def evalElBlock(block, oneBinding, bindings, depth=0):
    # walks down the block evaluating each statement and accumulating bindings
    # into this oneBinding for this block
    if len(block) == 0:  # empty block, return None
        return
    else:
        code = block[0]

        if code[0] == 'set':
            # map the name of the variable to the eval of value
            # store the name to value mapping in oneBindings

            name = code[1]
            oneBinding[name] = evalEl(code[2], [oneBinding] + bindings, depth)

            # keep going through the block
            return evalElBlock(block[1:], oneBinding, bindings, depth=depth)
        elif code[0] == 'def':
            # put mapping from name to arguments, block

            name = code[1]
            oneBinding[name] = [code[2], code[3]]

            # keep working through block
            return evalElBlock(block[1:], oneBinding, [oneBinding] + bindings, depth=depth)
        else:  # found an expression, evaluate it with current bindings
            ans = evalEl(block[0], [oneBinding] + bindings, depth)
            # if last expression then return the answer
            if not block[1:]:
                return ans
            else:  # keep going through the block
                return evalElBlock(block[1:], oneBinding, bindings, depth=depth)


def findValue(name, bindings, depth):
    # name is a variable, bindings is a list of dictionaries ordered most
    # recent first, search up the bindings seeing if this variable is in
    # one of the dictionaries

    for dictionary in bindings:
        if name in dictionary:
            return dictionary[name]

    return None


def toString(code):
    # prints the parse tree in a more readable form
    if isinstance(code, int) or isinstance(code, str) or len(code) == 0:
        return str(code) + " "
    string = "("
    for item in code:
        string = string + toString(item)
    return string + ')'
