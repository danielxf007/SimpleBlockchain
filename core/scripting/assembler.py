from core.scripting.definitions import AssemblerErrorMssg, TokenTypes, ByteSize
from core.scripting.parser import Parser

class Assembler:
    
    def __init__(self):
        self.parser = Parser()
        self.func_dict = {
        "constant": [None for _ in range(24)], "flow_control": [None for _ in range(10)],
        "stack": [None for _ in range(19)], "data_manipulation": [],
        "bitwise_logic":[None for _ in range(6)], "arithmetic": [None for _ in range(27)],
        "cryptography": [None for _ in range(10)]}
        self.init_func_dict()
    
    def init_func_dict(self):
        self.func_dict["constant"][TokenTypes.OP_0] = self.encode_push_empty
        self.func_dict["constant"][TokenTypes.OP_FALSE] = self.encode_push_empty
        self.func_dict["constant"][TokenTypes.DECIMAL_INT] = self.get_encode_int(
            TokenTypes.DECIMAL_INT)
        self.func_dict["constant"][TokenTypes.HEXADECIMAL_INT] = self.get_encode_int(
            TokenTypes.HEXADECIMAL_INT)
        self.func_dict["constant"][TokenTypes.STRING] = self.encode_string
        self.func_dict["constant"][TokenTypes.OP_1NEGATE] = self.encode_push_1_negate
        self.func_dict["constant"][TokenTypes.OP_1] = self.encode_push_1
        self.func_dict["constant"][TokenTypes.OP_TRUE] = self.encode_push_1
        for token_type in range(TokenTypes.OP_2, TokenTypes.OP_16+1):
            offset = token_type-TokenTypes.OP_2
            self.func_dict["constant"][token_type] = self.get_enconde_push_2_to_16(offset)
        self.func_dict["flow_control"][TokenTypes.OP_VERIFY] = self.encode_verify
        self.func_dict["stack"][TokenTypes.OP_DUP] = self.encode_dup
        self.func_dict["bitwise_logic"][TokenTypes.OP_EQUALVERIFY] = self.encode_equalverify
        self.func_dict["arithmetic"][TokenTypes.OP_ADD] = self.encode_add
        self.func_dict["arithmetic"][TokenTypes.OP_NUMEQUAL] = self.encode_numequal
        self.func_dict["cryptography"][TokenTypes.OP_HASH160] = self.encode_has160
        self.func_dict["cryptography"][TokenTypes.OP_CHECKSIG] = self.encode_checksig

    def encode_push_empty(self, string):
        op_code = (0x00).to_bytes(length=1, byteorder='little', signed=False)
        return op_code
    
    def get_encode_int(self, token_type):
        if token_type == TokenTypes.DECIMAL_INT:
            base_num = 10
        else:
            base_num = 16
        def encode_push_int(string):
            number = int(string, base=base_num)
            n_bytes = (number.bit_length() + 7) // 8
            if n_bytes <= ByteSize.INT:
                byte_arr = number.to_bytes(length=ByteSize.INT, byteorder='little',signed=True)
                op_code = (ByteSize.INT).to_bytes(length=1, byteorder='little', signed=False)
                op_code += byte_arr
            else:
                raise Exception(f"{AssemblerErrorMssg.MAX_INT_BYTES}: {string}")
            return op_code
        return encode_push_int
    
    def encode_string(self, string):
        n_bytes = len(string)
        if n_bytes <= ByteSize.OP_1_75:
            op_code = (n_bytes).to_bytes(length=1, byteorder='little', signed=False)
        elif n_bytes <= ByteSize.OP_PUSHDATA1:
            op_code = (0x4c).to_bytes(length=1, byteorder='little', signed=False)
            op_code += (n_bytes).to_bytes(length=1, byteorder='little', signed=False)
        elif n_bytes <= ByteSize.OP_PUSHDATA2:
            op_code = (0x4d).to_bytes(length=1, byteorder='little', signed=False)
            op_code += (n_bytes).to_bytes(length=2, byteorder='little', signed=False)
        elif n_bytes <= ByteSize.OP_PUSHDATA4:
            op_code = (0x4e).to_bytes(length=1, byteorder='little', signed=False)
            op_code += (n_bytes).to_bytes(length=4, byteorder='little', signed=False)
        else:
            raise Exception(AssemblerErrorMssg.MAX_BYTES)
        byte_arr = bytes(string, "ascii")
        op_code += byte_arr
        return op_code

    def encode_push_1_negate(self, string):
        op_code = (0x4f).to_bytes(length=1, byteorder='little', signed=False)
        return op_code

    def encode_push_1(self, string):
        op_code = (0x51).to_bytes(length=1, byteorder='little', signed=False)
        return op_code

    def get_enconde_push_2_to_16(self, offset):
        def encode_push_2_to_16(string):
            op_code = (0x52 + offset).to_bytes(length=1, byteorder='little', signed=False)
            return op_code
        return encode_push_2_to_16
    
    def encode_verify(self):
        op_code = (0x69).to_bytes(length=1, byteorder='little', signed=False)
        return op_code
    
    def encode_dup(self):
        op_code = (0x76).to_bytes(length=1, byteorder='little', signed=False)
        return op_code
    
    def encode_equalverify(self):
        op_code = (0x88).to_bytes(length=1, byteorder='little', signed=False)
        return op_code

    def encode_add(self):
        op_code = (0x93).to_bytes(length=1, byteorder='little', signed=False)
        return op_code
    
    def encode_numequal(self):
        op_code = (0x9c).to_bytes(length=1, byteorder='little', signed=False)
        return op_code
    
    def encode_has160(self):
        op_code = (0xa9).to_bytes(length=1, byteorder='little', signed=False)
        return op_code
    
    def encode_checksig(self):
        op_code = (0xac).to_bytes(length=1, byteorder='little', signed=False)
        return op_code        


    def assemble(self, source_file_content):
        """Gets the content of the source file, gets it parsed and returns a dictionary with
        a flag indicating whether an error happened or not, an error message and a binary
        with the encoded operations.

        This method is not responsible for getting the source file content.

        The byte array is little endian.

        Keyword arguments:
        source_file_content -- it is the content of an assembly file which was opened
        with flag r
        """
        result = {"success": True, "err": "", "binary": bytes()}
        try:
            binary = bytes("BTC", "ascii")
            tokens = self.parser.parse(source_file_content)
            for token in tokens:
                if token["category"] == "constant":
                    op_code = self.func_dict["constant"][token["type"]](token["string"])
                else:
                    op_code = self.func_dict[token["category"]][token["type"]]()
                binary += op_code
            result["binary"] = binary
        except Exception as e:
            result["success"] = False
            result["err"] = f"{AssemblerErrorMssg.COULD_NOT_ASSEMBLE}: {e}"
        return result