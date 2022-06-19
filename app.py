import argparse
import hashlib
import pickle
import random
from block import Block, BlockHeader
from miner import Miner
from transactions import TX, UTXO
from wallet import Wallet
from data_bases import TXDB, UTXODB, MerkleDB
from util import Util

class App:

    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Welcome to Basic Blockchain you can use the commands: ')
        self.commands = self.parser.add_argument_group('App Commands')
        self.wallets = {}
        self.miners = {}
        self.names_file_path = '/home/daniel/Documents/simple_blockchain/names.txt'
        self.n_names = 18238
        self.pending_txs = []
        self.valid_tx_db = TXDB()
        self.utxo_db = UTXODB()
        self.merkle_db = MerkleDB()
        self.last_block_hash = hashlib.sha256('0'.encode()).hexdigest()
        self.blockchain = {self.last_block_hash: None}
        self.blockchain_history = []
        self.util = Util()
    
    def create_commands(self):
        self.commands.add_argument('--wallet', type=str, dest='user_name',
                    help='Allows you to create a wallet given a user name')
        self.commands.add_argument('--wallet_r', type=int, dest='n_r_wallets',
                    help='Allows you to create n random wallets')
        self.commands.add_argument('--wallet_balance', type=str, dest='wallet_user',
                    help='Allows you to see how much BTC a wallet has')
        self.commands.add_argument('--get_n_wallets', action='store_true',
                    help='Allows you to see how many wallets are in the system')
        self.commands.add_argument('--list_wallets', action='store_true',
                    help='Allows you to see all the wallets in the system')
        self.commands.add_argument('--transfer', nargs=4, dest='transfer_args',
                    help='Allows your to transfer btc from a wallet to another')
        self.commands.add_argument('--transfer_r', type=int, dest='n_r_txs',
                    help='Satoshi transfer random btc to random wallets')
        self.commands.add_argument('--miner', type=str, dest='miner_user',
                    help='Allows your user to mine blocks')
        self.commands.add_argument('--list_miners', action='store_true',
                    help='Allows you to see all the miners')
        self.commands.add_argument('--mining', action='store_true',
            help='Allows you to validate pending txs')
        self.commands.add_argument('--history', action='store_true',
            help='Allows you to watch the miner and the block he added to the chain')
        self.commands.add_argument('--block', type=str, dest='block_hash',
            help='Allows you to watch the details of a block')           
        self.commands.add_argument('--exit', action='store_true',
                    help='Stops the program')

    def create_wallet(self, user_name):
        if not user_name in self.wallets.keys():
            pk = hashlib.sha256(user_name.encode()).hexdigest()
            wallet = Wallet(pk, self.valid_tx_db.txs.copy())
            self.wallets[user_name] = wallet
            print(f"{user_name} your wallet was created the address is: {pk}")
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
                self.create_wallet(user_name)
            else:
                number = str(random.randint(0, 1000))
                new_user_name = user_name+number
                while new_user_name in self.wallets.keys():
                    number = str(random.randint())
                    new_user_name = user_name+number
                self.create_wallet(new_user_name)
        names_file.close()
    
    def get_wallet_balance(self, user_name):
        balance = 0
        if user_name in self.wallets.keys():
            wallet = self.wallets[user_name]
            balance = wallet.get_wallet_balance()
            print(f"{user_name} has {self.util.satoshi_to_btc(balance):.8f} BTC") 
        else:
            print('Error {user_name} has no wallet')
    
    def print_n_wallets(self):
        print(len(self.wallets.keys()))
    
    def print_wallets(self):
        for user_name in self.wallets.keys():
            print(f"Wallet user: {user_name}, Wallet Addr: {self.wallets[user_name].pk}")
    
    def transfer(self, from_wallet, to_wallet, amount, fee):
        if not from_wallet in self.wallets.keys():
            print(f"The user {from_wallet} has no wallet")
            return
        elif not to_wallet in self.wallets.keys():
            print(f"The user {to_wallet} has no wallet")
            return
        source_wallet = self.wallets[from_wallet]
        dest_wallet = self.wallets[to_wallet]
        tx = source_wallet.create_tx(
            dest_wallet.pk,
            self.util.btc_to_satoshi(float(amount)),
            self.util.btc_to_satoshi(float(fee)))
        if tx:
            self.pending_txs.append(tx)
            print(f"{from_wallet} your transaction is waiting to be approved")
        else:
            print(f"Error {from_wallet} you don't have enough balance")
    
    def make_rdm_txs(self, n):
        wallet = self.wallets['Satoshi']
        balance = wallet.get_wallet_balance()
        if balance >= self.util.btc_to_satoshi(10**-5):
            targets = list(self.wallets.keys())
            for _ in range(n):
                target = targets[random.randint(0, len(targets)-1)]
                self.transfer('Satoshi', target, random.uniform(10**-6, 10**-5), random.uniform(0, 10**-7))
            print('Satoshi has made the transfers!')
        else:
            print('Sorry Satoshi cannot make more transfers')

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
    
    def print_history(self):
        for history in self.blockchain_history:
            print(f"The miner {history['miner']} added the block: {history['block']}")
    
    def print_block_header(self, header):
        print(f"Prev Hash: {header.prev_hash}")
        print(f"Merkle Root: {header.root_hash}")
        print(f"Difficulty: {header.difficulty}")
        print(f"Nonce: {header.nonce}")
    
    def get_txs(self, hash_arr):
        return list(map(lambda h: self.valid_tx_db.get_tx(h), hash_arr))
    
    def get_user_name(self, pk):
        user_name = ""
        for key in self.wallets.keys():
            wallet = self.wallets[key]
            if pk == wallet.pk:
                user_name = key
        return user_name
    
    def print_tx(self, tx):
        from_user = self.get_user_name(tx.creator)
        utxo = tx.get_utxo_arr()[1]
        to_user = self.get_user_name(utxo.pk)
        value = self.util.satoshi_to_btc(utxo.value)
        if not tx.coin_base:
            print(f"{from_user} transfered {value:.8f} BTC to {to_user}")
        else:
            print(f"{to_user} got rewarded with {value:.8f} BTC for mining")
    
    def print_txs(self, txs):
        for tx in txs:
            self.print_tx(tx)
    
    def print_line(self, lenght):
        line = ""
        for _ in range(lenght):
            line+='#'
        print(line)

    def print_block(self, block_hash):
        if block_hash in self.blockchain.keys():
            block = self.blockchain[block_hash]
            if block:
                miner_user = ""
                for history in self.blockchain_history:
                    if history['block'] == block_hash:
                        miner_user = history['miner']
                        break
                header = block.header
                self.print_line(16)
                print(f"Miner: {miner_user}")
                self.print_block_header(header)
                txs = self.get_txs(block.tx_hash_arr)
                self.print_txs(txs)
                self.print_line(16)
            
    def hash_txs(self, txs):
        hashed_txs = []
        for tx in txs:
            hashed_txs.append(hashlib.sha256(pickle.dumps(tx)).hexdigest())
        return hashed_txs
    
    def update_wallets(self):
        for key in self.wallets.keys():
            wallet:Wallet = self.wallets[key]
            utxos = self.utxo_db.get_utxos(wallet.pk)
            wallet.tx_db.txs = self.valid_tx_db.txs.copy()
            wallet.available_utxo_db.data = utxos.copy()
        
    def mining_block(self):
        miner_keys = list(self.miners.keys())
        miner_key = miner_keys[random.randint(0, len(miner_keys)-1)]
        miner: Miner = self.miners[miner_key]
        n_txs = miner.n_txs_request()
        if n_txs < len(self.pending_txs):
            txs = self.pending_txs[:n_txs]
        else:
            txs = self.pending_txs
        hashed_txs = self.hash_txs(txs)
        self.valid_tx_db.add_txs(txs, hashed_txs)
        coin_base_tx = miner.create_coin_base_tx(self.valid_tx_db, txs)
        coin_base_hash = hashlib.sha256(pickle.dumps(coin_base_tx)).hexdigest()
        self.valid_tx_db.add_tx(coin_base_hash, coin_base_tx)
        txs = [coin_base_tx]+txs
        hashed_txs = [coin_base_hash]+hashed_txs
        difficulty = random.randint(1, 16)
        miner.create_block(self.last_block_hash, hashed_txs, difficulty)
        block = miner.mining_block()
        self.last_block_hash = hashlib.sha256(pickle.dumps(block)).hexdigest()
        self.blockchain[self.last_block_hash] = block
        for i in range(len(txs)):
            self.utxo_db.add_utxos(hashed_txs[i], txs[i].get_utxo_arr())
        for i in range(1, len(txs)):
            self.utxo_db.remove_utxos(txs[i].creator, txs[i].get_tx_in_arr())
        self.update_wallets()
        self.pending_txs.clear()
        self.blockchain_history.append({'miner': miner_key, 'block': self.last_block_hash})
        print(f"The miner {miner_key} added the block: {self.last_block_hash}")

    def init_blockchain(self):
        self.create_wallet('Satoshi')
        self.create_miner('Satoshi')
        self.mining_block()

    def interact(self):
        while True:
            try:
                args = self.parser.parse_args(input('Enter Command: ').split())
                print()
                if args.user_name:
                    self.create_wallet(args.user_name)
                elif args.n_r_wallets:
                    self.create_random_wallets(args.n_r_wallets)
                elif args.wallet_user:
                    self.get_wallet_balance(args.wallet_user)
                elif args.get_n_wallets:
                    self.print_n_wallets()
                elif args.list_wallets:
                    self.print_wallets()
                elif args.transfer_args:
                    self.transfer(*args.transfer_args)
                elif args.n_r_txs:
                    self.make_rdm_txs(args.n_r_txs)
                elif args.miner_user:
                    self.create_miner(args.miner_user)
                elif args.list_miners:
                    self.print_miners()
                elif args.mining:
                    self.mining_block()
                elif args.history:
                    self.print_history()
                elif args.block_hash:
                    self.print_block(args.block_hash)
                elif args.exit:
                    print('See ya!')
                    break
                else:
                    print('Command not found')
            except:
                pass
            print()

app = App()
app.create_commands()
app.init_blockchain()
app.interact()