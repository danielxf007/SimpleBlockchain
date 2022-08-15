import os
import sys
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
root_dir = os.path.dirname(root_dir)
sys.path.append(root_dir)
from core.scripting.assembler import Assembler
from core.scripting.btc_vm import BTCVM

class TestBTCVM:
    assembler = Assembler()
    vm = BTCVM()

    def test_equations(self):
        self.vm.reset()
        source_path = "./test_files/equations.s"
        expected_stack = [
        (1).to_bytes(length=1, byteorder='little', signed=True),
        (1).to_bytes(length=1, byteorder='little', signed=True),
        (1).to_bytes(length=1, byteorder='little', signed=True),
        (0).to_bytes(length=1, byteorder='little', signed=True)
        ]
        result = {}
        with open(source_path, 'r') as source_file:
            source_file_content = source_file.read()
            assemble_result = self.assembler.assemble(source_file_content)
            result = self.vm.process(assemble_result["binary"])
        assert result["success"] == True
        assert self.vm.get_stack() == expected_stack

    def test_hash_puzzle(self):
        self.vm.reset()
        source_path = "./test_files/hash_puzzle.s"
        expected_stack = []
        result = {}
        with open(source_path, 'r') as source_file:
            source_file_content = source_file.read()
            assemble_result = self.assembler.assemble(source_file_content)
            result = self.vm.process(assemble_result["binary"])
        print(result)
        assert result["success"] == True
        assert self.vm.get_stack() == expected_stack


"""assembler = Assembler()
vm = BTCVM()
source_path = "./test_files/push_data.s"
result = {}
with open(source_path, 'r') as source_file:
    source_file_content = source_file.read()
    assemble_result = assembler.assemble(source_file_content)
    print(assemble_result)
    result = vm.process(assemble_result["binary"])
    print(result)"""