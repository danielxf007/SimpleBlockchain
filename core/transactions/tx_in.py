class TXIn:
    """This class represents a transaction input"""

    def __init__(self, tx_hash, utxo_index, public_key):
        """Initializes the class' attributes
        
        Keyword arguments:
        tx_hash -- it is the hash of the transaction that contains the
        unspent transaction output that will be spend
        utxo_index -- it indicates which unspent transaction output created in a tx
        will be spent
        public_key -- it is the public key of the one
        that will spend the unspent transaction output
        """
        self.tx_hash = tx_hash
        self.utxo_index = utxo_index
        self.public_key = public_key