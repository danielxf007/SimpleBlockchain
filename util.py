class Util:

    def btc_to_satoshi(self, btc, factor=10**8):
        return int(btc*factor)
    
    def satoshi_to_btc(self, satoshi, factor=10**8):
        return satoshi/factor