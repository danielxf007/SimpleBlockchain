import re

from core.scripting.definitions import ByteSize, Language, AssemblerErrorMssg

class Assembler:
    
    def is_op_0(self, string):
        return Language.OP_0 == string 
    
    def is_op_false(self, string):
        return Language.OP_FALSE == string
    
    def encode_push_0(self):
        op_code = (0x00).to_bytes(length=1, byteorder='little', signed=False)
        return op_code
    
    def is_decimal_integer(self, string):
        if re.fullmatch(Language.DECIMAL_LEADING_ZEROES, string):
            raise Exception(f"{AssemblerErrorMssg.LEADING_ZEROES}: {string}")
        return bool(re.fullmatch(Language.DECIMAL_INTEGER, string))

    def is_hexadecimal_integer(self, string):
        return bool(re.fullmatch(Language.HEXADECIMAL_INTEGER, string))
    
    def encode_push_integer(self, string, base_number):
        number = int(string, base=base_number)
        n_bytes = (number.bit_length() + 7) // 8
        if n_bytes <= ByteSize.INT:
            byte_arr = number.to_bytes(length=ByteSize.INT, byteorder='little',signed=True)
            op_code = (ByteSize.INT).to_bytes(length=1, byteorder='little', signed=False)
            op_code += byte_arr
        else:
            raise Exception(f"{AssemblerErrorMssg.MAX_INT_BYTES}: {string}")
        return op_code
    
    def is_string(self, string):
        return bool(re.fullmatch(Language.STRING, string))
    
    def encode_push_string(self, string):
        byte_arr = bytes(string, "ascii")
        n_bytes = len(byte_arr)
        if n_bytes <= ByteSize.STRING:
            if n_bytes <= ByteSize.OP_1_75:
                op_code = n_bytes.to_bytes(length=1, byteorder='little', signed=False)
            elif n_bytes <= ByteSize.OP_PUSHDATA1:
                op_code = (0x4c).to_bytes(length=1, byteorder='little', signed=False)
                op_code += (n_bytes).to_bytes(length=1, byteorder='little', signed=False)
            elif n_bytes <= ByteSize.OP_PUSHDATA2:
                op_code = (0x4d).to_bytes(length=1, byteorder='little', signed=False)
                op_code += (n_bytes).to_bytes(length=2, byteorder='little', signed=False)
            elif n_bytes <= ByteSize.OP_PUSHDATA4:
                op_code = (0x4d).to_bytes(length=1, byteorder='little', signed=False)
                op_code += (n_bytes).to_bytes(length=4, byteorder='little', signed=False)
            op_code += byte_arr
        else:
            raise Exception(AssemblerErrorMssg.MAX_BYTES)
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
    
    def is_op_dup(self, string):
        return Language.OP_DUP == string
    
    def encode_dup(self):
        op_code = (0x76).to_bytes(length=1, byteorder='little', signed=False)
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
            elif self.is_decimal_integer(string):
                encoded_instr = self.encode_push_integer(string, 10)
            elif self.is_hexadecimal_integer(string):
                encoded_instr = self.encode_push_integer(string, 16)
            elif self.is_string(string):
                encoded_instr = self.encode_push_string(string)
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
                raise Exception(f"{AssemblerErrorMssg.UNDEFINED_INSTR}: {string}")
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
        result = {"success": True, "err": "", "binary": bytes()}
        try:
            binary = bytes("BTC".encode())
            binary += self.parse(source_file_content)
            result["binary"] = binary
        except Exception as e:
            result["success"] = False
            result["err"] = f"{AssemblerErrorMssg.COULD_NOT_ASSEMBLE}: {e}"
        return result
        


