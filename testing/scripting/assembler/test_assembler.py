import os
import sys
import filecmp
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
root_dir = os.path.dirname(root_dir)
sys.path.append(root_dir)
from core.scripting.assembler import Assembler

class TestAssembler:

    assembler = Assembler()
    
    def test_push_constants(self):
        source_path = "./test_files/input/constants.s"
        target_path = "./test_files/output/constants.btc"
        expected_path = "./test_files/output/constants_expected.btc"
        result = {}
        with open(source_path, 'r') as source_file, open(target_path, 'wb') as target_file:
            source_file_content = source_file.read()
            result = self.assembler.assemble(source_file_content)
            target_file.write(result["binary"])
        assert result["success"] == True
        assert filecmp.cmp(target_path, expected_path) == True

"""assembler = Assembler()
source_path = "./test_files/input/constants.s"
target_path = "./test_files/output/constants.btc"
expected_path = "./test_files/output/constants.btc"
result = {}
with open(source_path, 'r') as source_file, open(target_path, 'wb') as target_file:
    source_file_content = source_file.read()
    result = assembler.assemble(source_file_content)
    print(result)"""