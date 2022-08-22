class UTXOReferenceDB:
    """This class represents a (key, dictionary) database,
    where key is a unsigned integer and the dictionary contains metadata to get a
    unspent transaction output
    """

    def __init__(self, references):
        """Initializes the class' attributes

        Keyword arguments:

        references -- it is a copy of the global state of references
        """
        self.references = references
    
    def set_references(self, references):
        self.references = references

    def get_references(self):
        """Retrieves the whole array of references"""
        return self.references

    def add_reference(self, tx_hash, utxo_index):
        """Stores the transaction hash and the index of the unspent transaction output
        into the database
        
        Keyword arguments:
        tx_hash -- it is the hash of the transaction that contains
        the unspent transation output
        utxo_index -- it is an index that references a unspent transaction output contained in
        the unspent transaction output array
        """        
        self.references.append({
            "tx_hash": tx_hash,
            "utxo_index": utxo_index})

    def remove_reference(self, tx_hash, utxo_index):
        """Removes the reference that has the given trasaction hash and
        unspent transaction output index from the database
        
        Keyword arguments:
        tx_hash -- it is the hash of the transaction that contains
        the unspent transation output
        utxo_index -- it is an index that references a unspent transaction output contained in
        the unspent transaction output array
        """  
        for reference in self.references:
            if reference["tx_hash"] == tx_hash and reference["utxo_index"] == utxo_index:
                self.references.remove(reference)
                break
        
    def has_reference(self, tx_hash, utxo_index):
        for reference in self.references:
            if reference["tx_hash"] == tx_hash and reference["utxo_index"] == utxo_index:
                return True
        return False
    
