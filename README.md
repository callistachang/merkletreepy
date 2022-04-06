```
                _   _     _
  _ __  ___ _ _| |_| |___| |_ _ _ ___ ___ _ __ _  _
 | '  \/ -_) '_| / / / -_)  _| '_/ -_) -_) '_ \ || |
 |_|_|_\___|_| |_\_\_\___|\__|_| \___\___| .__/\_, |
                                         |_|   |__/
```

# MerkleTree.py

> A Python port of merkletreejs. _:warning: Currently super unstable and doesn't work for many cases yet. :warning:_

[![PyPI version](https://badge.fury.io/py/merkletreepy.svg)](https://badge.fury.io/py/merkletreepy)

## Installation

```
pip install merkletreepy
```

## Working Code Examples

### sha256

```py
from merkletreepy import MerkleTree
import hashlib

def sha256(x):
    return hashlib.sha256(x).digest()

leaves = [sha256(leaf.encode()) for leaf in "abc"]
tree = MerkleTree(leaves, sha256)
root = tree.get_root()
leaf = sha256("a".encode())
bad_leaf = sha256("x".encode())
proof = tree.get_proof(leaf)
tree.verify(proof, leaf, root)      # returns True
tree.verify(proof, bad_leaf, root)  # returns False
```

### keccak256 (as implemented in the Solidity language)

```py
from merkletreepy import MerkleTree
import Web3

def hash_function(x):
    return Web3.keccak(text=x).hex()

leaves = [hash_function(leaf) for leaf in "abc"]
tree = MerkleTree(leaves, sha256)
root = tree.get_root()
leaf = sha256("a")
bad_leaf = sha256("x")
proof = tree.get_proof(leaf)
tree.verify(proof, leaf, root)      # returns True
tree.verify(proof, bad_leaf, root)  # returns False
```
