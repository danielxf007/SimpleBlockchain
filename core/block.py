class BlockHeader:
    """This class contains the fields of a block header"""

    def __init__(self, prev_hash, root_hash, height, difficulty, nonce):
        """Initializes the class' attributes

        Keyword arguments:
        prev_hash -- it is the hash of the previous block
        root_hash -- it is the root of a merkle tree which was build using the
        transactions in a block
        height -- it is the number of the block
        difficulty -- it is the number of binary zeroes which have to be found to 
        validate the proof of work
        nonce -- it is a number which will be changed everytime until
        the proof of work is valid
        """
        self.prev_hash = prev_hash
        self.root_hash = root_hash
        self.height = height
        self.difficulty = difficulty
        self.nonce = nonce
    
    def set_nonce(self, nonce):
        """Changes the current nonce for a new one"""
        self.nonce = nonce

class Block:
    """This class contains the fields of a block"""

    def __init__(self, header, tx_hash_arr):
        """Initializes the class' attributes
        
        Keyword arguments:
        header -- it is the header of this block
        tx_hash_arr -- it is the an array of hashed transactions
        """
        self.header = header
        self.tx_hash_arr = tx_hash_arr
    
    
