class TX:
    """This class represents a transaction"""

    def __init__(self, creator_public_key, tx_in_arr, utxo_arr, coin_base=False):
        """Initializes the class' attributes

        Keyword arguments:
        creator_public_key -- it is the public key of the one making the transaction
        tx_in_arr -- it contains the transaction inputs that reference the 
        unspent transaction outputs which are going to be used
        utxo_arr -- it is an array of unspent transation outputs,
        it always contains two elements, the first one is a unspent transaction output
        with the change and the second one is a new unspent transaction output
        coin_base-- it is a flag that indicates whether this transaction is a special type
        that can be used to create btc and collect fees
        """
        self.creator_public_key = creator_public_key
        self.tx_in_arr = tx_in_arr
        self.utxo_arr = utxo_arr
        self.coin_base = coin_base
    
    def get_tx_in_arr(self):
        """Returns a the whole transaction input array"""
        return self.tx_in_arr
    
    def get_utxo_arr(self):
        """Returns a the whole unspent transaction output array"""
        return self.utxo_arr
    
    def get_utxo(self, index):
        """Returns a utxo from the unspent transaction output array

        Keyword arguments:
        index -- it is a index in the unspent transaction output
        """
        return self.utxo_arr[index]
    
    def is_coin_base(self):
        """Checks whether this transaction is a special type 
        which can be used to create btc and collect fees
        """
        return self.coin_base