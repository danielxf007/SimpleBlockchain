from core.data_bases.utxo_reference_db import UTXOReferenceDB
from core.blockchain import Blockchain
from core.wallet import Wallet
from core.miner import Miner
from util.conversions import btc_to_satoshi
from util.conversions import satoshi_to_btc
import random
from ecdsa import SigningKey

class Backend:
    """This classes uses the core elements and has the global blockchain and the global
    utxo reference db which is used to make transactions easier to create.
    
    The whole system uses satoshi with eight decimals of precision, values smaller
    than 1/10^8 are considered to be 0
    """

    def __init__(self):
        """Initializes the class' attributes"""
        self.wallets = {}
        self.miners = {}
        self.names_file_path = "./data/names.txt"
        self.n_names = 18238
        self.pending_txs = []
        self.blockchain = Blockchain([])
        self.utxo_reference_db = UTXOReferenceDB([])
        self.current_fee = random.randint(10**2, 10**3)
        self.connected_wallet: Wallet = None
        self.initialized = False
        self.init_system()
    
    def init_system(self):
        """Initializes the system by creating a user called Satoshi and mining
        the genesis block, it also returns a list of messages about the operations
        """
        if self.initialized:
            return ["The system has been already initialized"]
        user_name = "Satoshi"
        self.create_wallet(user_name)["message"]
        self.create_miner(user_name)
        self.initialized = True
        print(self.mining_block())
    
    def download_lock_scripts(self, dir_path):
        """Downloads the lock scripts from the utxos on the utxo reference database,
        the script has comments were it specifies the tx hash of the tx which has the utxo,
        an utxo index

        dir_path -- it is the path of the directory where the scripts will be downloaded. 
        """
        generic_name = "lock_script"
        index = 1
        extension = ".s"
        message = "The scripts were downloaded"
        try:
            for reference in self.utxo_reference_db.get_references():
                tx_hash = reference["tx_hash"]
                utxo_index = reference["utxo_index"]
                utxo = self.blockchain.get_utxo(tx_hash, utxo_index)
                lock_script = f"# TX Hash: {tx_hash}\n# UTXO Index: {utxo_index}\n# Value: {utxo.value}\n# Script\n"
                lock_script += utxo.lock_script
                lock_script_file_path = dir_path + generic_name + str(index) + extension
                with open(lock_script_file_path, 'w') as lock_file:
                    lock_file.write(lock_script)
                index += 1
        except Exception as e:
            message = f"Something went wrong {e}"
        return message

    def create_wallet(self, user_name):
        """Returns a dictionary with a sucess flags and a message

        Keyword arguments:
        user_name -- it is the name associated to the wallet
        """
        if not user_name in self.wallets.keys():
            private_key = SigningKey.generate()
            public_key = private_key.verifying_key
            blockchain_state = self.blockchain.get_blocks().copy()
            utxo_references = self.utxo_reference_db.get_references().copy()
            wallet = Wallet(private_key, public_key, blockchain_state, utxo_references)
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
    
    def connect_to_wallet(self, user_name):
        """Given an user name it connects the user with the wallet

        Keyword arguments:
        user_name -- it is the name of an already registered user
        """
        if user_name in self.wallets.keys():
            self.connected_wallet =  self.wallets[user_name]
            return {
            "success": True,
            "message": f"Hello {user_name}"}
        return {
            "success": False,
            "message": f"{user_name} has no wallet"}
    
    def log_out(self):
        """Logs out from the wallet"""
        if self.connected_wallet:
            self.connected_wallet = None

    def get_wallet_keys(self):
        """Returns a message containing the 
        private and public key associated of a wallet

        The user has to be connected to their to use this method

        Keyword arguments:
        user_name -- it is the name associated to the wallet
        """
        private_key = self.connected_wallet.get_private_key()
        public_key = self.connected_wallet.get_public_key()
        return f"Private key: {private_key}\nPublic key: {public_key}"
    
    def create_tx_input(self, tx_hash, utxo_index, unlock_script_path):
        """The current connected wallet creates a tx input which would be used
        to spend the referenced utxo and
        returns a message indicating the result of the operation.
        
        Keyword arguments:
        tx_hash -- it is the hash of the tx where the utxo is stored
        utxo_index -- it is a string which holds the index of the utxo within the transaction
        unlock_script_path -- it is the script that unlocks the utxo
        """
        result = self.connected_wallet.create_tx_input(tx_hash, int(utxo_index), unlock_script_path)
        if result["success"]:
            message = "The Transaction input was created"
        else:    
            message = result["err"]
        return message

    def remove_tx_input(self, index):
        """The current connected wallet removes a tx input from the ones used to make a 
        transaction and
        returns a message indicating the result of the operation.
        
        Keyword arguments:
        index -- it is the index of the tx input
        """
        result = self.connected_wallet.remove_tx_input(index)
        if result["success"]:
            message = f"The Transaction input at {index} was deleted"
        else:    
            message = result["err"]
        return message
    
    def get_tx_inputs(self):
        """Gets the tx inputs which would be used
        to spend the referenced utxo from the current connected wallet
        """
        return self.connected_wallet.get_tx_inputs()
    
    def get_available_utxos(self):
        """The connected wallet gets the utxos that the user unlocked
        with the transaction input"""
        return self.connected_wallet.get_available_utxos()
    
    def create_utxo(self, value, lock_script_path):
        """A connected wallet can create a unspent transaction output and adds it to the
        current utxos that will be used to make a transaction and
        returns a message indicating the result of the operation.

        The value is on BTC but it gets convert to satoshi.

        Keyword arguments:
        value -- it is the value on BTC of the utxo.
        lock_script_path -- it is the BTC script that will have to be solved by a wallet if
        they want to spend the utxo.
        """
        value_satoshi = btc_to_satoshi(float(value))
        result = self.connected_wallet.create_utxo(value_satoshi, lock_script_path)
        if result["success"]:
            message = f"The Unspent Transaction Output was created"
        else:    
            message = result["err"]
        return message
    
    def remove_utxo(self, index):
        """Removes a utxo from the current utxos that will be used to make a transaction and
        returns a message indicating the result of the operation.
        Keyword arguments:
        index -- it is the number of the utxo
        """
        result = self.connected_wallet.remove_utxo(index)
        if result["success"]:
            message = f"The Unspent Transaction Output at {index} was deleted"
        else:    
            message = result["err"]
        return message
    
    def get_created_utxos(self):
        """Gets the current utxos that will be used to make a transaction"""
        return self.connected_wallet.get_utxos()

    def get_fee(self):
        """Gets a message with the current transaction fee on BTC"""
        return f"The current transaction fee is: {satoshi_to_btc(self.current_fee):.8f} BTC"

    def create_tx(self):
        """A connected wallet creates a transaction using the tx inputs and utxos created 
        beforehand.

        The list of tx inputs and utxos will be cleared after creating the transaction
        """
        result = self.connected_wallet.create_tx(self.current_fee)
        if result["success"]:
            self.pending_txs.append(result["tx"])
            message = "The transaction was created wait until it's validated"
        else:
            message = result["err"]
        return message

    def get_wallets(self):
        """Gets all the wallets in the system and returns an array of formatted messages"""
        messages = []
        for user_name in self.wallets.keys():
            message = f"Wallet user: {user_name}"
            messages.append(message)
        return messages

    def create_miner(self, user_name):
        """Created a miner and returns a formatted message about the creation

        Keyword arguments:
        user_name -- it is the name of a user who has a wallet
        """
        if user_name in self.wallets.keys():
            if not user_name in self.miners.keys():
                wallet = self.wallets[user_name]
                blockchain_state = self.blockchain.get_blocks().copy()
                utxo_references = self.utxo_reference_db.get_references().copy()
                miner = Miner(wallet.get_public_key(), blockchain_state, utxo_references)
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

    def choose_miner(self):
        """Returns a randomly selected miner who will mine the block"""
        miner_keys = list(self.miners.keys())
        miner_key = miner_keys[random.randint(0, len(miner_keys)-1)]
        return miner_key
    
    def update_utxo_references(self, miner):
        """Updates the global unspent transaction
        outputs database by storing a copy of the miner's reference
        after validating the transactions

        Keyword arguments:
        miner -- it is the miner who added the new block
        """
        references = miner.get_utxo_references().copy()
        self.utxo_reference_db.set_references(references)

    def update_wallets_utxo_references(self):
        """Updates the references to unspent transaction
        outputs database by storing a copy of the current state of the global state of the
        databases
        """
        for key in self.wallets.keys():
            wallet = self.wallets[key]
            wallet.set_utxo_references(self.utxo_reference_db.get_references().copy())
    
    def update_wallets_blockchain_state(self):
        for key in self.wallets.keys():
            wallet = self.wallets[key]
            wallet.set_blocks(self.blockchain.get_blocks().copy())

    def update_miners_utxo_references(self):
        """Updates the trasaction database and the references to unspent transaction
        outputs database by storing a copy of the current state of the global state of these
        databases
        """
        for key in self.miners.keys():
            miner = self.miners[key]
            miner.set_utxo_references(self.utxo_reference_db.get_references().copy())

    def update_miners_blockchain_state(self):
        """Updates the trasaction database and the references to unspent transaction
        outputs database by storing a copy of the current state of the global state of these
        databases
        """
        for key in self.miners.keys():
            miner = self.miners[key]
            miner.set_blocks(self.blockchain.get_blocks().copy())
    
    def update_fee(self):
        """Updates the fee that must be payed for a transaction

        The fee unit is satoshi
        """
        self.current_fee = random.randint(10**2, 10**3)

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
        block = miner.mining_block(txs, difficulty)
        self.blockchain.add(block)
        self.update_utxo_references(miner)
        self.update_wallets_utxo_references()
        self.update_wallets_blockchain_state()
        self.update_miners_utxo_references()
        self.update_miners_blockchain_state()
        self.update_fee()
        self.pending_txs.clear()
        return f"The miner {miner_key} added the block #{self.blockchain.get_height()} to the chain"
    
    def get_block(self, block_height):
        """Returns a a dictionary with a format which will be used to print the
        data in the block

        Keyword arguments:
        block_height -- it is the index where the block can be found
        """
        block = self.blockchain.get_block(block_height)
        if block:
            return {"success": True, "message": "", "block": block}       
        return {"success": False, "message": "Block not found", "block": block}
