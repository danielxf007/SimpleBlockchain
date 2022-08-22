from core.transactions.tx import TX
from core.transactions.utxo import UTXO
from core.block import Block
from core.block import BlockHeader
from core.blockchain import Blockchain
from core.data_bases.utxo_reference_db import UTXOReferenceDB
from core.scripting.assembler import Assembler
from core.scripting.btc_vm import BTCVM
from core.merkle_tree import create_merkle_tree
from util.conversions import btc_to_satoshi
from datetime import datetime
import pickle
import random
import hashlib

class Miner:
    """This class allows an user to verify transactions, add a block to the chain and 
    get rewarded by it"""

    def __init__(self, public_key, blocks, utxo_references):
        """Creates an instance of two databases and copies their current state

        Keyword arguments:
        public_key -- it is the public key string of a wallet which became a miner
        blocks -- it is a copy of the current state of the global blockchain
        utxo_reference_db_state -- it is a copy of the current state of the unspent 
        transaction out references database
        """
        self.public_key = public_key
        self.blockchain = Blockchain(blocks)
        self.utxo_reference_db = UTXOReferenceDB(utxo_references)
        self.assembler = Assembler()
        self.btcvm = BTCVM()
        self.p2k = f"\"{public_key}\" OP_CHECKSIG"

    def set_blocks(self, blocks):
        """Changes the data blockchain state

        Keyword arguments:
        blocks -- it is the global state of the chain
        """
        self.blockchain.set_blocks(blocks)
    
    def set_utxo_references(self, utxo_references):
        """Changes the references on the references db

        Keyword arguments:
        utxo_references -- it is a copy of the global state of the unspent transaction
        out references
        """
        self.utxo_reference_db.set_references(utxo_references)
    
    def get_utxo_references(self):
        return self.utxo_reference_db.get_references()
    
    def n_pending_txs_request(self):
        """Returns the number of pending transactions this miner will validate"""
        return random.randint(10, 100)

    def get_utxo_value(self, tx_in):
        """Returns the amount of satoshi from a unspent transaction output
        
        Keyword arguments:
        tx_in -- it is a transaction input from a pending transaction
        """
        utxo = self.blockchain.get_utxo(tx_in.tx_hash, tx_in.utxo_index)
        value = 0
        if utxo:
            value = utxo.value
        return value
    
    def get_utxos_value(self, tx_inputs):
        """Returns the total amount of satoshi from a unspent transaction output
        
        Keyword arguments:
        tx_inputs -- these are the transaction inputs from a pending transaction
        """
        value = 0
        for tx_in in tx_inputs:
            value += self.get_utxo_value(tx_in)
        return value

    def create_coinbase_tx(self, txs):
        """Creates a transaction which allows to transfer created bitcoin and collect
        transaction fees which would be given to this miner, this transaction generates 
        a unspent transaction output with value 0 and gets the whole value as a transfer
        
        Keyword arguments:
        txs -- these are valid pending transactions
        """
        value = 0
        for tx in txs:
            input_total_value = self.get_utxos_value(tx.get_tx_inputs())
            output_total_value = 0
            for utxo in tx.get_utxos():
                output_total_value+=utxo.value
            value += (input_total_value-output_total_value)
        value += btc_to_satoshi(random.randint(5, 10))
        return TX([], [UTXO(value, self.p2k)], True)

    def validate_tx(self, tx):
        """Checks whether the transaction was allowed
        to spend the unspent transaction outputs or not, transactions are added to the
        utxo referece database of the miner, used utxos are removed from the utxo referece
        database of the miner
        
        Keyword arguments:
        tx -- it is a pending transaction
        """
        valid = True
        tx_inputs = tx.get_tx_inputs()
        i = 0
        while i < len(tx_inputs):
            tx_input = tx_inputs[i]
            if self.utxo_reference_db.has_reference(tx_input.tx_hash, tx_input.utxo_index):
                utxo = self.blockchain.get_utxo(tx_input.tx_hash, tx_input.utxo_index)
                script = tx_input.unlock_script + utxo.lock_script
                assembly_result = self.assembler.assemble(script)
                if assembly_result["success"]:
                    self.btcvm.reset()
                    success, _ = self.btcvm.process(assembly_result["binary"])
                    if success and self.btcvm.on_valid_state():
                        self.utxo_reference_db.remove_reference(tx_input.tx_hash,
                         tx_input.utxo_index)
                    else:
                        valid = False
                        break
                else:
                    valid = False
                    break
            else:
                valid = False
                break
            i += 1
        if not valid:
            for j in range(i):
                tx_input = tx_inputs[j]
                self.utxo_reference_db.add_reference(tx_input.tx_hash, tx_input.utxo_index)
        return valid

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

    def mining_block(self, txs, difficulty):
        """Returns a block whith a header that holds metadata, a nonce for proof and 
        transactions

        The block header is serialized before hashing it

        Keyword arguments:
        txs -- these are pending transactions
        height -- it is the number of the block
        difficulty -- it is the number of zeroes the hash must have
        """
        valid_txs = list(filter(lambda tx: self.validate_tx(tx), txs))
        coin_base_tx = self.create_coinbase_tx(valid_txs)
        valid_txs = [coin_base_tx] + valid_txs
        hashed_txs = self.hash_txs(valid_txs)
        merkle_tree = create_merkle_tree(hashed_txs)
        prev_hash = self.blockchain.get_previous_hash()
        height = self.blockchain.get_height()+1
        block_header = BlockHeader(prev_hash, merkle_tree["root"], height, difficulty, 0)
        nonce = 0
        while True:
            block_header.nonce = nonce
            hashed_header = hashlib.sha256(pickle.dumps(block_header)).hexdigest()
            if self.has_enough_zeros(hashed_header, block_header.difficulty):
                break
            nonce += 1
        block = Block(block_header, valid_txs, self.public_key, datetime.now())
        for i in range(len(coin_base_tx.get_utxos())):
            self.utxo_reference_db.add_reference(hashed_txs[0], i)
        return block


