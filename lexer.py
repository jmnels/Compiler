import sys
#define keywords, special symbols and digit string
KEYWORDS = ['else', 'if', 'int', 'return', 'void', 'while']
SPEC_SYMBOLS = [  ',', ';', '{','}', '(', ')', '[', ']', '=']
DIGITS = '0123456789'
MULTOP = ['*', '/']
ADDOP = ['+', '-']
RELOP = ['<=', '>=', '==', '!=']
SPECOP = ['<', '>']
#######################################################################
#position class for future use in debugging

class Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, current_char):
        self.idx += 1
        self.col += 1

        if current_char == '\n':
            self.ln += 1
            self.col = 0

        return self

    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)

##########################################################################
#token types and token builder
    
TT_KEYWORD  = 'KEYWORD: '
TT_ID       = 'ID: '
TT_NUM	    = 'NUM: '
TT_SYMBOL   = ''
TT_ERROR    = 'ERROR: '

class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value
    
    def __repr__(self):
        if self.value: return "{0}{1}".format(self.type, self.value)
        return '{0}'.format(self.type)

###########################################################################
#the lexical analyzer

class Lexer:
    
    
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance()
    
    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

    def make_tokens(self):
        tokens = []
        
        while self.current_char != None:
            
            if self.current_char == ' ':
                self.advance()
            elif self.current_char.isalpha():
                tokens.append(self.make_ID())
            elif self.current_char.isdigit():
                tokens.append(self.make_num())
            elif self.current_char in MULTOP:
                tokens.append(Token('', self.current_char))
                self.advance()
            elif self.current_char in ADDOP:
                tokens.append(Token('', self.current_char))
                self.advance()
            elif self.current_char in SPECOP:
                tokens.append(Token('', self.current_char))
                self.advance()
            elif self.current_char in SPEC_SYMBOLS or self.current_char in RELOP:
                sym_str = ''

                while self.current_char != None and (self.current_char in SPEC_SYMBOLS or self.current_char in RELOP):
                    sym_str += self.current_char
                    self.advance()
                if sym_str in SPEC_SYMBOLS:
                    self.advance
                    tokens.append(Token(TT_SYMBOL, sym_str))
                elif sym_str in RELOP:
                    tokens.append(Token('', sym_str))
                    self.advance()
                else:
                    sym_list = list(sym_str)
                    for s in sym_list:
                        tokens.append(Token(TT_SYMBOL, s))
                    self.advance
            else:
                char_str = self.current_char
                self.advance()
                while self.current_char != None and self.current_char != ' ':
                    char_str += self.current_char
                    self.advance()
                if char_str == '!=':
                    tokens.append(Token(TT_SYMBOL, char_str))
                    self.advance()
                elif char_str[-1] == ';':
                    tokens.append(Token(TT_ERROR, char_str.split(";", 1)[0]))
                    tokens.append(Token(TT_SYMBOL, char_str[-1]))
                else:
                    tokens.append(Token(TT_ERROR, char_str))
                    self.advance()

        return tokens

    #function to create numerical types
    def make_num(self):
        num_str = ''
        
        while self.current_char != None and self.current_char.isdigit():
           
            num_str += self.current_char
            self.advance()
            if num_str == '0':
                num = '0'
            else:
                num = int(num_str) 
        return Token(TT_NUM, num)

    #function to determine if keyword or identifier
    def make_ID(self):
        id_str = ''

        while self.current_char != None and self.current_char.isalpha():
            id_str += self.current_char
            self.advance()
        if id_str in KEYWORDS:
            return Token(TT_KEYWORD, id_str)
        else:
            return Token(TT_ID, id_str)

       
##############################################################
#to make it go
        
def run(fn, text):
    lexer = Lexer(fn, text)
    tokens = lexer.make_tokens()

    return tokens

