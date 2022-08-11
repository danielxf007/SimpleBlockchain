class ByteSize:
    INT = 4
    STRING = 4294967296
    OP_1_75 = 75
    OP_PUSHDATA1 = 255
    OP_PUSHDATA2 = 65535
    OP_PUSHDATA4 = 4294967295

class Language:
    #Constants
    OP_0 = "OP_0"
    OP_FALSE = "OP_FALSE"
    DECIMAL_LEADING_ZEROES = "^0[0-9]+|-0[0-9]+"
    DECIMAL_INTEGER = "-?([0-9]|[1-9][0-9]*)"
    HEXADECIMAL_INTEGER = "-?(0X([0-9]|[A-F])+)"
    STRING = "\"[\x00-\x7F]*\""
    OP_1NEGATE = "OP_1NEGATE"
    OP_1 = "OP_1"
    OP_TRUE = "OP_TRUE"
    OP_2_TO_16 = "OP_([2-9]|1[0-6])"
    #Stack
    OP_DUP = "OP_DUP"
    #Arithmetic
    OP_ADD = "OP_ADD"
    OP_NUMEQUAL = "OP_NUMEQUAL"

class AssemblerErrorMssg:
    EMPTY_FILE = "The given file is empty"
    UNDEFINED_INSTR = "Undefined Instruction"
    LEADING_ZEROES = "Decimal numbers cannot have leading zeroes"
    HEXADECIMAL = "0x must be followeb by hexadecimal numbers"
    MAX_INT_BYTES = "The maximun number of bytes for an integer is 4"
    MAX_BYTES = "You cannot push more than 4294967296"
    COULD_NOT_ASSEMBLE = "Something went wrong and the file could not be assembled"

class BTCVMErrorMssg:
    COULD_NOT_PROCESS = "Something went wrong the binary could not be processed"
    NOT_ENOUGH_BYTES = "You are trying to push more bytes than the ones that are available"
    NOT_BTC = "The given binary was not of type btc"
    BINARY_OP = "Binay operations need that the stack has at least two elements"