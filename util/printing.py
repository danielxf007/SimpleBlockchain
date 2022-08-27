from util.conversions import satoshi_to_btc

def print_messages(messages):
    """Prints the given messages

    Keyword arguments:
    messages -- it is an array of strings
    """
    for message in messages:
        print(message)

def print_tx_inputs(tx_inputs):
    index = 1
    for tx_input in tx_inputs:
        print(f"{index}.TX Input:")
        print(" "*4, f"TX Hash: {tx_input.tx_hash}")
        print(" "*4, f"UTXO Index: {tx_input.utxo_index}")
        print(" "*4, f"Unlock Script: {tx_input.unlock_script}")
        index +=1

def print_utxos(utxos):
    index = 1
    for utxo in utxos:
        print(f"{index}.Unspent Transaction Output:")
        print(" "*4, f"Value: {satoshi_to_btc(utxo.value)} BTC")
        print(" "*4, f"Lock Script: {utxo.lock_script}")
        index += 1
    
def print_tx_input_index_utxo_value(utxos):
    index = 1
    for utxo in utxos:
        print(f"The UTXO unlocked by the tx input at {index} is worth {satoshi_to_btc(utxo.value)} BTC")
        index +=1

def print_tx(tx):
    """Prints a trasaction data using a format

    Keyword arguments:
    tx_format -- it is the format of the transaction
    """
    print("="*50)
    index = 1
    for tx_input in tx.get_tx_inputs():
        print(f"{index}.Transaction Input:")
        print(" "*4, f"Transaction Hash: {tx_input.tx_hash}")
        print(" "*4, f"UTXO Index: {tx_input.utxo_index}")
        print(" "*4, f"Unlock Script: {tx_input.unlock_script}")
        index += 1
    index = 1
    for utxo in tx.get_utxos():
        print(f"{index}.Unspent Transaction Output:")
        print(" "*4, f"Value: {satoshi_to_btc(utxo.value)} BTC")
        print(" "*4, f"Lock Script: {utxo.lock_script}")
        index += 1
    print("="*50)

def print_txs(tx_format_arr):
    """Prints trasaction data using a format

    Keyword arguments:
    tx_format_arr -- it is an array of transaction formats
    """
    index = 1
    for tx_format in tx_format_arr:
        print_tx(tx_format, str(index))
        index+=1

def print_block(block):
    """Prints the data of a block using a format

    Keyword arguments:
    block_format -- it is the format of the block
    """
    print("="*50)
    header = block.header
    print(f"Author: {block.author}")
    print(f"Previous Hash: {header.prev_hash}")
    print(f"Root Hash: {header.root_hash}")
    print(f"Height: {header.height}")
    print(f"Difficulty: {header.difficulty}")
    print(f"Nonce: {header.nonce}")
    print(f"Date: {block.date}")
    print("Transactions:")
    for tx in block.txs:
        print_tx(tx)
    print("="*50)