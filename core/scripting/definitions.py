class ByteSize:
    INT = 8
    STRING = 4294967295
    OP_1_75 = 75
    OP_PUSHDATA1 = 255
    OP_PUSHDATA2 = 65535
    OP_PUSHDATA4 = 4294967295

class LanguageKeywords:
    #Constants
    OP_0 = "(OP_0|op_0)"
    OP_FALSE = "(OP_FALSE|op_false)"
    OP_1NEGATE = "(OP_1NEGATE|op_1negate)"
    OP_1 = "(OP_1|op_1)"
    OP_TRUE = "(OP_TRUE|op_true)"
    OP_2 = "(OP_2|op_2)"
    OP_3 = "(OP_3|op_3)"
    OP_4 = "(OP_4|op_4)"
    OP_5 = "(OP_5|op_5)"
    OP_6 = "(OP_6|op_6)"
    OP_7 = "(OP_7|op_7)"
    OP_8 = "(OP_8|op_8)"
    OP_9 = "(OP_9|op_9)"
    OP_10 = "(OP_10|op_10)"
    OP_11 = "(OP_11|op_11)"
    OP_12 = "(OP_12|op_12)"
    OP_13 = "(OP_13|op_13)"
    OP_14 = "(OP_14|op_14)"
    OP_15 = "(OP_15|op_15)"
    OP_16 = "(OP_16|op_16)"
    #Flow Control
    OP_VERIFY = "(OP_VERIFY|op_verify)"
    #Stack
    OP_DUP = "(OP_DUP|op_dup)"
    #Bitwise Logic
    OP_EQUALVERIFY = "(OP_EQUALVERIFY|op_equalverify)"
    #Arithmetic
    OP_ADD = "(OP_ADD|op_add)"
    OP_NUMEQUAL = "(OP_NUMEQUAL|op_numequal)"
    #Cryptography
    OP_HASH160 = "(OP_HASH160|op_hash160)"
    OP_CHECKSIG = "(OP_CHECKSIG|op_checksig)"


class LanguageSymbols:
    DECIMAL_DIGIT = "[0-9]"
    NON_ZERO_DECIMAL_DIGIT = "[1-9]"
    DECIMAL = "D"
    HEXADECIMAL_DIGIT = "([0-9]|([a-f]|[A-F]))"
    HEXADECIMAL = "H"
    NEGATIVE = "-"
    INT = "I"
    WHITE_SPACE = "\s"
    ASCII = "[\x00-\x7F]"
    WORD = "W"
    SLASH ="\\"
    DOUBLE_QUOTES = "\""
    STRING = "S" 

class TokenTypes:
    UNRECOGNIZED = -1
    #Constants
    OP_0 = 0
    OP_FALSE = 1
    DECIMAL_INT = 2
    HEXADECIMAL_INT = 3
    STRING = 4
    OP_1NEGATE = 5
    OP_1 = 7
    OP_TRUE = 8
    OP_2 = 9
    OP_3 = 10
    OP_4 = 11
    OP_5 = 12
    OP_6 = 13
    OP_7 = 14
    OP_8 = 15
    OP_9 = 16
    OP_10 = 17
    OP_11 = 18
    OP_12 = 19
    OP_13 = 20
    OP_14 = 21
    OP_15 = 22
    OP_16 = 23
    #Flow Control
    OP_VERIFY = 8
    #Stack
    OP_DUP = 11
    #Bitwise Logic
    OP_EQUALVERIFY = 5
    #Arithmetic
    OP_ADD = 8
    OP_NUMEQUAL = 17
    #Cryptography
    OP_HASH160 = 3
    OP_CHECKSIG = 6

class ParserErrorMssg:
    LEADING_ZEROES = "Decimal numbers cannot have leading zeroes"
    INT_CHARACTER = "Integers are made of numbers only"
    HEXA_START = "Hexadecimal numbers must have a leading 0x"
    NEGATIVE = "A negative symbol must be followed by 0X or a decimal digit"
    HEXADECIMAL = "0X must be followed by hexadecimal digits"
    NOT_ASCII = "The character is not ascii encoded"
    WORD_SEP = "You cannot use - as a separator"
    STRING_SCANNING = "EOL while scanning string literal"
    KEY_WORD = "You did not write a valid keyword"

class AssemblerErrorMssg:
    EMPTY_FILE = "The given file is empty"
    UNDEFINED_INSTR = "Undefined Instruction"
    LEADING_ZEROES = "Decimal numbers cannot have leading zeroes"
    HEXADECIMAL = "0x must be followeb by hexadecimal numbers"
    MAX_INT_BYTES = "The maximun number of bytes for an integer is 4"
    MAX_BYTES = "You cannot push more than 4294967296 bytes"
    COULD_NOT_ASSEMBLE = "Something went wrong and the file could not be assembled"

class BTCVMErrorMssg:
    COULD_NOT_PROCESS = "Something went wrong the binary could not be processed"
    NOT_ENOUGH_BYTES = "You are trying to push more bytes than the ones that are available"
    NOT_BTC = "The given binary was not of type btc"
    BINARY_OP = "needs that the stack has at least two elements"
    UNARY_OP = "needs that the stack has at least one element"
    FAILED_VERIFY = "failed verification"