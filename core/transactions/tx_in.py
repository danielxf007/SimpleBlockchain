class TXIn:
    """This data structure represents a transaction input"""

    def __init__(self, tx_hash, utxo_index, unlock_script):
        """Initializes the class' attributes
        
        Keyword arguments:
        tx_hash -- it is the hash of the transaction that contains the
        unspent transaction output that will be spend
        utxo_index -- it indicates which unspent transaction output created in a tx
        will be spent
        unlock_script -- it is a script with push only operations, which solved the
        lock script of the referenced utxo
        """
        self.tx_hash = tx_hash
        self.utxo_index = utxo_index
        self.unlock_script = unlock_script