class TXDB:
    """This class represents a (key, transaction) data base,
    where key is the hash of transaction"""

    def __init__(self):
        """Initializes the class' attributes

        The class uses a dictionary to store the transactions
        """
        self.txs = {}

    def add_tx(self, tx_hash, tx):
        """Stores a new transaction into the database

        Keyword arguments:
        tx_hash -- it is the hash of the given transaction, it is going to be used as a key
        tx -- it is the transaction that is going to be stored
        """        
        self.txs[tx_hash] = tx
    
    def add_txs(self, txs_hash, txs):
        """Stores new transactions into the database

        Keyword arguments:
        txs_hash -- these are the hashes of the given transactions, they will be used as keys
        txs -- these are the transactions that are going to be stored into the database
        """      
        for i in range(len(txs)):
            self.txs[txs_hash[i]] = txs[i]
    
    def remove_tx(self, tx_hash):
        """Removes a transaction from the database

        Keyword arguments:
        tx_hash -- it is the key of the transaction
        """
        self.txs.pop(tx_hash, None)
    
    def remove_txs(self, txs_hash):
        """Removes transactions from the database

        Keyword arguments:
        txs_hash -- these are the key of the transactions
        """
        for tx_hash in txs_hash:
            self.remove_tx(tx_hash)
    
    def get_txs(self):
        """Retrieves all the trasactions"""
        return self.txs

    def get_tx(self, tx_hash):
        """Retrives a transaction from the database

        Keyword arguments:
        tx_hash -- it is the key associated with the transaction
        """
        return self.txs.get(tx_hash)
    
    def get_txs_by_hash(self, tx_hash_arr):
        """Retrives the trasactions that have the hashes in the given hash array

        Keyword arguments:
        tx_hash_arr -- these are the hashes of the trasactions that will be retrieved
        """
        txs = {}
        for tx_hash in tx_hash_arr:
            txs[tx_hash] = self.get_tx(tx_hash)
        return txs
    
    def n_txs(self):
        """Returns the number of txs stored"""
        return len(self.txs)