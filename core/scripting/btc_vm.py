class BTCVM:
    """ This class represents a stack based virtual machine that
    is able to execute functions according to the data in tokens
    created by a BTC Tokenizer.

    The name for the functions and how they work can be seem on:
    https://wiki.bitcoinsv.io/index.php/Opcodes_used_in_Bitcoin_Script
    """
    
    def __init__(self):
        self.MAX_OP_CODES = 185
        self.stack = []
        self.function_vector = [None for _ in range(self.MAX_OP_CODES)]
        self.token_rom = []
        self.pc = 0 #Program counter
    
    def init_function_map(self):
        self.function_vector[0] = self.OP_0
        for i in range(1, 76):
            self.function_vector[i] = self.OP_1_75
        self.function_vector[76] = self.OP_PUSHDATA1
        self.function_vector[77] = self.OP_PUSHDATA2
        self.function_vector[78] = self.OP_PUSHDATA4
        self.function_vector[79] = self.OP_1NEGATE
        self.function_vector[80] = self.OP_1
        self.function_vector[139] = self.OP_1ADD
    
    def push(self, byte_arr):
        self.stack.append(byte_arr)
    
    def pop(self):
        pass

    def OP_0(self):
        self.push(bytes())

    def OP_1_75(self, value):
        """Push a byte array of a given size onto the stack.

        The byte array is little endian.

        Keyword arguments:
        value -- it is the number of bytes that will be pushed, its minimun is 1 and
        its maximun is 75 
        """
        self.push(bytes(value))
        """value.to_bytes(length=value.bit_length() + 7) // 8,
         byteorder="little", signed=True
        """
    
    def OP_PUSHDATA1(self, value):
        """Takes the next 1 byte as the number of bytes to push onto the stack.

        The byte array is little endian.

        Keyword arguments:
        value -- it is the number of bytes that will be pushed, its minimun is 1 and
        its maximun is 255 
        """
        self.push(bytes(value))
    
    def OP_PUSHDATA2(self, value):
        """Takes the next 2 bytes as the number of bytes to push onto the stack.

        The byte array is little endian.

        Keyword arguments:
        value -- it is the number of bytes that will be pushed, its minimun is 256 and
        its maximun is 65,535
        """
        self.push(bytes(value))
    
    def OP_PUSHDATA4(self, value):
        """Takes the next 2 bytes as the number of bytes to push onto the stack.

        The byte array is little endian.

        Keyword arguments:
        value -- it is the number of bytes that will be pushed, its minimun is 65,536 and
        its maximun is 4,294,967,295
        """
        self.push(bytes(value))
    
    def OP_1NEGATE(self):
        """Pushes the number -1 as an array of bytes of length 1 onto the stack.
        
        The byte array is little endian.
        """
        value = -1
        self.push(value.to_bytes(length=1, byteorder="little", signed=True))
    
    def OP_1(self):
        """Pushes the number 1 as an array of bytes of length 1 onto the stack.
        
        The byte array is little endian.
        """
        value = 1
        self.push(value.to_bytes(length=1, byteorder="little", signed=True))
    
    def OP_2_16(self, value):
        """Pushes a value as a byte array of length 1 onto the stack.

        The byte array is little endian.

        Keyword arguments:
        value -- it is the number that will be pushed
        """
        self.push(value.to_bytes(length=1, byteorder="little", signed=True))

    def OP_1ADD(self, args):
        pass


    
