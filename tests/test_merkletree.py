from merkletreepy import MerkleTree
import hashlib
from web3 import Web3
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))


def sha256(x):
    return hashlib.sha256(x.encode("utf-8")).hexdigest()


def web3_solidity_keccak(x):
    return Web3.keccak(text=x).hex()


def test_sha256():
    leaves = [sha256(leaf) for leaf in "abc"]
    tree = MerkleTree(leaves, sha256)
    root = tree.get_root()
    leaf = sha256("a")
    bad_leaf = sha256("x")
    proof = tree.get_proof(leaf)
    assert tree.verify(proof, leaf, root) == True
    assert tree.verify(proof, bad_leaf, root) == False


def test_web3_solidity_keccak():
    leaves = [
        "0xAC0D2DC707C62C151135149DB9AD83BB29DA7AFE",
        "0x435731F32287ED87C4B8A3BA842372BDBF192B5C",
        "0x435731F32287ED87C4B8A3BA842372BDBF192B5C",
    ]
    hashed_leaves = [web3_solidity_keccak(leaf) for leaf in leaves]
    tree = MerkleTree(hashed_leaves, web3_solidity_keccak)
    root = tree.get_root()
    leaf = hashed_leaves[0]
    bad_leaf = "0x635731F32287ED87C4B8A3BA842372BDBF192B5D"
    proof = tree.get_proof(leaf)
    assert tree.verify(proof, leaf, root) == True
    assert tree.verify(proof, bad_leaf, root) == False
