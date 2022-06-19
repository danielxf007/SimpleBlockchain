import pickle
import random
import hashlib
from transactions import TX, UTXO
from merkle_tree import MerkleTree
from block import BlockHeader, Block
from util import Util

class Miner:

    def __init__(self, pk):
        random.seed()
        self.current_block = None
        self.merkle_struct = None
        self.pk = pk
    
    def n_txs_request(self):
        return random.randint(10, 100)
    
    def validate_tx(self, valid_tx_db, tx):
        valid = True
        for tx_in in tx.get_tx_in_arr():
            valid_tx = valid_tx_db.get_tx(tx_in.tx_id)
            utxo = valid_tx.get_utxo(tx_in.utxo_index)
            if not utxo.p2k(tx_in.pk):
                valid = False
                break
        return valid

    def get_input_value(self, valid_tx_db, input):
        return valid_tx_db.get_tx(input.tx_id).get_utxo(input.utxo_index).value
    
    def get_inputs_value(self, valid_tx_db, inputs):
        value = 0
        for input in inputs:
            value += self.get_input_value(valid_tx_db, input)
        return value
    
    def get_utxos_value(self, utxos):
        value = 0
        for utxo in utxos:
            value += utxo.value
        return value 

    def create_coin_base_tx(self, valid_tx_db, txs):
        value = 0
        util = Util()
        if txs:
            for tx in txs:
                input_total_value = self.get_inputs_value(valid_tx_db, tx.tx_in_arr)
                utxo_total_value = self.get_utxos_value(tx.utxo_arr)
                value+=(input_total_value-utxo_total_value)
                value+=util.btc_to_satoshi(random.randint(1, 10))
        else:
            value = util.btc_to_satoshi(random.randint(50, 100))
        return TX(self.pk, [], [UTXO(0, self.pk), UTXO(value, self.pk)], True)
    
    def create_block(self, prev_hash, hashed_txs, difficulty):
        merkle_tree = MerkleTree()
        self.merkle_struct = merkle_tree.create(hashed_txs)
        header = BlockHeader(
            prev_hash,
            self.merkle_struct['root'],
            difficulty,
            0)
        self.current_block = Block(header, hashed_txs)
    
    def has_enough_zeros(self, hashed_header, difficulty):
        n_zeros = 0
        stop = False
        for n in hashed_header:
            nibble = f"{int(n, 16):0{4}b}"
            for bit in nibble:
                if bit == '0':
                    n_zeros+=1
                else:
                    stop = True
                    break
            if stop:
                break
        return n_zeros == difficulty

    def mining_block(self):
        nonce = 0
        while True:
            self.current_block.header.set_nonce(nonce)
            hashed_header = hashlib.sha256(pickle.dumps(self.current_block.header)).hexdigest()
            if self.has_enough_zeros(hashed_header, self.current_block.header.difficulty):
                break
            nonce+=1
        return self.current_block



