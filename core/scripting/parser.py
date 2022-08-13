from lib2to3.pgen2 import token
import re
from core.scripting.definitions import LanguageKeywords, LanguageSymbols, TokenTypes, ParserErrorMssg

class PushDownAutomata:

    def __init__(self):
        self.stack = []
    
    def push(self, symbol):
        self.stack.append(symbol)

    def empty(self):
        return len(self.stack) == 0
       
    def pop(self):
        if self.empty():
            return None
        return self.stack.pop()
    
    def get_top_symbol(self):
        if self.empty():
            return None
        return self.stack[len(self.stack)-1]
    
    def reset(self):
        self.stack.clear()

class Parser:
    def __init__(self):
        self.automata = PushDownAutomata()
        self.aux_automata = PushDownAutomata() # Holds special symbols

    def is_decimal_digit(self, symbol):
        return re.match(LanguageSymbols.DECIMAL_DIGIT, symbol)
    
    def is_non_zero_decimal_digit(self, symbol):
        return re.match(LanguageSymbols.NON_ZERO_DECIMAL_DIGIT, symbol)
    
    def is_hexadecimal_digit(self, symbol):
        return re.match(LanguageSymbols.HEXADECIMAL_DIGIT, symbol)
    
    def is_decimal(self, symbol):
        return LanguageSymbols.DECIMAL == symbol
    
    def is_hexadecimal(self, symbol):
        return LanguageSymbols.HEXADECIMAL == symbol
    
    def is_negative(self, symbol):
        return LanguageSymbols.NEGATIVE == symbol
    
    def is_int(self, symbol):
        return LanguageSymbols.INT == symbol

    def is_white_space(self, symbol):
        return re.match(LanguageSymbols.WHITE_SPACE, symbol)
    
    def is_double_quotes(self, symbol):
        return LanguageSymbols.DOUBLE_QUOTES == symbol
    
    def is_ascii(self, symbol):
        return re.match(LanguageSymbols.ASCII, symbol)
    
    def is_string(self, symbol):
        return LanguageSymbols.STRING == symbol
    
    def is_word(self, symbol):
        return LanguageSymbols.WORD == symbol
    
    def get_decimal_int_token(self):
        token = {"string": "", "type": TokenTypes.DECIMAL_INT}
        while not self.automata.empty():
            token["string"] = self.automata.pop() + token["string"]
        self.aux_automata.pop()
        if self.is_negative(self.aux_automata.get_top_symbol()):
            token["string"] = "-" + token["string"]
            self.aux_automata.pop()
        
        self.aux_automata.pop()
        return token

    def get_hexadecimal_int_token(self):
        token = {"string": "", "type": TokenTypes.HEXADECIMAL_INT}
        while not self.automata.empty():
            token["string"] = self.automata.pop() + token["string"]
        token["string"] = "0x" + token["string"]
        self.aux_automata.pop()
        if self.is_negative(self.aux_automata.get_top_symbol()):
            token["string"] = "-" + token["string"]
            self.aux_automata.pop()
        self.aux_automata.pop()
        return token

    def get_string_token(self):
        token = {"string": "", "type": TokenTypes.STRING}
        while not self.automata.empty():
            token["string"] = self.automata.pop() + token["string"]
        self.aux_automata.pop()
        return token
    
    def get_keyword_type(self, string):
        keyword_type = TokenTypes.UNRECOGNIZED
        if re.match(LanguageKeywords.OP_0, string):
            keyword_type = TokenTypes.OP_0
        elif re.match(LanguageKeywords.OP_FALSE, string):
            keyword_type = TokenTypes.OP_FALSE
        elif re.match(LanguageKeywords.OP_1NEGATE, string):
            keyword_type = TokenTypes.OP_1NEGATE
        elif re.match(LanguageKeywords.OP_1, string):
            keyword_type = TokenTypes.OP_1
        elif re.match(LanguageKeywords.OP_TRUE, string):
            keyword_type = TokenTypes.OP_TRUE
        elif re.match(LanguageKeywords.OP_2, string):
            keyword_type = TokenTypes.OP_2
        elif re.match(LanguageKeywords.OP_3, string):
            keyword_type = TokenTypes.OP_3
        elif re.match(LanguageKeywords.OP_4, string):
            keyword_type = TokenTypes.OP_4
        elif re.match(LanguageKeywords.OP_5, string):
            keyword_type = TokenTypes.OP_5
        elif re.match(LanguageKeywords.OP_6, string):
            keyword_type = TokenTypes.OP_6
        elif re.match(LanguageKeywords.OP_7, string):
            keyword_type = TokenTypes.OP_7
        elif re.match(LanguageKeywords.OP_8, string):
            keyword_type = TokenTypes.OP_8
        elif re.match(LanguageKeywords.OP_9, string):
            keyword_type = TokenTypes.OP_9
        elif re.match(LanguageKeywords.OP_10, string):
            keyword_type = TokenTypes.OP_10
        elif re.match(LanguageKeywords.OP_11, string):
            keyword_type = TokenTypes.OP_11
        elif re.match(LanguageKeywords.OP_12, string):
            keyword_type = TokenTypes.OP_12
        elif re.match(LanguageKeywords.OP_13, string):
            keyword_type = TokenTypes.OP_13
        elif re.match(LanguageKeywords.OP_14, string):
            keyword_type = TokenTypes.OP_14
        elif re.match(LanguageKeywords.OP_15, string):
            keyword_type = TokenTypes.OP_15
        elif re.match(LanguageKeywords.OP_16, string):
            keyword_type = TokenTypes.OP_16
        return keyword_type

    def get_word_token(self):
        token = {"string": "", "type": TokenTypes.UNRECOGNIZED}
        while not self.automata.empty():
            token["string"] = self.automata.pop() + token["string"]
        token["type"] = self.get_keyword_type(token["string"])
        if token["type"] == TokenTypes.UNRECOGNIZED:
            raise Exception(ParserErrorMssg.KEY_WORD)
        self.aux_automata.pop()
        return token

    def parse(self, symbol_arr):
        self.automata.reset()
        self.aux_automata.reset()
        symbol_arr_copy = symbol_arr + " "
        n_tokens = 0
        tokens = []
        i = 0
        for i in range(len(symbol_arr_copy)):
            symbol = symbol_arr_copy[i]
            print(f"Symbol: {symbol}")
            print(f"Before Automata: {self.automata.stack}")
            print(f"Before Aux Automata: {self.aux_automata.stack}")
            top_symbol = self.automata.get_top_symbol()
            aux_top_symbol = self.aux_automata.get_top_symbol()
            if not self.is_ascii(symbol):
                raise Exception(ParserErrorMssg.NOT_ASCII)
            if self.automata.empty() and self.aux_automata.empty():
                if self.is_negative(symbol):
                    self.aux_automata.push(LanguageSymbols.INT)
                    self.aux_automata.push(LanguageSymbols.NEGATIVE)
                elif self.is_non_zero_decimal_digit(symbol):
                    self.automata.push(symbol)
                    self.aux_automata.push(LanguageSymbols.INT)
                    self.aux_automata.push(LanguageSymbols.DECIMAL)
                elif self.is_decimal_digit(symbol):
                    self.automata.push(symbol)
                    self.aux_automata.push(LanguageSymbols.INT)
                elif self.is_double_quotes(symbol):
                    self.aux_automata.push(LanguageSymbols.STRING)
                elif self.is_white_space(symbol):
                    continue
                else:
                    self.automata.push(symbol)
                    self.aux_automata.push(LanguageSymbols.WORD)
            elif self.automata.empty() and not self.aux_automata.empty():
                if self.is_negative(aux_top_symbol):
                    if symbol == '0':
                        self.automata.push(symbol)
                    elif self.is_non_zero_decimal_digit(symbol):
                        self.automata.push(symbol)
                        self.aux_automata.push(LanguageSymbols.DECIMAL)
                    else:
                        raise Exception(ParserErrorMssg.NEGATIVE)
                elif self.is_hexadecimal(aux_top_symbol):
                    if self.is_hexadecimal_digit(symbol):
                        self.automata.push(symbol)
                    else:
                        raise Exception(ParserErrorMssg.HEXADECIMAL)
                elif self.is_string(aux_top_symbol):
                    if self.is_double_quotes(symbol):
                        tokens.append(self.get_string_token())
                    else:
                        self.automata.push(symbol)
            elif not self.automata.empty() and not self.aux_automata.empty():
                if self.is_negative(aux_top_symbol) or self.is_int(aux_top_symbol):
                    if top_symbol == '0':
                        if self.is_white_space(symbol):
                            tokens.append(self.get_decimal_int_token())
                        elif symbol.lower() == 'x':
                            self.automata.pop()
                            self.aux_automata.push(LanguageSymbols.HEXADECIMAL)
                        elif self.is_decimal_digit(symbol):
                            raise Exception(ParserErrorMssg.LEADING_ZEROES)
                        else:
                            raise Exception(ParserErrorMssg.INT_CHARACTER)
                    elif self.is_decimal_digit(symbol):
                        self.automata.push(symbol)
                        self.aux_automata.push(LanguageSymbols.DECIMAL)
                    else:
                        raise Exception(ParserErrorMssg.INT_CHARACTER)
                elif self.is_decimal(aux_top_symbol):
                    if self.is_white_space(symbol):
                        tokens.append(self.get_decimal_int_token())
                    elif self.is_decimal_digit(symbol):
                        self.automata.push(symbol)
                    else:
                        raise Exception(ParserErrorMssg.INT_CHARACTER)
                elif self.is_hexadecimal(aux_top_symbol):
                    if self.is_white_space(symbol):
                        tokens.append(self.get_hexadecimal_int_token())
                    elif self.is_hexadecimal_digit(symbol):
                        self.automata.push(symbol)
                    else:
                        raise Exception(ParserErrorMssg.INT_CHARACTER)
                elif self.is_string(aux_top_symbol):
                    if self.is_double_quotes(symbol):
                        tokens.append(self.get_string_token())
                    else:
                        self.automata.push(symbol)
                elif self.is_word(aux_top_symbol):
                    if self.is_white_space(symbol):
                        tokens.append(self.get_word_token())
                    else:
                        self.automata.push(symbol)
            print(f"After Automata: {self.automata.stack}")
            print(f"After Aux Automata: {self.aux_automata.stack}")
            if len(tokens) != n_tokens:
                n_tokens = len(tokens)
                print(f"Tokens {tokens}")
        print(tokens)
        return tokens

