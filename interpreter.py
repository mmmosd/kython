import sys
from enum import IntEnum

class Token(IntEnum):
    NONE = 0

    PLUS = 1
    MINUS = 2
    MULTI = 3
    DIVI = 4
    MOD = 5

    ASSIGNMENT = 6

    EQUAL = 7
    NOT_EQUAL = 8
    OVER = 9
    UNDER = 10
    OVER_OR_EQUAL = 11
    UNDER_OR_EQUAL = 12

    INPUT = 13
    PRINT = 14

    VAR = 15

    INT = 16
    FLOAT = 17
    STRING = 18

    IF = 19
    WHILE = 20

class Error(IntEnum):
    ERROR_SYNTAX = 0
    ERROR_SAME_VAR_NAME = 1
    ERROR_VAR_NOT_EXIST = 2

def get_token(word):
    if word == "더하기":
        return Token.PLUS
    if word == "빼기":
        return Token.MINUS
    if word == "곱하기":
        return Token.MULTI
    if word == "나누기":
        return Token.DIVI
    if word == "나머지":
        return Token.MOD
    
    if word == "은" or word == "는":
        return Token.ASSIGNMENT

    if word == "==":
        return Token.EQUAL
    if word == "!=":
        return Token.NOT_EQUAL
    if word == ">":
        return Token.OVER
    if word == "<":
        return Token.UNDER
    if word == ">=":
        return Token.OVER_OR_EQUAL
    if word == "<=":
        return Token.UNDER_OR_EQUAL

    if word == "입력":
        return Token.INPUT
    if word == "출력":
        return Token.PRINT
    
    if word == "변수":
        return Token.VAR
    
    if word == "정수":
        return Token.INT
    if word == "실수":
        return Token.FLOAT
    if word == "글자":
        return Token.STRING
    
    if word == "만약":
        return Token.IF
    if word == "반복":
        return Token.WHILE
    
    return Token.NONE

def error(Type):
    if Type == Error.ERROR_SYNTAX:
        sys.exit("문법이 맞지 않습니다. 에러코드: {}".format(Type))
    if Type == Error.ERROR_SAME_VAR_NAME:
        sys.exit("같은 변수 이름이 존재합니다. 에러코드: {}".format(Type))
    if Type == Error.ERROR_VAR_NOT_EXIST:
        sys.exit("존재하지 않는 변수입니다. 에러코드: {}".format(Type))

def data_declare_func(name, data, value):
    if name in data:
        error(Error.ERROR_SAME_VAR_NAME)

    data[name] = value

def data_access_func(name, data, value=None):
    if name not in data:
        error(Error.ERROR_VAR_NOT_EXIST)

    if value is None:
        return data[name]
    else:
        data[name] = value
        return data[name]

def get_data_type(name, data):
    if name not in data:
       error(Error.ERROR_VAR_NOT_EXIST)

    if type(data[name]) is int:
        return int
    elif type(data[name]) is float:
        return float
    elif type(data[name]) is str:
        return str

    return int

def get_string_data(line):
    result = []
    value = ""

    is_string = False
    for w in line:
        if w == 'ㅐ':
            if is_string:
                result.append(value)
                continue
            else:
                is_string = True
                value = ""
                continue

        if is_string:
            value += w

    return result
    
def get_formula_value(formula, data):
    result = 0

    if len(formula) == 1:
        return float(formula[0])
    elif len(formula) == 2:
        return data_access_func(formula[1], data)

    op = {Token.PLUS : 1, Token.MINUS : 1, Token.MULTI : 2, Token.DIVI : 2, Token.MOD : 2}

    stack = []
    prefix_f = []

    is_var = False
    for word in formula:
        token = get_token(word)

        if token == Token.VAR:
            is_var = True
            continue
        if is_var:
            prefix_f.append(data_access_func(word, data))
            is_var = False

        if word.isnumeric():
            prefix_f.append(float(word))
        elif token in op:
            if stack and (op[token] <= op[get_token(stack[-1])]):
                prefix_f.append(stack.pop())
            stack.append(word)
    while stack:
        prefix_f.append(stack.pop())

    stack = []
    for now in prefix_f:
        if type(now) is str:
            now = get_token(now)

            if now == Token.PLUS:
                a = stack.pop()
                b = stack.pop()
                result = b + a
                stack.append(result)
            if now == Token.MINUS:
                a = stack.pop()
                b = stack.pop()
                result = b - a
                stack.append(result)
            if now == Token.MULTI:
                a = stack.pop()
                b = stack.pop()
                result = b * a
                stack.append(result)
            if now == Token.DIVI:
                a = stack.pop()
                b = stack.pop()
                result = b / a
                stack.append(result)
            if now == Token.MOD:
                a = stack.pop()
                b = stack.pop()
                result = b % a
                stack.append(result)
        else:
            stack.append(now)
    
    return result

def logical_operation(A, B, operator):
    if operator == Token.EQUAL:
        return A == B
    if operator == Token.NOT_EQUAL:
        return A != B
    if operator == Token.OVER:
        return A > B
    if operator == Token.UNDER:
        return A < B
    if operator == Token.OVER_OR_EQUAL:
        return A >= B
    if operator == Token.UNDER_OR_EQUAL:
        return A <= B

