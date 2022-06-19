from data_bases import AvailableUTXODB, TXDB
from transactions import UTXO, TXIn, TX
import hashlib
import pickle

class Wallet:

    def __init__(self, pk, tx_db_state):
        self.pk = pk
        self.available_utxo_db = AvailableUTXODB()
        self.tx_db: TXDB = TXDB()
        self.tx_db.txs = tx_db_state
    
    def create_tx_inputs(self):
        inputs = []
        for data in self.available_utxo_db.data:
            inputs.append(TXIn(data['tx_id'], data['utxo_index'], self.pk))
        return inputs
    
    def get_input_value(self, input):
        return self.tx_db.get_tx(input.tx_id).get_utxo(input.utxo_index).value
    
    def get_inputs_value(self, inputs):
        value = 0
        for input in inputs:
            value += self.get_input_value(input)
        return value

    def get_balance(self, inputs):
        return self.get_inputs_value(inputs)
    
    def get_wallet_balance(self):
        inputs = self.create_tx_inputs()
        return self.get_balance(inputs)
    
    def get_inputs_to_cover_cost(self, inputs, cost):
        index = 1
        accum = cost
        for input in inputs:
            accum -= self.get_input_value(input)
            if accum <= 0:
                break
            index += 1
        return inputs[:index]

    def create_tx(self, to, amount, fee=0):
        cost = amount+fee
        inputs = self.create_tx_inputs()
        balance = self.get_balance(inputs)
        tx = None
        if balance >= cost:
            tx_in_arr = self.get_inputs_to_cover_cost(inputs, cost)
            utxo_arr = []
            change_val = self.get_inputs_value(tx_in_arr) - cost
            utxo_arr.append(UTXO(change_val, self.pk))
            utxo_arr.append(UTXO(amount, to))
            tx = TX(self.pk, tx_in_arr, utxo_arr)
            tx_id = hashlib.sha256(pickle.dumps(tx)).hexdigest()
            self.tx_db.add_tx(tx_id, tx)
            self.available_utxo_db.remove_utxos(tx.get_tx_in_arr())
            if self.pk == to:
                self.available_utxo_db.add_utxos(tx_id, tx.get_utxo_arr())
            else:
                self.available_utxo_db.add_utxo(tx_id, 0)
        return tx