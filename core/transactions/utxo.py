class UTXO:
    """This data structure represents a unspent transaction output"""

    def __init__(self, value, lock_script):
        """Initializes the class' attributes

        Keyword arguments:
        value -- it is the amount of satoshi this unspent transaction output is worth
        lock_script -- it is the script key that if given the correct set of inputs
        allows the utxo to be spent
        """
        self.value = value
        self.lock_script = lock_script