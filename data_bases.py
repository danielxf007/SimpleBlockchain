from transactions import UTXO


class MerkleDB:

    def __init__(self):
        self.trees = {}
    
    def add_tree(self, root, structure, n_bits):
        self.trees[root] = {'structure': structure, 'n_bits': n_bits}
    
    def get_merkle_path(self, root, tx_index):
        """
        Returns a path of the form [(i, node_hash), ..., (k, node_hash)]
        i=1: the node_hash has to be concatenated to the right
        i=0: the node_hash has to be concatenated to the left
        """
        structure = self.trees[root]['structure']
        n_bits = self.trees[root]['n_bits']
        path = f"{tx_index:0{n_bits}b}"
        merkle_path = []
        for i in path[:len(path)-1]:
            if i == '0':
                merkle_path = [(1, structure[2 if len(structure) == 3 else 1][0])] + merkle_path
                structure = structure[1]
            else:
                merkle_path = [(0, structure[1][0])] + merkle_path
                structure = structure[2 if len(structure) == 3 else 1]
        if path[len(path)-1] == '0':
            merkle_path = [(1, structure[2 if len(structure) == 3 else 1])] + merkle_path
        else:
            merkle_path = [(0, structure[1])] + merkle_path
        return merkle_path

class TXDB:

    def __init__(self):
        self.txs = {}
    
    def add_tx(self, tx_hash, tx):
        self.txs[tx_hash] = tx
    
    def add_txs(self, txs, txs_hash):
        for i in range(len(txs)):
            self.txs[txs_hash[i]] = txs[i]
    
    def get_tx(self, tx_hash):
        return self.txs[tx_hash]
    
    def remove_tx(self, tx_hash):
        self.txs.pop(tx_hash, None)
    
    def remove_txs(self, txs_hash):
        for tx_hash in txs_hash:
            self.remove_tx(tx_hash)
    
    def get_n_txs(self, n):
        if len(self.txs) == 0:
            return []
        txs = []
        for tx_hash in self.txs:
            txs.append(self.txs[tx_hash])
            if len(txs) == n:
                break
        return txs
    
    def n_txs(self):
        return len(self.txs)

class AvailableUTXODB:

    def __init__(self):
        self.data = []
    
    def add_utxo(self, tx_id, utxo_index):
        self.data.append({
            'tx_id': tx_id,
            'utxo_index': utxo_index})
    
    def add_utxos(self, tx_id, utxos):
        for utxo_index in range(len(utxos)):
            self.add_utxo(tx_id, utxo_index)
    
    def remove_utxo(self, tx_id, utxo_index):
        for element in self.data:
            if element['tx_id'] == tx_id and element['utxo_index'] == utxo_index:
                self.data.remove(element)
                break
    
    def remove_utxos(self, tx_in_arr):
        for tx_in in tx_in_arr:
            self.remove_utxo(tx_in.tx_id, tx_in.utxo_index)
            

class UTXODB:

    def __init__(self):
        self.data = {}
    
    def add_utxos(self, tx_id, utxo_arr):
        for utxo_index in range(len(utxo_arr)):
            utxo: UTXO = utxo_arr[utxo_index]
            if not utxo.pk in self.data.keys():
                self.data[utxo.pk] = []
            self.data[utxo.pk].append({
            'tx_id': tx_id,
            'utxo_index': utxo_index
            })
    
    def remove_utxos(self, pk, tx_in_arr):
        for tx_in in tx_in_arr:
            for element in self.data[pk]:
                if tx_in.tx_id == element['tx_id'] and tx_in.utxo_index == element['utxo_index']:
                    self.data[pk].remove(element)
                    break
    
    def get_utxos(self, pk):
        if not pk in self.data.keys():
            return []
        return self.data[pk]
