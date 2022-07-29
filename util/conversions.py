def btc_to_satoshi(btc, factor=10**8):
    """ Transforms bitcoin into satoshi

    Keyword arguments:
    btc -- it is the amount of bitcoin to convert
    factor -- it is the amount of satoshi equivalent to one bitcoin
    """
    return int(btc*factor)

def satoshi_to_btc(satoshi, factor=10**8):
    """ Transforms satoshi into bitcoin

    Keyword arguments:
    satoshi -- it is the amount of satoshi to convert
    factor -- it is the amount of satoshi equivalent to one bitcoin
    """    
    return satoshi/factor