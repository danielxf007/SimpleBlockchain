# Simple Blockchain

This program is a simple simulation of a blockchain, you can interact with it using console commands

## Commands:

![alt text](./images/commands.png)

## System initialization

![alt text](./images/command_init.png)

## Genesis Block:
![alt text](./images/command_block.png)

## Wallet creation

![alt text](./images/command_wallet.png)

![alt text](./images/command_wallet_r.png)

## Checking a wallet's balance

![alt text](./images/command_wallet_balance.png)

## Checking a wallet's utxos

![alt text](./images/command_wallet_utxo.png)

### Note:

If you want to know more about utxos visit: https://github.com/bitcoinbook/bitcoinbook/blob/develop/ch06.asciidoc

## Getting the number of wallets created

![alt text](./images/command_get_n_wallets.png)

## Listing the wallets

![alt text](./images/command_list_wallets.png)

## Miner creation

![alt text](./images/command_miner.png)

![alt text](./images/command_miner_r.png)

## Listing the miners

![alt text](./images/command_list_miners.png)

## Checking the transaction fee

![alt text](./images/command_fee.png)

### Note:

The transaction fee changes everytime a block is added to the chain

## Transaction making

![alt text](./images/command_transfer.png)

### Note:

The arguments are: the user name of the one making the transaction, the beneficiary, the amount of btc and a third user that will get the change of the transaction (it can be any user who has a wallet)

![alt text](./images/command_transfer_r.png)

## Mining a block

![alt text](./images/command_mining.png)

## Displaying a block's data

![alt text](./images/command_block1.png)

### Note:

The difficulty is the number of binary zeroes that must be found in a hash digest

## Getting the chain's history

![alt text](./images/command_history.png)

## Note:

Run the program using **python3 main.py**

You can see the commands anytime using the command: **--help**