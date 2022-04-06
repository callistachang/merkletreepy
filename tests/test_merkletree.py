from merkletreepy import MerkleTree
import hashlib
from web3 import Web3
import sys
import os


def sha256(x):
    return hashlib.sha256(x).digest()


def web3_solidity_keccak(x):
    return Web3.keccak(text=x).hex()


def test_sha256():
    leaves = [sha256(leaf.encode()) for leaf in "abc"]
    tree = MerkleTree(leaves, sha256)
    root = tree.get_root()
    leaf = sha256("a".encode())
    bad_leaf = sha256("x".encode())
    proof = tree.get_proof(leaf)
    assert tree.verify(proof, leaf, root) == True
    assert tree.verify(proof, bad_leaf, root) == False
