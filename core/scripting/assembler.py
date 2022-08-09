import re

class ByteLimits:
    U_INT = 8

class Language:
    OP_0 = "OP_0"
    OP_FALSE = "OP_FALSE"
    DECIMAL_LEADING_ZEROES = "^0[0-9]+"
    DECIMAL = "[0-9]|[1-9][0-9]*"
    HEXADECIMAL = "0X([0-9]|[A-F])+"
    OP_1NEGATE = "OP_1NEGATE"
    OP_1 = "OP_1"
    OP_TRUE = "OP_TRUE"
    OP_2_TO_16 = "OP_([2-9]|1[0-6])"
    OP_ADD = "OP_ADD"
    OP_NUMEQUAL = "OP_NUMEQUAL"

class ErrorMssg:
    EMPTY_FILE = "The given file is empty"
    UNDEFINED_INSTR = "Undefined Instruction"
    LEADING_ZEROES = "Decimal numbers cannot have leading zeroes"
    HEXADECIMAL = "0x must be followeb by hexadecimal numbers"
    MAX_INT_BYTES = "The maximun number of bytes for an integer is 8"
    COULD_NOT_ASSEMBLE = "Something went wrong and the file could not be assembled"

class Assembler:
    
    def is_op_0(self, string):
        return Language.OP_0 == string 
    
    def is_op_false(self, string):
        return Language.OP_FALSE == string
    
    def encode_push_0(self):
        op_code = (0x00).to_bytes(length=1, byteorder='little', signed=False)
        return op_code

    def is_decimal_constant(self, string):
        if re.fullmatch(Language.DECIMAL_LEADING_ZEROES, string):
            raise Exception(f"{ErrorMssg.LEADING_ZEROES}: {string}")
        return bool(re.fullmatch(Language.DECIMAL, string))

    def is_hexadecimal_constant(self, string):
        return bool(re.fullmatch(Language.HEXADECIMAL, string))
    
    def encode_push_u_int_constant(self, string, base_number):
        number = int(string, base=base_number)
        n_bytes = (number.bit_length() + 7) // 8
        if n_bytes <= ByteLimits.U_INT:
            byte_arr = number.to_bytes(length=n_bytes, byteorder='little',signed=False)
            op_code = n_bytes.to_bytes(length=1, byteorder='little', signed=False)
            op_code += byte_arr
        else:
            raise Exception(f"{ErrorMssg.MAX_INT_BYTES}: {string}")
        return op_code  
    
    def is_op1_negate(self, string):
        return Language.OP_1NEGATE == string
    
    def encode_push_1_negate(self):
        op_code = (0x4f).to_bytes(length=1, byteorder='little', signed=False)
        return op_code

    def is_op_1(self, string):
        return Language.OP_1 == string

    def encode_push_1(self):
        op_code = (0x51).to_bytes(length=1, byteorder='little', signed=False)
        return op_code
    
    def is_op_true(self, string):
        return Language.OP_TRUE == string
    
    def is_op_2_to_16(self, string):
        return bool(re.fullmatch(Language.OP_2_TO_16, string))
    
    def enconde_push_2_to_16(self, string):
        offset = int(string.split("_")[1]) - 2
        op_code = (0x52 + offset).to_bytes(length=1, byteorder='little', signed=False)
        return op_code
    
    def is_op_add(self, string):
        return Language.OP_ADD == string
    
    def encode_add(self):
        op_code = (0x93).to_bytes(length=1, byteorder='little', signed=False)
        return op_code

    def is_op_numequal(self, string):
        return Language.OP_NUMEQUAL == string
    
    def encode_numequal(self):
        op_code = (0x9C).to_bytes(length=1, byteorder='little', signed=False)
        return op_code

    def parse(self, source_file_content):
        """Returns a byte array with the encoded instructions found on the source file.

        White spaces are stripped.

        The content is transformed to upper case.

        This method is not responsible for opening nor closing the source file.

        The byte array is little endian.

        If the source file does not follow the sintax and uses disabled op codes,
        then an exception is raised

        Keyword arguments:
        source_file_content -- it is the content of an assembly file
        which was opened with flag r
        """
        encoded_instrs = bytes()
        strings = source_file_content.upper()
        strings = strings.split()
        for string in strings:
            if self.is_op_0(string):
                encoded_instr = self.encode_push_0()
            elif self.is_op_false(string):
                encoded_instr = self.encode_push_0()
            elif self.is_decimal_constant(string):
                encoded_instr = self.encode_push_u_int_constant(string, 10)
            elif self.is_hexadecimal_constant(string):
                encoded_instr = self.encode_push_u_int_constant(string, 16)
            elif self.is_op1_negate(string):
                encoded_instr = self.encode_push_1_negate()
            elif self.is_op_1(string):
                encoded_instr = self.encode_push_1()
            elif self.is_op_true(string):
                encoded_instr = self.encode_push_1()
            elif self.is_op_2_to_16(string):
                encoded_instr = self.enconde_push_2_to_16(string)
            elif self.is_op_add(string):
                encoded_instr = self.encode_add()
            elif self.is_op_numequal(string):
                encoded_instr = self.encode_numequal()
            else:
                raise Exception(f"{ErrorMssg.UNDEFINED_INSTR}: {string}")
            encoded_instrs += encoded_instr
        return encoded_instrs
    
    def assemble(self, source_file_content):
        """Parses the source file and  returns a dictionary with
        information about the method's execution.

        This method is not responsible for opening nor closing the source file.
        This method is not responsible for opening nor closing the target file.

        If there is an exception during parsing, then a dictionary with a failure flag and
        a message of what happened is returned.

        The byte array is little endian.

        Keyword arguments:
        source_file_content -- it is the content of an assembly file which was opened
        with flag r
        """
        result = {"success": True, "err": "", "encoded_file_content": bytes()}
        try:
            encoded_file_content = bytes("BTC".encode())
            encoded_file_content += self.parse(source_file_content)
            result["encoded_file_content"] = encoded_file_content
        except Exception as e:
            result["success"] = False
            result["err"] = f"{ErrorMssg.COULD_NOT_ASSEMBLE}: {e}"
        return result
        


