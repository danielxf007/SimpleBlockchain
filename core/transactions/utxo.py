class UTXO:
    """This class represents a unspent transaction output"""

    def __init__(self, value, public_key):
        """Initializes the class' attributes

        Keyword arguments:
        value -- it is the amount of satoshi this unspent transaction output is worth
        public_key -- it is the public key that can spend this unspent transaction output
        """
        self.value = value
        self.public_key = public_key
    
    def can_spend(self, public_key):
        """Checks whether a public key can spend this unspent transaction output or not

        Keyword arguments:
        public_key -- it is the public key that wants to spend this unspent transaction output
        """
        return self.public_key == public_key
    
    def get_value(self):
        """Returns the value of this unspent transaction output"""
        return self.value