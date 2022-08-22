class BlockHeader:
    """This data structure contains the fields of a block header"""

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

class Block:
    """This data structure contains the fields of a block"""

    def __init__(self, header, txs, author, date):
        """Initializes the class' attributes
        
        Keyword arguments:
        header -- it is the header of this block
        txs-- it is a list  of transactions
        """
        self.header = header
        self.txs = txs
        self.author = author
        self.date = date
