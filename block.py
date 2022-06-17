class BlockHeader:

    def __init__(self, prev_hash, root_hash, difficulty, nonce):
        self.prev_hash = prev_hash
        self.root_hash = root_hash
        self.difficulty = difficulty
        self.nonce = nonce
    
    def set_nonce(self, nonce):
        self.nonce = nonce

class Block:

    def __init__(self, header, tx_hash_arr):
        self.header = header
        self.tx_hash_arr = tx_hash_arr
    
    
