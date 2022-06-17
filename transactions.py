class UTXO:

    def __init__(self, value, pk):
        self.value = value
        self.p2k = pk
    
    def p2k(self, pk):
        return self.pk == pk

class TXIn:

    def __init__(self, tx_id, utxo_index, pk):
        self.tx_id = tx_id
        self.utxo_index = utxo_index
        self.pk = pk

class TX:

    def __init__(self, creator, tx_in_arr, utxo_arr):
        self.creator = creator
        self.tx_in_arr = tx_in_arr
        self.utxo_arr = utxo_arr
    
    def get_tx_in_arr(self):
        return self.tx_in_arr
    
    def get_utxo_arr(self):
        return self.utxo_arr
    
    def get_utxo(self, index):
        return self.utxo_arr[index]