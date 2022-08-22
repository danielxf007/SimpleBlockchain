import hashlib
import pickle

class Blockchain:

    def __init__(self, blocks):
        self.previous_hash = hashlib.sha256('0'.encode()).hexdigest()
        self.blocks = blocks
    
    def get_block(self, height):
        if len(self.blocks) > 0 and len(self.blocks)-1 <= height:
            return self.blocks[height]
        return None
    
    def get_height(self):
        return len(self.blocks)-1
    
    def set_blocks(self, blocks):
        self.blocks = blocks

    def get_blocks(self):
        return self.blocks
        
    def get_previous_hash(self):
        return self.previous_hash

    def add(self, block):
        self.blocks.append(block)
        self.previous_hash = hashlib.sha256(pickle.dumps(block)).hexdigest()
    
    def get_transaction(self, req_tx_hash):
        for block in self.blocks:
            for tx in block.txs:
                tx_hash = hashlib.sha256(pickle.dumps(tx)).hexdigest()
                if req_tx_hash == tx_hash:
                    return tx
        return None
    
    def get_utxo(self, tx_hash, utxo_index):
        tx = self.get_transaction(tx_hash)
        if tx:
            return tx.get_utxo(utxo_index)
        return None