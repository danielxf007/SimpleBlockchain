from core.data_bases.tx_db import TXDB
from core.data_bases.utxo_reference_db import UTXOReferenceDB
from core.transactions.tx import TX
from core.transactions.tx_in import TXIn
from core.transactions.utxo import UTXO
from itertools import permutations
import hashlib
import pickle
import sys

from util.conversions import satoshi_to_btc

class Wallet:
    """This class allows the user to create transactions """

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

    def get_available_utxo_references(self):
        """Returns the references to unspent transaction outputs this wallet can spend"""
        utxo_references = self.utxo_reference_db.get_utxo_references()
        available_utxo_references = []
        for utxo_reference in utxo_references:
            tx = self.tx_db.get_tx(utxo_reference["tx_hash"])
            utxo = tx.get_utxo(utxo_reference["utxo_index"])
            if utxo.can_spend(self.public_key):
                available_utxo_references.append(utxo_reference)
        return available_utxo_references
    
    def create_tx_inputs(self, utxo_references):
        """Returns the transaction inputs with the references to
        unspent transaction outputs this wallet can spend
        
        Keyword arguments:
        utxo_references -- these are refereces to unspent transaction outputs
        this wallet can spend
        """
        tx_inputs = []
        for utxo_reference in utxo_references:
            tx_input = TXIn(utxo_reference["tx_hash"], utxo_reference['utxo_index'],
                            self.public_key)
            tx_inputs.append(tx_input)
        return tx_inputs
    
    def get_utxo_value(self, tx_in):
        """Returns the amount of satoshi from a unspent transaction output

        Keyword arguments:
        tx_in -- it is the transaction input which holds a referece to
        a unspent transaction output this wallet can spend
        """
        tx = self.tx_db.get_tx(tx_in.tx_hash)
        utxo = tx.get_utxo(tx_in.utxo_index)
        return utxo.get_value()

    def get_utxos_value(self, tx_in_arr):
        """Returns the total amount of satoshi from the references in the
        transactions inputs

        Keyword arguments:
        tx_in_arr -- these are the transaction inputs which hold a referece to
        a unspent transaction output this wallet can spend
        """
        value = 0
        for tx_in in tx_in_arr:
            value += self.get_utxo_value(tx_in)
        return value
    
    def get_balance(self):
        """Returns the total amount of satoshi this wallets owns

        This method is not mean to be used inside the class but
        for external consultation purposes
        
        """
        utxo_references = self.get_available_utxo_references()
        tx_in_arr = self.create_tx_inputs(utxo_references)
        return self.get_utxos_value(tx_in_arr)
    
    def get_available_utxo_values(self):
        """Returns the values greatet than 0 
        of each unspent transaction this wallet can use

        This method is not mean to be used inside the class but
        for external consultation purposes     
        """
        utxo_references = self.get_available_utxo_references()
        tx_in_arr = self.create_tx_inputs(utxo_references)
        values = []
        for tx_in in tx_in_arr:
            value = self.get_utxo_value(tx_in)
            if value > 0:
                values.append(self.get_utxo_value(tx_in))
        return values

    def get_tx_inputs_to_cover_cost(self, tx_in_arr, cost):
        """Returns the transaction inputs which can be used to pay for a cost

        The algorithm excludes unspent transactions outputs with value 0 and 
        tries to use, few unspent transactions outputs and the
        ones which have the least value to cover the cost 

        Keyword arguments:
        tx_in_arr -- these are the transaction inputs which hold a referece to
        a unspent transaction output this wallet can spend
        cost -- it is the amount of satoshi which will be spent on a transaction
        """
        tx_in_arr_fil = list(filter(lambda tx_in: self.get_utxo_value(tx_in) > 0, tx_in_arr))
        tx_inputs_permutations = list(permutations(tx_in_arr_fil))
        min_tx_inputs = tx_in_arr_fil[:]
        min_value = sys.maxsize
        for tx_inputs in tx_inputs_permutations:
            index = 1
            value = 0
            for tx_in in tx_inputs:
                value+=self.get_utxo_value(tx_in)
                if cost - value <= 0:
                    break
                index += 1
            choosen_tx_inputs = tx_inputs[:index]
            if len(choosen_tx_inputs) < len(min_tx_inputs) and value < min_value:
                min_tx_inputs = choosen_tx_inputs
                min_value = value
        return min_tx_inputs
    
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

    def create_tx(self, to, amount, change_target, fee=0):
        """Adds a transaction to the current version of the databases in this wallet
        and returns it

        Keyword arguments:
        to -- it is the public key of the beneficiary wallet
        amount -- it is the amount of satoshi that will be transfered
        change_target -- it is the public key of the wallet which would get 
        the change
        fee -- it is the amount of satoshi this transaction is going to pay to a miner
        """
        cost = amount + fee
        utxo_references = self.get_available_utxo_references()
        tx_in_arr = self.create_tx_inputs(utxo_references)
        balance = self.get_utxos_value(tx_in_arr)
        tx = None
        if balance >= cost:
            tx_in_arr = self.get_tx_inputs_to_cover_cost(tx_in_arr, cost)
            utxo_arr = []
            change_val = self.get_utxos_value(tx_in_arr) - cost
            utxo_arr.append(UTXO(change_val, change_target))
            utxo_arr.append(UTXO(amount, to))
            tx = TX(self.public_key, tx_in_arr, utxo_arr)
            tx_hash = hashlib.sha256(pickle.dumps(tx)).hexdigest()
            self.update_tx_db(tx_hash, tx)
            self.update_utxo_reference_db(tx_hash, tx)
        return tx