from app.backend import Backend
from util.printing import print_messages, print_block
import argparse


class Frontend:
    """Uses the backend functions and defines methods to interact with the application
    using console commands
    """

    def __init__(self):
        """Initializes the class' attributes"""
        self.parser = argparse.ArgumentParser(description='Welcome to Basic Blockchain you can use the commands: ')
        self.commands = self.parser.add_argument_group('App Commands')
        self.create_commands()
        self.backend = Backend()

    def create_commands(self):
        """Creates the commands the user would be able to use to interact with the app"""
        self.commands.add_argument('--init', action='store_true',
                    help='Satoshi initializes the system by mining the genesis block')
        self.commands.add_argument('--wallet', type=str, dest='user_name',
                    help='Allows you to create a wallet given a user name')
        self.commands.add_argument('--wallet_r', type=int, dest='n_r_wallets',
                    help='Allows you to create n random wallets')
        self.commands.add_argument('--wallet_balance', type=str, dest='wallet_user',
                    help='Allows you to see how much BTC a wallet has')
        self.commands.add_argument('--wallet_utxos', type=str, dest='wallet_user_utxo',
                    help='Shows the unspent transactions outputs the wallet user can spend')
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
        self.commands.add_argument('--transfer', nargs='*', dest='trans_args', action='store',
                                    help='Allows you to transfer btc the arguments are:\
                                    Your user, the user you want to transfer to,\
                                    the amount, the user who will get the change')
        self.commands.add_argument('--transfer_r', type=int, dest='n_r_txs',
            help='Satoshi transfers random btc to random wallets')
        self.commands.add_argument('--mining', action='store_true',
            help='Some pending transactions are validated')
        self.commands.add_argument('--block', type=int, dest='h',
            help='Allows you to watch the details of the block at height h')
        self.commands.add_argument('--history', action='store_true',
            help='Lists the miner and the block number he added to the chain')
        self.commands.add_argument('--exit', action='store_true',
                    help='Stops the program')
        
    def interact(self):
        """This method is used a program loop, it will parse each command and will end
        the loop when the exit command is given
        """
        print("Welcome to Simple Blockchain")
        while True:
            try:
                args = self.parser.parse_args(input('Enter Command: ').split())
                print()
                if args.init:
                    messages = self.backend.init_system()
                    print_messages(messages)
                elif args.user_name:
                    _, message = self.backend.create_wallet(args.user_name).values()
                    print(message)
                elif args.n_r_wallets:
                    messages = self.backend.create_random_wallets(args.n_r_wallets)
                    print_messages(messages)
                elif args.wallet_user:
                    message = self.backend.get_wallet_balance(args.wallet_user)
                    print(message)
                elif args.wallet_user_utxo:
                    user_name = args.wallet_user_utxo
                    messages = self.backend.get_wallet_available_utxo_values(user_name)
                    print_messages(messages)
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
                elif args.trans_args:
                    if(len(args.trans_args) == 4):
                        _, message = self.backend.transfer(*args.trans_args).values()
                        print(message)
                    else:
                        print("Not enough arguments")
                elif args.n_r_txs:
                    message = self.backend.make_r_txs(args.n_r_txs)
                    print(message)
                elif args.mining:
                    message = self.backend.mining_block()
                    print(message)
                elif args.h != None:
                    block_format = self.backend.get_block_format(args.h)
                    print_block(block_format)
                elif args.history:
                    messages = self.backend.get_block_history()
                    print_messages(messages)
                elif args.exit:
                    print('See ya!')
                    break
                else:
                    print('Command not found')
            except:
                pass
            print()