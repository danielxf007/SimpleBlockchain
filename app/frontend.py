from app.backend import Backend
from util.printing import print_messages, print_tx_inputs, print_tx_input_index_utxo_value, print_block, print_utxos_value
import argparse


class Frontend:
    """Uses the backend functions and defines methods to interact with the application
    using console commands
    """

    def __init__(self):
        """Initializes the class' attributes"""
        self.parser = argparse.ArgumentParser(description='Welcome to Basic Blockchain')
        self.commands = self.parser.add_argument_group('App Commands')
        self.wallet_commands = self.parser.add_argument_group('Wallet Commands')
        self.create_commands()
        self.create_wallet_commands()
        self.backend = Backend()
        self.app_state = "main_menu"
        self.connected_user_name = ""
        
    def create_commands(self):
        """Creates the commands the user would be able to use to interact with the app"""
        self.commands.add_argument('--init', action='store_true',
                    help='Satoshi initializes the system by mining the genesis block')
        self.commands.add_argument('--download_lock_scripts', type=str,
                    dest='dir_path', action='store', 
                    help='Downloads the locking scripts of utxos to the given directory')
        self.commands.add_argument('--wallet', type=str, dest='wallet_user_name',
                    help='Creates a wallet and associates a user name to it')
        self.commands.add_argument('--wallet_r', type=int, dest='n_r_wallets',
                    help='Allows you to create n random wallets')
        self.commands.add_argument('--connect_wallet', type=str, dest='connect_wallet_user',
                    help='Connects you to the user wallet')
        self.commands.add_argument('--block', type=int, dest='h',
            help='Allows you to watch the details of the block at height h')
        """
        self.commands.add_argument('--get_n_wallets', action='store_true',
                    help='Allows you to see how many wallets are in the system')
        self.commands.add_argument('--list_wallets', action='store_true',
                    help='Allows you to see all the wallets in the system')
        self.commands.add_argument('--miner', type=str, dest='miner_user',
                    help='Allows your user to become a miner')
        self.commands.add_argument('--miner_r', type=int, dest='n_r_miners',
                    help='N random users will become miners')
        self.commands.add_argument('--list_miners', action='store_true',
                    help='Allows you to see all the miners')
        self.commands.add_argument('--fee', action='store_true',
                    help='Gets the current transaction fee')
        self.commands.add_argument('--mining', action='store_true',
            help='Some pending transactions are validated')"""
        self.commands.add_argument('--exit', action='store_true',
                    help='Stops the program')
    
    def create_wallet_commands(self):
        """Creates the commands the user would to interact with the wallet"""
        self.wallet_commands.add_argument('--get_keys', action='store_true',
                    help='Shows your private and public keys')
        self.wallet_commands.add_argument('--create_tx_input', type=str, nargs=3,
        dest='create_tx_input_args', action='store',
        help='Creates a tx input that would be used by the wallet on a transaction, it expects the tx hash, utxo index and unlock script')
        self.wallet_commands.add_argument('--remove_tx_input', type=int,
        dest='remove_tx_input_index', action='store',
        help='Removes a tx input at an index from the ones that will be used by the wallet on a transaction')
        self.wallet_commands.add_argument('--get_tx_inputs', action='store_true',
        help='Shows the tx inputs that will be used by the wallet on a transaction')
        self.wallet_commands.add_argument('--get_available_utxos', action='store_true',
        help='Shows the value of the utxos unlocked using the tx input')
        self.wallet_commands.add_argument('--create_utxo', type=str, nargs=2,
        dest='create_utxo_args', action='store',
        help='Creates a utxo that would be used as output by the wallet on a transaction')
        self.wallet_commands.add_argument('--remove_utxo', type=int,
        dest='remove_utxo_index', action='store',
        help='Removes a utxo at an index from the ones that will be used by the wallet on a transaction, it expects the value on BTC and the lock script')
        self.wallet_commands.add_argument('--get_utxos', action='store_true',
        help='Shows the utxos that will be used by the wallet on a transaction')
        self.wallet_commands.add_argument('--fee', action='store_true',
                    help='Gets the current transaction fee')
        self.wallet_commands.add_argument('--log_out', action='store_true',
                    help='Takes you back to the main commands')
        
    def interact(self):
        """This method is used a program loop, it will parse each command and will end
        the loop when the exit command is given
        """
        print("Welcome to Simple Blockchain")
        while True:
            try:
                if self.app_state == "main_menu":
                    args = self.parser.parse_args(input('Enter Command: ').split())
                    print()
                    if args.init:
                        messages = self.backend.init_system()
                        print_messages(messages)
                    elif args.dir_path:
                        message = self.backend.download_lock_scripts(args.dir_path)
                        print(message)
                    elif args.wallet_user_name:
                        message = self.backend.create_wallet(args.user_name).values()
                        print(message)
                    elif args.n_r_wallets:
                        messages = self.backend.create_random_wallets(args.n_r_wallets)
                        print_messages(messages)
                    elif args.connect_wallet_user:
                        success, _ = self.backend.connect_to_wallet(
                            args.connect_wallet_user)
                        if success:
                            self.app_state = "wallet_menu"
                            self.connected_user_name = args.connect_wallet_user
                        continue
                    elif args.h != None:
                        result = self.backend.get_block(args.h)
                        if result["success"]:
                            print_block(result["block"])
                        else:
                            print(result["message"])
                    elif args.exit:
                        print('See ya!')
                        break
                    else:
                        print('Command not found')
                    """
                    elif args.get_n_wallets:
                        message = self.backend.get_n_wallets()
                        print(message)
                    elif args.list_wallets:
                        messages = self.backend.get_wallets()
                        print_messages(messages)
                    elif args.miner_user:
                        message = self.backend.create_miner(args.miner_user)
                        print(message)
                    elif args.n_r_miners:
                        messages = self.backend.create_miner_r(args.n_r_miners)
                        print_messages(messages)
                    elif args.list_miners:
                        messages = self.backend.get_miners()
                        print_messages(messages)
                    elif args.fee:
                        message = self.backend.get_fee()
                        print(message)
                    elif args.mining:
                        message = self.backend.mining_block()
                        print(message)"""
                elif self.app_state == "wallet_menu":
                    args = self.parser.parse_args(
                        input(f"{self.connected_user_name}> ").split())
                    print()
                    if args.get_keys:
                        message = self.backend.get_wallet_keys()
                        print(message)
                    elif args.create_tx_input_args:
                        message = self.backend.create_tx_input(*args.create_tx_input_args)
                        print(message)
                    elif args.remove_tx_input_index != None:
                        message = self.backend.remove_tx_input(args.remove_tx_input_index)
                        print(message)
                    elif args.get_tx_inputs:
                        print_tx_inputs(self.backend.get_tx_inputs())
                    elif args.get_available_utxos:
                        print_tx_input_index_utxo_value(self.backend.get_available_utxos())
                    elif args.create_utxo_args:
                        message = self.backend.create_utxo(*args.create_utxo_args)
                        print(message)
                    elif args.remove_utxo_index:
                        message = self.backend.remove_utxo(args.remove_utxo_index)
                        print(message)
                    elif args.get_utxos:
                        print_utxos_value(self.backend.get_created_utxos())
                    elif args.fee:
                        print(self.backend.get_fee())
                    elif args.log_out:
                        self.app_state = "main_menu"
                        self.connected_wallet_user = ""
                        self.backend.log_out()
                    else:
                        print('Command not found')
            except Exception as e:
                print(e)
            print()