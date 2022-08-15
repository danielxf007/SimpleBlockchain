import os
import sys
import filecmp
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
root_dir = os.path.dirname(root_dir)
sys.path.append(root_dir)
from core.scripting.assembler import Assembler

class TestAssembler:

    assembler = Assembler()

    def assemble(self, source_path, target_path):
        result = {}
        with open(source_path, 'r') as source_file, open(target_path, 'wb') as target_file:
            source_file_content = source_file.read()
            result = self.assembler.assemble(source_file_content)
            target_file.write(result["binary"])
        return result
    
    def test_push_constants(self):
        source_path = "./test_files/input/constants.s"
        target_path = "./test_files/output/constants.btc"
        expected_path = "./test_files/output/constants_expected.btc"
        result = self.assemble(source_path, target_path)
        assert result["success"] == True
        assert filecmp.cmp(target_path, expected_path) == True
    
    def test_arithmetic(self):
        source_path = "./test_files/input/arithmetic.s"
        target_path = "./test_files/output/arithmetic.btc"
        expected_path = "./test_files/output/arithmetic_expected.btc"
        result = self.assemble(source_path, target_path)
        assert result["success"] == True
        assert filecmp.cmp(target_path, expected_path) == True