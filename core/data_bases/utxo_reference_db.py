class UTXOReferenceDB:
    """This class represents a (key, dictionary) database,
    where key is a unsigned integer and the dictionary contains metadata to get a
    unspent transaction output
    """

    def __init__(self):
        """Initializes the class' attributes

        The class uses an array to store the metadata
        """
        self.utxo_references = []

    def add_utxo_reference(self, tx_hash, utxo_index):
        """Stores the transaction hash and the index of the unspent transaction output
        into the database
        
        Keyword arguments:
        tx_hash -- it is the hash of the transaction that contains
        the unspent transation output
        utxo_index -- it is an index that references a unspent transaction output contained in
        the unspent transaction output array
        """        
        self.utxo_references.append({
            "tx_hash": tx_hash,
            "utxo_index": utxo_index})
    
    def add_utxo_references(self, tx_hash, utxo_arr):
        """Stores the transaction hash and the index of the unspent transaction output
        into the database
        
        Keyword arguments:
        tx_hash -- it is the hash of the transaction that contains
        the unspent transation output array
        utxo_arr -- it is an array of unspent transaction outputs,
        it contains two elements, the first one is a unspent transaction output
        with the change and the second one is a new unspent transaction output
        which a beneficiary can spend 
        """
        for utxo_index in range(len(utxo_arr)):
            self.add_utxo_reference(tx_hash, utxo_index)

    def remove_utxo_reference(self, tx_hash, utxo_index):
        """Removes the reference that has the given trasaction hash and
        unspent transaction output index from the database
        
        Keyword arguments:
        tx_hash -- it is the hash of the transaction that contains
        the unspent transation output
        utxo_index -- it is an index that references a unspent transaction output contained in
        the unspent transaction output array
        """  
        for utxo_reference in self.utxo_references:
            if (utxo_reference["tx_hash"] == tx_hash and
                utxo_reference["utxo_index"] == utxo_index):
                self.utxo_references.remove(utxo_reference)
                break
    
    def remove_utxos_reference(self, tx_in_arr):
        """Removes the references to unspent transaction outputs contained in
        the trasaction input array 
        
        Keyword arguments:
        tx_in_arr -- it contains the transaction inputs that reference the 
        unspent transaction outputs
        """  
        for tx_in in tx_in_arr:
            self.remove_utxo_reference(tx_in.tx_hash, tx_in.utxo_index)
    
    def get_utxo_references(self):
        """Retrieves the whole array of references"""
        return self.utxo_references