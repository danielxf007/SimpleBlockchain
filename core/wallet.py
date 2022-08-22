from core.blockchain import Blockchain
from core.data_bases.utxo_reference_db import UTXOReferenceDB
from core.transactions.tx import TX
from core.transactions.tx_in import TXIn
from core.transactions.utxo import UTXO
from core.scripting.assembler import Assembler
from core.scripting.btc_vm import BTCVM
from util.conversions import satoshi_to_btc

class WalletErrorMssgs:
    SPENT_UTXO = "The utxo has been already spent by someone else"
    UNLOCK_SCRIPT = "The utxo could not be unlock with the given unlock script"

class Wallet:
    """This class allows the user to create transactions """

    def __init__(self, private_key, public_key, blocks, utxo_references):
        """Creates an instance of two databases and copies their current state

        Keyword arguments:
        private_key -- it is a SigningKey object assigned to this wallet
        public_key -- it is an object which will be used to verify signatures, it was 
        generated from the corresonding SigningKey object
        blocks -- it is a copy of the current state of the global blockchain
        utxo_reference_db_state -- it is a copy of the current state of the unspent 
        transaction out references database
        """
        self.private_key = private_key
        self.public_key = public_key
        self.blockchain = Blockchain(blocks)
        self.utxo_reference_db = UTXOReferenceDB(utxo_references)
        self.assembler = Assembler()
        self.btcvm = BTCVM()
        self.tx_inputs = []
        self.utxos = []

    def get_private_key(self):
        """Returns the private key as an hexadecimal string"""
        return self.private_key.to_string().hex()
    
    def get_public_key(self):
        """Returns the public key as an hexadecimal string"""
        return self.public_key.to_string().hex()

    def set_blocks(self, blocks):
        """Changes the data blockchain state

        Keyword arguments:
        blocks -- it is the global state of the chain
        """
        self.blockchain.set_blocks(blocks)
    
    def set_utxo_references(self, utxo_references):
        """Changes the references on the references db

        Keyword arguments:
        utxo_references -- it is a copy of the global state of the unspent transaction
        out references
        """
        self.utxo_reference_db.set_references(utxo_references)
    
    def available_utxo(self, tx_hash, utxo_index):
        return self.utxo_reference_db.has_reference(tx_hash, utxo_index)
    
    def unlock_utxo(self, tx_hash, utxo_index, unlock_script_path):
        result = {"success": True, "err": ""}
        try:
            with open(unlock_script_path, 'r') as unlock_script_file:
                if not self.available_utxo(tx_hash, utxo_index):
                    raise Exception(f"{tx_hash}, {utxo_index}. {WalletErrorMssgs.SPENT_UTXO}")
                unlock_script = unlock_script_file.read()
                utxo = self.blockchain.get_utxo(tx_hash, utxo_index)
                lock_script = utxo.lock_script
                assembly_result = self.assembler.assemble(unlock_script+lock_script)
                if assembly_result["success"]:
                    self.btcvm.reset()
                    processing_result = self.btcvm.process(assembly_result["binary"])
                    if processing_result["success"]:
                        if self.btcvm.on_valid_state():
                            result["script"] = unlock_script
                            return result
                        else:
                            raise Exception(WalletErrorMssgs.UNLOCK_SCRIPT)
                    else:
                        raise Exception(processing_result["err"])
                else:
                    raise Exception(assembly_result["err"])
        except Exception as e:
            result["success"] = False
            result["err"] = f"{e}"
        return result
    
    def create_tx_input(self, tx_hash, utxo_index, unlock_script_path):
        unlock_result = self.unlock_utxo(tx_hash, utxo_index, unlock_script_path)
        if unlock_result["success"]:
            self.tx_inputs.append(TXIn(tx_hash, utxo_index, unlock_result["script"]))
        return unlock_result
    
    def remove_tx_input(self, index):
        result = {"success": True, "err": ""}
        if len(self.tx_inputs) > 0 and len(self.tx_inputs) >= index:
            self.tx_inputs.remove(self.tx_inputs[index-1])
            return result
        result["success"] = False
        result["err"] = f"The input does not exist at {index}"
        return result
    
    def get_tx_inputs(self):
        return self.tx_inputs

    def get_available_utxos(self):
        """Returns the unspent transaction outputs this wallet is going to spend"""
        utxos = []
        for tx_in in self.tx_inputs:
            utxo = self.blockchain.get_utxo(tx_in.tx_hash, tx_in.utxo_index)
            utxos.append(utxo)
        return utxos
    
    def create_utxo(self, value, lock_script_path):
        result = {"success": True, "err": ""}
        try:
            with open(lock_script_path, 'r') as lock_script_file:
                lock_script = lock_script_file.read()
                assembly_result = self.assembler.assemble(lock_script)
                if assembly_result["success"]:
                    self.utxos.append(UTXO(value, lock_script))
                else:
                    raise Exception(assembly_result["err"])                        
        except Exception as e:
            result["success"] = False
            result["err"] = f"{e}"
        return result

    def remove_utxo(self, index):
        result = {"success": True, "err": ""}
        if len(self.utxos) > 0 and len(self.utxos) >= index:
            self.utxos.remove(self.utxos[index-1])
            return result
        result["success"] = False
        result["err"] = f"The utxo does not exist at {index}"
        return result
    
    def get_utxos(self):
        return self.utxos
    
    def get_utxos_total_value(self, utxos):
        """
        """
        total_value = 0
        for utxo in utxos:
            total_value += utxo.value
        return total_value

    def create_tx(self, system_fee):
        """Returns a transaction which used the tx_inputs and utxos created by the wallet

        The total value that will be spent as input has to be greater or equal than the total
        value that will be outputed.

        Be careful, the fee that will be payed to the miner will be
        total_value_in - total_value_out = fee

        The list of tx inputs and utxos will be cleared after creating the transaction

        Keyword arguments:
        system_fee -- it is an amount of satohsi that is payed for using the system
        at the current time which will be payed to a miner
        """
        result = {"success": True, "err": "", "tx": None}
        total_value_in = self.get_utxos_total_value(self.get_available_utxos())
        total_value_out = self.get_utxos_total_value(self.utxos)
        if total_value_in < total_value_out:
            result["success"] = False
            result["err"] = f"The transaction could not be created the inputs {satoshi_to_btc(total_value_in)} BTC cannot cover the outputs {satoshi_to_btc(total_value_out)} BTC"
        fee = total_value_in-total_value_out
        if fee < system_fee:
            result["success"] = False
            result["err"] = f"The transactions is paying {satoshi_to_btc(fee)} BTC instead of {satoshi_to_btc(system_fee)} BTC"
        result["tx"] = TX(self.tx_inputs.copy(), self.utxos.copy())
        self.tx_inputs.clear()
        self.utxos.clear()
        return result