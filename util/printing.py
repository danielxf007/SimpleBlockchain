def print_messages(messages):
    """Prints the given messages

    Keyword arguments:
    messages -- it is an array of strings
    """
    for message in messages:
        print(message)

def print_tx(tx_format, str_index):
    """Prints a trasaction data using a format

    Keyword arguments:
    tx_format -- it is the format of the transaction
    """
    if(len(tx_format) == 1):
        print(" "*4, f"Transaction {str_index} (Coinbase):")
        print(" "*8, tx_format["transfer"])
    else:
        print(" "*4, f"Transaction {str_index}:")
        print(" "*8, tx_format["transfer"])
        print(" "*8, tx_format["change"])

def print_txs(tx_format_arr):
    """Prints trasaction data using a format

    Keyword arguments:
    tx_format_arr -- it is an array of transaction formats
    """
    index = 1
    for tx_format in tx_format_arr:
        print_tx(tx_format, str(index))
        index+=1

def print_block(block_format):
    """Prints the data of a block using a format

    Keyword arguments:
    block_format -- it is the format of the block
    """
    if not block_format["Err"]:
        print("="*block_format["n_sep_lines"])
        print(block_format["author"])
        print(block_format["prev_hash"])
        print(block_format["root_hash"])
        print(block_format["height"])
        print(block_format["difficulty"])
        print(block_format["nonce"])
        print(block_format["date"])
        print("Transactions: ")
        print_txs(block_format["txs"])
        print("="*block_format["n_sep_lines"])
    else:
        print(block_format["Err"])