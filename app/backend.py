from core.data_bases.tx_db import TXDB
from core.data_bases.utxo_reference_db import UTXOReferenceDB
from core.wallet import Wallet
from core.miner import Miner
from util.conversions import btc_to_satoshi
from util.conversions import satoshi_to_btc
from datetime import datetime
import pickle
import hashlib
import random

class Backend:
    """This classes uses the core elements
    
    The whole system uses satoshi and it has eight decimals of precision, values smaller
    than 1/10^8 are considered to be 0
    """

    def __init__(self):
        """Initializes the class' attributes"""
        self.wallets = {}
        self.miners = {}
        self.names_file_path = "names.txt"
        self.n_names = 18238
        self.pending_txs = []
        self.tx_db = TXDB()
        self.utxo_reference_db = UTXOReferenceDB()
        self.last_block_hash = hashlib.sha256('0'.encode()).hexdigest()
        self.blockchain = []
        self.blockchain_history = []
        self.current_fee = random.randint(10**2, 10**3)
    
    def init_system(self):
        """Initializes the system by creating a user called Satoshi and mining
        the genesis block, it also returns a list of messages about the operations
        """
        messages = []
        user_name = "Satoshi"
        messages.append(self.create_wallet(user_name)["message"])
        messages.append(self.create_miner(user_name))
        messages.append(self.mining_block())
        return messages

    def create_wallet(self, user_name):
        """Returns a dictionary with a sucess flags and a message

        Keyword arguments:
        user_name -- it is the name associated to the wallet
        """
        if not user_name in self.wallets.keys():
            public_key = hashlib.sha256(user_name.encode()).hexdigest()
            tx_db_state = self.tx_db.get_txs().copy()
            utxo_reference_db_state = self.utxo_reference_db.get_utxo_references().copy()
            wallet = Wallet(public_key, tx_db_state, utxo_reference_db_state)
            self.wallets[user_name] = wallet
            return {"success": True,
                    "message": f"{user_name} your wallet was created"}
        return {"success": False,
                "message": f"The user {user_name} has already created a wallet"}
    
    def create_random_wallets(self, n_r_wallets):
        """Reads a random name from a text file and returns a list of messages

        Keyword arguments:
        n_r_wallets -- it is the number of wallets that are going to be created
        """
        names_file = open(self.names_file_path, 'r')
        messages = []
        n_created_wallets = 0
        while n_created_wallets < n_r_wallets:
            names_file.seek(0, 0)
            line = random.randint(0, self.n_names)
            while line:
                user_name = names_file.readline().strip()
                line-=1
            success, message = self.create_wallet(user_name).values()
            if success:
                messages.append(message)
                n_created_wallets+=1
        names_file.close()
        return messages

    def get_wallet_balance(self, user_name):
        """Gets the balance of a wallet and returns a formatted message

        Keyword arguments:
        user_name -- it is the name of a user who has a wallet
        """
        balance = 0
        if user_name in self.wallets.keys():
            wallet = self.wallets[user_name]
            balance = wallet.get_balance()
            return f"{user_name} has {satoshi_to_btc(balance):.8f} BTC"
        return f"{user_name} has no wallet"
    
    def get_wallet_available_utxo_values(self, user_name):
        """Gets the balance values of unspent transaction output the given user
        can spend and returns a formatted message

        Keyword arguments:
        user_name -- it is the name of a user who has a wallet
        """
        messages = []
        if user_name in self.wallets.keys():
            wallet:Wallet = self.wallets[user_name]
            index = 1
            for utxo_value in wallet.get_available_utxo_values():
                message = f"{index}.UTXO Value: {satoshi_to_btc(utxo_value):.8f} BTC"
                messages.append(message)
                index+=1
            if not messages:
                message = f"{user_name} there are not UTXOs that you can spend"
                messages.append(message)
        else:
            messages.append(f"{user_name} has no wallet")
        return messages


    def get_n_wallets(self):
        """Gets the number of wallets in the system and returns a formatted message"""
        return f"There are {len(self.wallets.keys())} wallets in the system"

    def get_wallets(self):
        """Gets all the wallets in the system and returns an array of formatted messages"""
        messages = []
        for user_name in self.wallets.keys():
            message = f"Wallet user: {user_name}"
            messages.append(message)
        return messages

    def create_miner(self, user_name):
        """Returns a formatted message

        Keyword arguments:
        user_name -- it is the name of a user who has a wallet
        """
        if user_name in self.wallets.keys():
            if not user_name in self.miners.keys():
                wallet = self.wallets[user_name]
                tx_db_state = self.tx_db.get_txs().copy()
                utxo_reference_db_state = self.utxo_reference_db.get_utxo_references().copy()
                miner = Miner(wallet.public_key, tx_db_state, utxo_reference_db_state)
                self.miners[user_name] = miner
                return f"{user_name} you can now mine blocks!"
            return f"{user_name} can mine blocks already!"
        return f"{user_name} has no wallet"

    def create_miner_r(self, n_r_miners):
        """Chooses random wallets to be miners and returns a list of formatted messages

        Keyword arguments:
        n_r_miners -- it is the number of miners that could be created
        """
        messages = []
        if n_r_miners:
            miner_keys = list(self.miners.keys())
            users = list(self.wallets.keys())
            candidates = list(filter(lambda user_name: not user_name in miner_keys, users))
            n_available = n_r_miners
            while n_available and candidates:
                choosen_user = candidates[random.randint(0, len(candidates)-1)]
                message = self.create_miner(choosen_user)
                messages.append(message)
                n_available-=1
                candidates.remove(choosen_user)
        return messages

    def get_miners(self):
        """Gets all the miners in the system and returns an array of formatted messages"""
        messages = []
        for user_name in self.miners.keys():
            message = f"Miner: {user_name}"
            messages.append(message)
        return messages
    
    def get_fee(self):
        """Gets a message with the current transaction fee on BTC"""
        return f"The current transaction fee is: {satoshi_to_btc(self.current_fee):.8f} BTC"


    def transfer(self, from_user, to_user, amount, change_target):
        """Creates a transaction, saves it into a pending transaction list and
        returns a dictionary with a sucess flags and a formatted message

        Keyword arguments:
        from_user -- it is the user who wants to tranfer btc
        to_user -- it is the user who will get the btc
        amount -- it is the amount of btc that will be transfered
        change_target -- it is the user who will get the change generated by the transaction
        fee -- it is the amount of btc the miner will be paid for their work 
        """
        if not from_user in self.wallets.keys():
            return f"The user {from_user} has no wallet"
        elif not to_user in self.wallets.keys():
            return f"The user {to_user} has no wallet"
        elif not change_target in self.wallets.keys():
            return f"The user {change_target} has no wallet"
        source_wallet = self.wallets[from_user]
        dest_wallet = self.wallets[to_user]
        change_wallet = self.wallets[change_target]
        tx = source_wallet.create_tx(
            dest_wallet.public_key,
            btc_to_satoshi(float(amount)),
            change_wallet.public_key,
            self.current_fee)
        if tx:
            self.pending_txs.append(tx)
            return {"success": True,
                    "message": f"{from_user} your transaction is waiting to be approved"}
        return {"success": True,
                "message": f"{from_user} you don't have enough balance"}
                

    def make_r_txs(self, n_transactions):
        """Creates random trasactions using the user Satohsi, finally it returns a list
        of formatted messages

        Keyword arguments:
        n_transactions -- it is the random number of transactions to be made
        """
        targets = list(self.wallets.keys())
        messages = []
        for _ in range(n_transactions):
            target = targets[random.randint(0, len(targets)-1)]
            amount = random.uniform(10**-3, 10**-4)
            change_target = "Satoshi"
            success, message = self.transfer("Satoshi", target, amount, change_target).values()
            messages.append(message)
            if not success:
                break
        return messages

    def choose_miner(self):
        """Returns a randomly selected miner who will mine the block"""
        miner_keys = list(self.miners.keys())
        miner_key = miner_keys[random.randint(0, len(miner_keys)-1)]
        return miner_key
    
    def update_global_dbs(self, miner):
        """Updates the trasaction database and the references to unspent transaction
        outputs database by storing a copy of the current state of this databases the miner has
        after validating the transactions

        Keyword arguments:
        miner -- it is the miner who added the new block
        """
        self.tx_db.txs = miner.get_tx_db_state().copy()
        self.utxo_reference_db.utxo_references = miner.get_utxo_reference_db_state().copy()


    def update_wallet_dbs(self):
        """Updates the trasaction database and the references to unspent transaction
        outputs database by storing a copy of the current state of the global state of these
        databases
        """
        for key in self.wallets.keys():
            wallet = self.wallets[key]
            wallet.set_tx_db_state(self.tx_db.get_txs().copy())
            wallet.set_utxo_reference_db_state(
                self.utxo_reference_db.get_utxo_references().copy())

    def update_miner_dbs(self):
        """Updates the trasaction database and the references to unspent transaction
        outputs database by storing a copy of the current state of the global state of these
        databases
        """
        for key in self.miners.keys():
            miner = self.miners[key]
            miner.set_tx_db_state(self.tx_db.get_txs().copy())
            miner.set_utxo_reference_db_state(
                self.utxo_reference_db.get_utxo_references().copy())
    
    def update_fee(self):
        """Updates the fee that must be payed for a transaction

        The fee unit is satoshi
        """
        self.current_fee = random.randint(10**2, 10**3)
    
    def valid_proof_of_work(self, hashed_header, difficulty):
        """Checks whether the proof of work a miner did is valid or not

        Each number from the hash is transformed into a binary nibbel (4 bits),
        then the number of consecutives zeroes are counted
        
        Keyword arguments:
        hashed_header -- it is the hash represented as a hexdigest of the block header
        difficulty -- it is the number of zeroes the hash must have, according to the
        block header
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

    def mining_block(self):
        """This method is used to add a new block to the chain,
        update the global databases, update the transaction fee and
        save data to indentify who was the block's author, which block was added and
        when he added the block, finally it returns a formatted message

        The proof of work is checked before accepting the block
        The block header is serialized before hashing it
        The transactions that were not validated on the new block are wiped out
        """
        miner_key = self.choose_miner()
        miner = self.miners[miner_key]
        n_txs = miner.n_pending_txs_request()
        if n_txs < len(self.pending_txs):
            txs = self.pending_txs[:n_txs]
        else:
            txs = self.pending_txs
        difficulty = random.randint(1, 16)
        height = len(self.blockchain)
        block = miner.mining_block(self.last_block_hash, txs, height, difficulty)
        block_header = block.header
        hashed_header = hashlib.sha256(pickle.dumps(block_header)).hexdigest()
        if not self.valid_proof_of_work(hashed_header, block.header.difficulty):
            return f"The miner {miner_key} did not present a valid proof of work"
        self.blockchain.append(block)
        self.update_global_dbs(miner)
        self.update_wallet_dbs()
        self.update_miner_dbs()
        self.update_fee()
        self.last_block_hash = hashlib.sha256(pickle.dumps(block)).hexdigest()
        self.pending_txs.clear()
        self.blockchain_history.append({"author": miner_key, "height": height,
                                        "date": datetime.now()})
        return f"The miner {miner_key} added the block #{height} to the chain"

    def get_user_name(self, public_key):
        """Returns the user name which has a wallet with the given public key

        Keyword arguments:
        public_key -- it is a public key associated to a wallet      
        """
        user_name = ""
        for key in self.wallets.keys():
            wallet = self.wallets[key]
            if public_key == wallet.public_key:
                user_name = key
        return user_name
    
    def get_tx_format(self, tx):
        """Returns a a dictionary with a format which will be used to print the
        data in the trasaction

        Keyword arguments:
        tx -- it is a transaction that will be printed
        """
        format = {}
        from_user = self.get_user_name(tx.creator_public_key)
        change_utxo = tx.get_utxo_arr()[0]
        transfer_utxo = tx.get_utxo_arr()[1]
        change_beneficiary = self.get_user_name(change_utxo.public_key)
        transfer_beneficiary = self.get_user_name(transfer_utxo.public_key)
        change_value = satoshi_to_btc(change_utxo.value)
        transfer_value = satoshi_to_btc(transfer_utxo.value)
        if not tx.coin_base:
            format["change"] = f"{change_beneficiary} got {change_value:.8f} BTC as change"
            format["transfer"] = f"{from_user} transfered {transfer_value:.8f} BTC to {transfer_beneficiary}"
        else:
            format["transfer"] = f"{transfer_beneficiary} got rewarded with {transfer_value:.8f} BTC for mining"
        return format
    
    def get_block_format(self, block_height):
        """Returns a a dictionary with a format which will be used to print the
        data in the block

        Keyword arguments:
        block_height -- it is the index where the block can be found
        """        
        format = {}
        if block_height > len(self.blockchain)-1:
            format["Err"] = f"The block #{block_height} has not been added to the chain yet"
            return format
        format["n_sep_lines"] = 100
        block = self.blockchain[block_height]
        author = self.blockchain_history[block_height]["author"]
        format["author"] = f"Author: {author}"
        block_header = block.header
        format["prev_hash"] = f"Previous Block Hash: {block_header.prev_hash}"
        format["root_hash"] = f"Root Hash: {block_header.root_hash}"
        format["height"] = f"Height: {block_header.height}"
        format["difficulty"] = f"Difficulty: {block_header.difficulty}"
        format["nonce"] = f"Nonce: {block_header.nonce}"
        date = self.blockchain_history[block_height]["date"]
        format["date"] = f"Timestamp: {date}"
        txs = self.tx_db.get_txs_by_hash(block.tx_hash_arr)
        format["txs"] = []
        for key in txs:
            format["txs"].append(self.get_tx_format(txs[key]))
        format["Err"] = ""
        return format
    
    def get_block_history(self):
        """Returns the whole history of the chain, that is who added the block to the chain
        and the number of the block that was added
        """
        messages = []
        for history in self.blockchain_history:
            author = history["author"]
            block_height = history["height"]
            message = f"The miner {author} added the block #{block_height} to the chain"
            messages.append(message)
        if not messages:
            message = f"The blockchain is empty"
            messages.append(message)
        return messages