def Get_Conditional_Statement_data(cs, data):
    A = []
    B = []
    operator = Token.NONE
    for w in cs[1:]:
        if get_token(w) == Token.EQUAL or get_token(w) == Token.NOT_EQUAL or get_token(w) == Token.OVER or get_token(w) == Token.UNDER or get_token(w) == Token.OVER_OR_EQUAL or get_token(w) == Token.UNDER_OR_EQUAL:
            operator = get_token(w)
            continue

        if operator == Token.NONE:
            A.append(w)
        else:
            B.append(w)
        
    if len(get_string_data(A[0])) > 0: #is string?
        A = get_string_data(A[0])[0]
    elif get_token(A[0]) == Token.VAR and len(A) == 2: #is var?
        A = data_access_func(A[1], data)
    else:
        A = get_formula_value(A, data)

    if len(get_string_data(B[0])) > 0: #is string?
        B = get_string_data(B[0])[0]
    elif get_token(B[0]) == Token.VAR and len(B) == 2: #is var?
        B = data_access_func(B[1], data)
    else:
        B = get_formula_value(B, data)

    return (A, B, operator)

def Code_Block_Run(code, cs, data):
    if len(cs) == 0:
        data = compile(code, data, line_num)
        return data
    elif get_token(cs[0]) == Token.IF:
        A, B, operator = Get_Conditional_Statement_data(cs, data)

        if logical_operation(A, B, operator):
            data = compile(code, data, line_num)
        
        return data
    elif get_token(cs[0]) == Token.WHILE:
        A, B, operator = Get_Conditional_Statement_data(cs, data)

        while logical_operation(A, B, operator):
            data = compile(code, data, line_num)
            A, B, operator = Get_Conditional_Statement_data(cs, data)

        return data

def translate_line(line, data):
    if (line == ""): return 0
    if (line[0] == "ㄱ") or (line[0] == "ㄴ"): return 0

    words = line.split(" ")
    tokens = []

    for w in words:
        if (w == "ㅣ"): break
        token = get_token(w)
        tokens.append(token)

    if tokens[0] == Token.NONE:
        error(Error.ERROR_SYNTAX)

    #선언: 변수 이름 타입 (계산식)
    if tokens[0] == Token.VAR:
        name = words[1]
        if tokens[2] == Token.INT:
            if len(tokens) > 3:
                value = int(get_formula_value(words[3:], data))
            else:
                value = 0

            data_declare_func(name, data, value)
            return 0
        elif tokens[2] == Token.FLOAT:
            if len(tokens) > 3:
                value = float(get_formula_value(words[3:], data))
            else:
                value = 0.0
            
            data_declare_func(name, data, value)
            return 0
        elif tokens[2] == Token.STRING:
            if len(tokens) > 3:
                value = get_string_data(line)[0]
            else:
                value = ""
            
            data_declare_func(name, data, value)
            return 0

    #입력: 입력 변수 이름
    if tokens[0] == Token.INPUT:
        if tokens[1] == Token.VAR:
            name = words[2]
            var_type = get_data_type(name, data)
            data_access_func(name, data, var_type(input()))
            return 0

    #출력: 출력 (변수 or 내용)
    if tokens[0] == Token.PRINT:
        if tokens[1] == Token.VAR:
            name = words[2]
            value = data_access_func(name, data)
            if len(words) >= 4 and words[3] == "ㄴ>":
                print(value)
            else:
                print(value, end='')

            return 0
        else:
            value = get_string_data(line)[0]

            if len(words) >= 3 and words[2] == "ㄴ>":
                print(value)
            else:
                print(value, end='')

            return 0

    #연산:변수 이름 는/은 (계산식)
    if tokens[0] == Token.VAR:
        name = words[1]
        if tokens[2] == Token.ASSIGNMENT:
            var_type = get_data_type(name, data)
            data_access_func(name, data, var_type(get_formula_value(words[3:], data)))
            return 0

def compile(code, data={}, line=1):
    global line_num
    line_num = line
    is_in_block = False
    code_block = []
    block_stack = 0
    Conditional_Statement = []
    before_data = data.copy()

    for line in code:
        line = line.strip()

        if is_in_block:
            code_block.append(line)
        else:
            translate_line(line, data)
            
            words = line.split(" ")
            if get_token(words[0]) == Token.IF or get_token(words[0]) == Token.WHILE:
                Conditional_Statement = words

        if len(line) == 1:
            if line[0] == 'ㄱ':
                is_in_block = True
                block_stack += 1
            elif line[0] == 'ㄴ':
                block_stack -= 1

                if block_stack == 0:
                    code_block.pop()
                    data = Code_Block_Run(code_block, Conditional_Statement, data)

                    is_in_block = False
                    code_block = []
                    Conditional_Statement = []

        line_num += 1

    for k in before_data.keys():
        before_data[k] = data[k]

    return before_data.copy()

def run():
    global line_num
    line_num = 1
    data = {}
    is_in_block = False
    code_block = []
    block_stack = 0
    Conditional_Statement = []

    while (1):
        line = input(">>>")
        line.strip()

        if is_in_block:
            code_block.append(line)
        else:
            translate_line(line, data)
            
            words = line.split(" ")
            if get_token(words[0]) == Token.IF or get_token(words[0]) == Token.WHILE:
                Conditional_Statement = words

        if len(line) == 1:
            if line[0] == 'ㄱ':
                is_in_block = True
                block_stack += 1
            elif line[0] == 'ㄴ':
                block_stack -= 1

                if block_stack == 0:
                    code_block.pop()
                    data = Code_Block_Run(code_block, Conditional_Statement, data)

                    is_in_block = False
                    code_block = []
                    Conditional_Statement = []

        line_num += 1