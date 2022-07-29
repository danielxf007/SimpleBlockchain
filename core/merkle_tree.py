import hashlib
import math

def create_merkle_tree(hash_arr):
    """Returns a dictionary with the root, the structure of the tree and
    the number of bits needed to represent all the hashes

    Keyword arguments:
    hash_arr -- it is an array of hashes which are going to be used to build the tree
    """
    if len(hash_arr) == 0:
        return None
    arr_len = len(hash_arr)
    tree = []
    for i in range(0, arr_len if not (arr_len & 1) else arr_len-1, 2):
        left_leaf = hashlib.sha256(hash_arr[i].encode()).hexdigest()
        right_leaf = hashlib.sha256(hash_arr[i+1].encode()).hexdigest()
        concat_hash = hashlib.sha256((left_leaf+right_leaf).encode()).hexdigest()
        tree.append((concat_hash, left_leaf, right_leaf))
    if arr_len & 1:
        left_leaf = hashlib.sha256(hash_arr[arr_len-1].encode()).hexdigest()
        concat_hash = hashlib.sha256((left_leaf+left_leaf).encode()).hexdigest()
        tree.append((concat_hash, left_leaf))
    tree_len = len(tree)
    while tree_len != 1:
        aux = []
        for i in range(0, tree_len if not (tree_len & 1) else tree_len-1, 2):
            left_node = tree[i]
            right_node = tree[i+1]
            concat_hash = hashlib.sha256((left_node[0]+right_node[0]).encode()).hexdigest()
            aux.append((concat_hash, left_node, right_node))
        if tree_len & 1:
            left_node = tree[tree_len-1]
            concat_hash = hashlib.sha256((left_node[0]+left_node[0]).encode()).hexdigest()
            aux.append((concat_hash, left_node))       
        tree = aux
        tree_len = len(tree)
    return {'root': tree[0][0], 'structure': tree[0], 'n_bits': math.ceil(math.log2(len(hash_arr)))}

def proof(root, merkle_path, hash):
    proof_root = hashlib.sha256(hash.encode()).hexdigest()
    for hash_node in merkle_path:
        if hash_node[0]:
            proof_root = hashlib.sha256((proof_root+hash_node[1]).encode()).hexdigest()
        else:
            proof_root = hashlib.sha256((hash_node[1]+proof_root).encode()).hexdigest()
    return root == proof_root