from core.scripting.definitions import ByteSize,BTCVMErrorMssg
    

class BTCVM:
    """ This class represents a stack based virtual machine that
    is able to execute functions according to the data in tokens
    created by a BTC Tokenizer.

    The name for the functions and how they work can be seem on:
    https://wiki.bitcoinsv.io/index.php/Opcodes_used_in_Bitcoin_Script
    """
    
    def __init__(self):
        self.binary_type = bytes("BTC".encode())
        self.MAX_OP_CODES = 256
        self.function_vector = []
        self.stack = []
        self.program_rom = bytes()
        self.pc = 0 #Program counter
        self.init_function_vector()
    
    def init_function_vector(self):
        self.function_vector = [None for _ in range(self.MAX_OP_CODES)]
        self.function_vector[0x00] = self.push_empty_byte_arr
        for i in range(0x01, 0x4c):
            self.function_vector[i] = self.generate_push_data(i)
        self.function_vector[0x4c] = None
        self.function_vector[0x4d] = None
        self.function_vector[0x4e] = None
        self.function_vector[0x4f] = self.push_1_negate
        self.function_vector[0x51] = self.push_1
        for i in range(0x52, 0x61):
            self.function_vector[i] = self.generate_op_2_16(i-0x50)
        self.function_vector[0x93] = None
        self.function_vector[0x9c] = None
    
    def reset(self):
        self.stack.clear()
        self.program_rom = bytes()
        self.pc = 0
    
    def get_stack(self):
        return self.stack
    
    def push(self, byte_arr):
        self.stack.append(byte_arr)
    
    def pop(self):
        return self.stack.pop()

    def push_empty_byte_arr(self):
        self.push(bytes())
        self.pc += 1

    def generate_push_data(self, n_bytes):
        """Push a byte array of a given size onto the stack.

        The byte array is little endian.

        Keyword arguments:
        value -- it is the number of bytes that will be pushed, its minimun is 1 and
        its maximun is 75 
        """
        def push_n_bytes():
            if self.pc+n_bytes > len(self.program_rom)-1:
                raise Exception(BTCVMErrorMssg.NOT_ENOUGH_BYTES)
            byte_arr = self.program_rom[self.pc+1 : (self.pc+1)+n_bytes]
            self.push(byte_arr)
            self.pc += (n_bytes + 1)
        return push_n_bytes
    
    def push_1_negate(self):
        """Pushes the number -1 as an array of bytes of length 1 onto the stack.
        
        The byte array is little endian.
        """
        value = -1
        self.push(value.to_bytes(length=ByteSize.INT, byteorder="little", signed=True))
        self.pc += 1
    
    def push_1(self):
        """Pushes the number 1 as an array of bytes of length 1 onto the stack.
        
        The byte array is little endian.
        """
        value = 1
        self.push(value.to_bytes(length=ByteSize.INT, byteorder="little", signed=True))
        self.pc += 1
    
    def generate_op_2_16(self, n):
        """Pushes a value as a byte array of length 1 onto the stack.

        The byte array is little endian.

        Keyword arguments:
        value -- it is the number that will be pushed
        """
        def push_n():
            self.push(n.to_bytes(length=ByteSize.INT, byteorder="little", signed=False))
            self.pc += 1
        return push_n

    def add(self):
        if len(self.stack) < 2:
            raise Exception(BTCVMErrorMssg.BINARY_OP)
        value_1 = int.from_bytes(bytes=self.pop(), byteorder="little", signed=True)
        value_2 = int.from_bytes(bytes=self.pop(), byteorder="little", signed=True)
        number = value_1 + value_2
        n_bytes = (number.bit_length() + 7) // 8
        if n_bytes <= ByteSize.INT:
            self.push(number.to_bytes(length=ByteSize.INT, byteorder="little", signed=True))
        else:
            self.push(number.to_bytes(length=n_bytes, byteorder="little", signed=True))
        self.pc += 1
    
    def numequal(self):
        if len(self.stack) < 2:
            raise Exception(BTCVMErrorMssg.BINARY_OP)
        value_1 = int.from_bytes(bytes=self.pop(), byteorder="little", signed=True)
        value_2 = int.from_bytes(bytes=self.pop(), byteorder="little", signed=True)
        if value_1 == value_2:
            self.push((1).to_bytes(length=ByteSize.INT, byteorder="little", signed=True))
        else:
            self.push((0).to_bytes(length=ByteSize.INT, byteorder="little", signed=True))
        self.pc += 1

    def is_btc_binary(self, binary_type):
        return self.binary_type == binary_type
    
    def load_program(self, binary_program):
        self.program_rom += binary_program

    def process(self, binary):
        result = {"success": True, "err": ""}
        if len(binary) < 3 or not self.is_btc_binary(binary[0:3]):
            result["success"] = False
            result["err"] = BTCVMErrorMssg.NOT_BTC
            return result
        self.load_program(binary[3:])
        try:
            while self.pc < len(self.program_rom):
                op_code = self.program_rom[self.pc]
                func = self.function_vector[op_code]
                func()
            result["success"] = True
        except Exception as e:
            result["success"] = False
            result["err"] = f"{BTCVMErrorMssg.COULD_NOT_PROCESS}: {e}"
        return result


    
