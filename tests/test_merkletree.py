from merkletreepy import MerkleTree
import hashlib
from web3 import Web3
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))


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
    print(tree.get_hex_layers())
    assert tree.verify(proof, leaf, root) == True
    assert tree.verify(proof, bad_leaf, root) == False


# def test_web3_solidity_keccak():
#     leaves = [
#         "0xAC0D2DC707C62C151135149DB9AD83BB29DA7AFE",
#         "0x435731F32287ED87C4B8A3BA842372BDBF192B5C",
#         "0x435731F32287ED8712313241232372BDBF192B5C",
#     ]
#     hashed_leaves = [web3_solidity_keccak(leaf) for leaf in leaves]
#     tree = MerkleTree(hashed_leaves, web3_solidity_keccak, sort=True)
#     root = tree.get_root()
#     leaf = hashed_leaves[0]
#     proof = tree.get_proof(leaf)
#     hex_proof = tree.get_hex_proof(leaf)
#     with open("lmao.txt", "w") as f:
#         f.write(root + "\n")
#         f.write(leaf + "\n")
#         f.write(str(hex_proof) + "\n")
#     # print(tree.layers)
#     print(hashed_leaves)
# assert tree.verify(proof, leaf, root) == True
# assert leaf == "0xc846e6f2516ffd49b5c964bf2561a93c660556fb944258fc72e9717fe512d08f"
# assert root == "0xef646858ccb735bfb84092c5ca117239f3b172c18cfcc2d20f18b406a82c3f60"
# assert hex_proof == ["0x81fa386dda29ea83366435371ea9ecfaa2fb699489a479adb00e400fff46be69"]


# def test_pls():
#     f = sha256
#     hashed_leaves = [f(leaf.encode()) for leaf in "abcd"]
#     tree = MerkleTree(hashed_leaves, f)
#     root = tree.get_root()
#     leaf = bytearray.fromhex(f("a"))
#     proof = tree.get_proof(leaf)
#     bleaf = bytearray.fromhex(f("b"))

#     print(leaf)
#     print(bleaf)
#     # print(b"".join([leaf, bleaf]))
#     # print(f(b"".join([leaf.encode(), bleaf.encode()])))
#     # print(bytes([leaf, bleaf]))

#     print("layers:", tree.get_hex_layers())
#     print("root:", tree.get_hex_root())
#     print("leaf:", leaf)
#     print("proof:", tree.get_hex_proof(leaf))
#     assert tree.verify(proof, leaf, root) == True
