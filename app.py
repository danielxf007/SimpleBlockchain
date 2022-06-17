import argparse
import hashlib
import pickle
import random
from miner import Miner
from wallet import Wallet
from data_bases import TXDB, UTXODB, MerkleDB

class App:

    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Welcome to Basic Blockchain you can use the commands: ')
        self.commands = self.parser.add_argument_group('App Commands')
        self.wallets = {}
        self.miners = {}
        self.names_file_path = '/home/daniel/Documents/simple_blockchain/names.txt'
        self.n_names = 18238
        self.pending_tx_db = TXDB()
        self.valid_tx_db = TXDB()
        self.utxo_db = UTXODB()
        self.merkle_db = MerkleDB()
        self.last_block_hash = hashlib.sha256('0'.encode()).hexdigest()
        self.block_chain = {self.last_block_hash: None}
    
    def create_commands(self):
        self.commands.add_argument('--wallet', type=str, dest='user_name',
                    help='Allows you to create a wallet given a user name')
        self.commands.add_argument('--wallet_r', type=int, dest='n_r_wallets',
                    help='Allows you to create n random wallets')
        self.commands.add_argument('--get_n_wallets', action='store_true',
                    help='Allows you to see how many wallets are in the system')
        self.commands.add_argument('--list_wallets', action='store_true',
                    help='Allows you to see all the wallets in the system')
        self.commands.add_argument('--miner', type=str, dest='miner_user',
                    help='Allows your user to mine blocks')
        self.commands.add_argument('--list_miners', action='store_true',
                    help='Allows you to see all the miners')       
        self.commands.add_argument('--exit', action='store_true',
                    help='Stops the program')

    def create_wallet(self, user_name):
        if not user_name in self.wallets.keys():
            pk = hashlib.sha256(user_name.encode()).hexdigest()
            wallet = Wallet(pk)
            self.wallets[user_name] = wallet
            print(f"{user_name} your wallet was created!")
        else:
            print(f"Error: The user {user_name} has already created a wallet")
    
    def create_random_wallets(self, n_r_wallets):
        names_file = open(self.names_file_path, 'r')
        for _ in range(n_r_wallets):
            names_file.seek(0, 0)
            line = random.randint(0, self.n_names)
            while line:
                user_name = names_file.readline().strip()
                line-=1
            if not user_name in self.wallets.keys():
                pk = hashlib.sha256(user_name.encode()).hexdigest()
                wallet = Wallet(pk)
                self.wallets[user_name] = wallet
            else:
                number = str(random.randint())
                new_user_name = user_name+number
                while new_user_name in self.wallets.keys():
                    number = str(random.randint())
                    new_user_name = user_name+number
                pk = hashlib.sha256(new_user_name.encode()).hexdigest()
                wallet = Wallet(pk)
                self.wallets[user_name] = wallet
        names_file.close()

    def print_n_wallets(self):
        print(len(self.wallets.keys()))
    
    def print_wallets(self):
        for user_name in self.wallets.keys():
            print(f"Wallet user: {user_name}, Wallet Addr: {self.wallets[user_name].pk}")
    
    def create_miner(self, user_name):
        if not user_name in self.miners.keys():
            if user_name in self.wallets.keys():
                wallet = self.wallets[user_name]
                self.miners[user_name] = Miner(wallet.pk)
                print(f"{user_name} you can now mine blocks!")
            else:
                print(f"{user_name} has no wallet")
        else:
            print(f"Error {user_name} can mine blocks already!")
    
    def print_miners(self):
        for user_name in self.miners.keys():
            print(f"{user_name}")
    
    def hash_txs(self, txs):
        hashed_txs = []
        for tx in txs:
            hashed_txs.append(hashlib.sha256(pickle.dumps(tx)).hexdigest())
        return hashed_txs
        
    def mining_block(self):
        miner_keys = self.miners.keys()
        miner_key = miner_keys[random.randint(0, len(miner_keys)-1)]
        miner: Miner = self.miners[miner_key]
        txs = self.pending_tx_db.get_n_txs(miner.n_txs_request())
        if txs:
            txs = list(filter(lambda tx: miner.validate_tx(self.valid_tx_db, tx), txs))
        coin_base_tx = miner.create_coin_base_tx(self.valid_tx_db, txs)
        txs+=[coin_base_tx]+txs
        hashed_txs = self.hash_txs(txs)
        difficulty = random.randint(1, 4)
        miner.create_block(self.last_block_hash, hashed_txs, difficulty)
        block = miner.mining_block()
        self.last_block_hash = hashlib.sha256(pickle.dumps(block)).hexdigest()
        self.block_chain[self.last_block_hash] = block
        print(f"The miner: {miner_key} added the block: {self.last_block_hash}")

    def init_blockchain(self):
        self.create_wallet('Satoshi')
        self.create_miner('Satoshi')
    def interact(self):
        while True:
            try:
                args = self.parser.parse_args(input('Enter Command: ').split())
                print(args)
                if args.user_name:
                    self.create_wallet(args.user_name)
                elif args.n_r_wallets:
                    self.create_random_wallets(args.n_r_wallets)
                elif args.get_n_wallets:
                    self.print_n_wallets()
                elif args.list_wallets:
                    self.print_wallets()
                elif args.miner_user:
                    self.create_miner(args.miner_user)
                elif args.list_miners:
                    self.print_miners()
                elif args.exit:
                    print('See ya!')
                    break
                else:
                    print('Command not found')
            except:
                pass

app = App()
app.create_commands()

app.interact()