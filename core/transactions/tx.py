class TX:
    """This class represents a transaction"""

    def __init__(self, tx_inputs, utxos, coin_base=False):
        """Initializes the class' attributes

        Keyword arguments:
        creator_public_key -- it is the public key of the one making the transaction
        tx_inputs -- it contains the transaction inputs that reference the 
        unspent transaction outputs which are going to be used
        utxos -- it is an array of unspent transation outputs
        coin_base -- it is a flag that indicates whether this transaction is a special type
        that can be used to create btc and collect fees
        """
        self.tx_inputs = tx_inputs
        self.utxos = utxos
        self.coin_base = coin_base
    
    def get_tx_inputs(self):
        """Returns a the whole transaction input array"""
        return self.tx_inputs
    
    def get_utxos(self):
        """Returns a the whole unspent transaction output array"""
        return self.utxos
    
    def get_utxo(self, index):
        """Returns a utxo from the unspent transaction output array

        Keyword arguments:
        index -- it is a index in the unspent transaction output
        """
        if index < len(self.utxos):
            return self.utxos[index]
        return None
    
    def is_coin_base(self):
        """Checks whether this transaction is a special type 
        which can be used to create btc and collect fees
        """
        return self.coin_base