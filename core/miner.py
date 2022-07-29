from core.block import Block
from core.block import BlockHeader
from core.merkle_tree import create_merkle_tree
from core.data_bases.tx_db import TXDB
from core.data_bases.utxo_reference_db import UTXOReferenceDB
from core.transactions.tx import TX
from core.transactions.utxo import UTXO
from util.conversions import btc_to_satoshi
import pickle
import random
import hashlib

class Miner:
    """This class allows an user to verify transactions, add a block to the chain and 
    get rewarded by it"""

    def __init__(self, public_key, tx_db_state, utxo_reference_db_state):
        """Creates an instance of two databases and copies their current state

        Keyword arguments:
        public_key -- it is the public_key assigned to this wallet
        tx_db_state -- it is the current state of the transaction database
        utxo_reference_db_state -- it is the current state of the unspent transaction
        out references database
        """
        self.public_key = public_key
        self.tx_db: TXDB = TXDB()
        self.utxo_reference_db = UTXOReferenceDB()
        self.tx_db.txs = tx_db_state
        self.utxo_reference_db.utxo_references = utxo_reference_db_state
    
    def get_tx_db_state(self):
        """Returns the state of the transaction database of this miner"""
        return self.tx_db.get_txs()
    
    def get_utxo_reference_db_state(self):
        """Returns the state of the references to unspent transaction outputs"""
        return self.utxo_reference_db.get_utxo_references()

    def set_tx_db_state(self, tx_db_state):
        """Changes the data stored in the transaction database by given state

        Keyword arguments:
        tx_db_state -- it is a copy of the global state of the transaction database
        """
        self.tx_db.txs = tx_db_state
    
    def set_utxo_reference_db_state(self, utxo_reference_db_state):
        """Changes the data stored in the unspent transaction
        out references database by given state

        Keyword arguments:
        tx_db_state -- it is a copy of the global state of the unspent transaction
        out references database
        """
        self.utxo_reference_db.utxo_references = utxo_reference_db_state
    
    def n_pending_txs_request(self):
        """Returns the number of pending transactions this miner will validate"""
        return random.randint(10, 100)

    def get_utxo_value(self, tx_in):
        """Returns the amount of satoshi from a unspent transaction output
        
        Keyword arguments:
        tx_in -- it is a transaction input from a pending transaction
        """
        tx = self.tx_db.get_tx(tx_in.tx_hash)
        utxo = tx.get_utxo(tx_in.utxo_index)
        return utxo.get_value()
    
    def get_utxos_value(self, tx_in_arr):
        """Returns the total amount of satoshi from a unspent transaction output
        
        Keyword arguments:
        tx_in_arr -- these are the transaction inputs from a pending transaction
        """
        value = 0
        for tx_in in tx_in_arr:
            value += self.get_utxo_value(tx_in)
        return value

    def create_coinbase_tx(self, txs):
        """Creates a transaction which allows to transfer created bitcoin and collect
        transaction fees which would be given to this miner, this transaction generates 
        a unspent transaction output with value 0 and gets the whole value as a transfer
        
        Keyword arguments:
        tx_db -- it is the global database 
        txs -- these are valid pending transactions
        """
        value = 0
        for tx in txs:
            input_total_value = self.get_utxos_value(tx.get_tx_in_arr())
            output_total_value = 0
            for utxo in tx.get_utxo_arr():
                output_total_value+=utxo.get_value()
            value+=(input_total_value-output_total_value)
        value+=btc_to_satoshi(random.randint(5, 10))
        return TX(self.public_key, [],
                 [UTXO(0, self.public_key), UTXO(value, self.public_key)], True)

    def valid_tx(self, tx):
        """Checks whether the transaction was allowed
        to spend the unspent transaction outputs or not, coinbase trasactions
        are assumed to be always valid 
        
        Keyword arguments:
        tx -- it is a pending transaction
        """
        valid = True
        if tx.is_coin_base():
            return valid
        for tx_in in tx.get_tx_in_arr():
            aux_tx = self.tx_db.get_tx(tx_in.tx_hash)
            if aux_tx:
                utxo = aux_tx.get_utxo(tx_in.utxo_index)
                if not utxo.can_spend(tx_in.public_key):
                    valid = False
                    break
            else:
                valid = False
                break
        return valid
    
    def update_tx_db(self, tx_hash, tx):
        """Updates the state of the current transaction data base
        by adding a new valid transaction into it
        
        Keyword arguments:
        tx_hash -- it is the hash of the valid pending transaction
        tx -- it is a valid pending transaction
        """
        self.tx_db.add_tx(tx_hash, tx)

    def update_utxo_reference_db(self, tx_hash, tx):
        """Updates the state of the current unspent transaction
        out references database by adding a new valid transaction into it
        
        Keyword arguments:
        tx_hash -- it is the hash of the valid pending transaction
        tx -- it is a valid pending transaction
        """
        self.utxo_reference_db.remove_utxos_reference(tx.get_tx_in_arr())
        self.utxo_reference_db.add_utxo_references(tx_hash, tx.get_utxo_arr())

    def update_databases(self, txs):
        """Updates the state of the current unspent transaction
        out references database and the current transaction data base
        by adding a new valid transaction into them
        
        Each transaction is serialized before getting hashed

        Keyword arguments:
        txs -- these are pending transactions
        """
        for tx in txs:
            if self.valid_tx(tx):
                tx_hash = hashlib.sha256(pickle.dumps(tx)).hexdigest()
                self.update_tx_db(tx_hash, tx)
                self.update_utxo_reference_db(tx_hash, tx)

    def has_enough_zeros(self, hashed_header, difficulty):
        """Checks whether a hashed block header has the asked number of zeroes

        Each number from the hash is transformed into a binary nibbel (4 bits),
        then the number of consecutives zeroes are counted

        Keyword arguments:
        hashed_header -- it is the hash of a block header
        difficulty -- it is the number of zeroes the hash must have
        """
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

    def hash_txs(self, txs):
        """Returns an array of hashed transactions

        Each transaction is serialized before getting hashed
        
        Keyword arguments:
        hashed_header -- it is the hash represented as a hexdigest of a block header
        txs -- it is an array of transactions
        """
        hashed_txs = []
        for tx in txs:
            hashed_txs.append(hashlib.sha256(pickle.dumps(tx)).hexdigest())
        return hashed_txs        

    def mining_block(self, prev_hash, txs, height, difficulty):
        """Returns a block whith a validated proof of work 
        
        The block header is serialized before hashing it

        Keyword arguments:
        prev_hash -- it is the hash of the previous block
        txs -- these are pending transactions
        height -- it is the number of the block
        difficulty -- it is the number of zeroes the hash must have
        """
        self.update_databases(txs)
        valid_txs = list(filter(lambda tx: self.valid_tx(tx), txs))
        coin_base_tx = self.create_coinbase_tx(valid_txs)
        self.update_databases([coin_base_tx])
        valid_txs = [coin_base_tx] + valid_txs
        hashed_txs = self.hash_txs(valid_txs)
        merkle_tree = create_merkle_tree(hashed_txs)
        block_header = BlockHeader(prev_hash, merkle_tree["root"], height, difficulty, 0)
        block = Block(block_header, hashed_txs)
        nonce = 0
        while True:
            block_header.set_nonce(nonce)
            hashed_header = hashlib.sha256(pickle.dumps(block_header)).hexdigest()
            if self.has_enough_zeros(hashed_header, block_header.difficulty):
                break
            nonce+=1
        return block


