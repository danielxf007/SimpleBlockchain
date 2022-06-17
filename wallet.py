from transactions import UTXO, TXIn, TX

class Wallet:

    def __init__(self, pk):
        self.pk = pk
    
    def create_tx_inputs(self, available_utxo):
        inputs = []
        for data in available_utxo:
            inputs.append(TXIn(data['tx_id'], data['utxo_index'], self.pk))
        return inputs
    
    def get_input_value(self, valid_tx_db, input):
        return valid_tx_db.get_tx(input.tx_id).get_utxo(input.utxo_index).value
    
    def get_inputs_value(self, valid_tx_db, inputs):
        value = 0
        for input in inputs:
            value += self.get_input_value(valid_tx_db, input)
        return value

    def get_balance(self, valid_tx_db, inputs):
        return self.get_inputs_value(valid_tx_db, inputs)
    
    def get_inputs_to_cover_cost(self, valid_tx_db, inputs, cost):
        index = 1
        accum = cost
        for input in inputs:
            accum -= self.get_input_value(valid_tx_db, input)
            if accum <= 0:
                break
            index += 1
        return inputs[:index]

    def create_tx(self, valid_tx_db, available_utxo, to, amount, fee=0):
        cost = amount + fee
        inputs = self.create_tx_inputs(available_utxo)
        if self.get_balance(valid_tx_db, inputs) >= cost:
            tx_in_arr = self.get_inputs_to_cover_cost(valid_tx_db, inputs, cost)
            utxo_arr = []
            change_val =  self.get_inputs_value(valid_tx_db, tx_in_arr) - cost
            if change_val > 0:
                utxo_arr.append(UTXO(change_val, self.pk))
            if amount > 0:
                utxo_arr.append(UTXO(amount, to))
            return TX(self.pk, tx_in_arr, utxo_arr)
        else:
            return None
"""valid_tx_db = TXDB()
for i in range(random.randint(3, 30)):
    utxo_arr = []
    for j in range(random.randint(5, 40)):
        utxo = UTXO(random.randint(100, 10000), hashlib.sha256('0'.encode()).hexdigest())
        utxo_arr.append(utxo)
    tx = TX([], utxo_arr)
    tx_ser = pickle.dumps(tx)
    tx_hash = hashlib.sha256(tx_ser).hexdigest()
    valid_tx_db.add_tx(tx_hash, tx)
utxo_db = UTXODB()
pk = hashlib.sha256('0'.encode()).hexdigest()
for tx_id in valid_tx_db.txs.keys():
    tx = valid_tx_db.get_tx(tx_id)
    utxo_db.add_utxos(pk, tx_id, tx.utxo_arr)
wallet = Wallet(pk)
available_utxo = utxo_db.get_utxos(wallet.pk)
wallet = Wallet(pk)
tx = wallet.create_tx(valid_tx_db, available_utxo, [{'amount': 100000, 'pk': '0'}], 100000, 100)
tx_ser = pickle.dumps(tx)
tx_hash = hashlib.sha256(tx_ser).hexdigest()
valid_tx_db.add_tx(tx_hash, tx)
print(len(utxo_db.get_utxos(wallet.pk)))
utxo_db.remove_utxos(wallet.pk, tx.get_tx_in_arr())
print(len(utxo_db.get_utxos(wallet.pk)))
utxo_db.add_utxos(pk, tx_hash, tx.get_utxo_arr())
print(len(utxo_db.get_utxos(wallet.pk)))"""



"""
valid_tx_db = {}
for i in range(random.randint(3, 30)):
    utxo_arr = []
    for j in range(random.randint(5, 40)):
        utxo = UTXO(random.randint(100, 10000), hashlib.sha256('0'.encode()).hexdigest())
        utxo_arr.append(utxo)
    tx = TX([], utxo_arr)
    tx_ser = pickle.dumps(tx)
    valid_tx_db[hashlib.sha256(tx_ser).hexdigest()] = tx
utxo_space = {}
pk = hashlib.sha256('0'.encode()).hexdigest()
for tx_id in valid_tx_db.keys():
    tx = valid_tx_db[tx_id]
    if not pk in utxo_space.keys():
        utxo_space[pk] = []
    for utxo_index in range(len(tx.utxo_arr)):
        utxo_space[pk].append({'tx_id': tx_id, 'utxo_index': utxo_index})
wallet = Wallet(pk)
available_utxo = utxo_space[wallet.pk]
tx = wallet.create_tx(valid_tx_db, available_utxo, '0', 100000, 100)
available_utxo_arr = utxo_space[wallet.pk]
print(len(available_utxo_arr))
for input in tx.tx_in_arr:
    spent_utxo = None
    for available_utxo in available_utxo_arr:
        if available_utxo['tx_id'] == input.tx_id and available_utxo['utxo_index'] == input.utxo_index:
            spent_utxo = available_utxo
            break
    available_utxo_arr.remove(spent_utxo)
print(len(available_utxo_arr))
tx_id = hashlib.sha256(pickle.dumps(tx)).hexdigest()
for index in range(len(tx.utxo_arr)):    
    available_utxo_arr.append({'tx_id': tx_id, 'utxo_index': index})
print(len(available_utxo_arr))
utxo_space[wallet.pk] = available_utxo_arr

"""

