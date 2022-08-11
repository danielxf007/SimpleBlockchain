import os
import sys
import filecmp
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
root_dir = os.path.dirname(root_dir)
sys.path.append(root_dir)
from core.scripting.assembler import Assembler

class TestAssembler:

    assembler = Assembler()
    
    def test_push_data(self):
        source_path = "./test_files/input/push_data.s"
        target_path = "./test_files/output/push_data.btc"
        expected_path = "./test_files/output/push_data_expected.btc"
        result = {}
        with open(source_path, 'r') as source_file, open(target_path, 'wb') as target_file:
            source_file_content = source_file.read()
            result = self.assembler.assemble(source_file_content)
            target_file.write(result["binary"])
        assert result["success"] == True
        assert filecmp.cmp(target_path, expected_path) == True