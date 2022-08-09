import os
import sys
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
root_dir = os.path.dirname(root_dir)
sys.path.append(root_dir)
from core.scripting.btc_vm import BTCVM