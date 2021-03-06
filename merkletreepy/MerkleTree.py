from typing import List, Any, Callable, Dict, Optional
from hexbytes import HexBytes


class MerkleTree:
    def __init__(
        self, leaves: List[Any], hash_function: Callable, sort: Optional[bool] = False
    ) -> None:
        self.hash_function = self.bufferify_function(hash_function)
        self.leaves = leaves
        self.sort_leaves = sort
        self.sort_pairs = sort
        self._process_leaves()

    @staticmethod
    def to_hex(value: Any) -> str:
        return value.hex()

    @staticmethod
    def bufferify(value: str) -> str:
        if type(value) == bytes:
            return value
        else:
            return value.encode()

    @staticmethod
    def bufferify_function(func: Callable) -> Callable:
        def f(val):
            return MerkleTree.bufferify(func(val))

        return f

    def _process_leaves(self) -> None:
        self.leaves = [self.bufferify(leaf) for leaf in self.leaves]
        if self.sort_leaves:
            self.leaves.sort()
        self.layers = [self.leaves]
        self._create_hashes(self.leaves)

    def _create_hashes(self, nodes: List[Any]) -> None:
        while len(nodes) > 1:
            n = len(nodes)
            layer_index = len(self.layers)
            self.layers.append([])
            for i in range(0, n, 2):
                if n == i + 1 and n % 2 == 1:
                    self.layers[layer_index].append(nodes[i])
                    continue
                left = self.bufferify(nodes[i])
                right = left if i + 1 == n else self.bufferify(nodes[i + 1])
                combined = (
                    left + right
                    if not (self.sort_pairs and right > left)
                    else right + left
                )
                hashed_data = self.hash_function(combined)
                self.layers[layer_index].append(hashed_data)
            nodes = self.layers[layer_index]

    def get_hex_layers(self) -> List[str]:
        return [[self.to_hex(leaf) for leaf in layer] for layer in self.layers]

    def get_root(self) -> str:
        try:
            return self.layers[-1][0]
        except IndexError:
            return []

    def get_hex_root(self) -> str:
        if self.get_root():
            return self.to_hex(self.get_root())
        else:
            return []

    def get_proof(self, leaf: str, index: Optional[int] = None) -> List[Dict[str, Any]]:
        proof = []
        leaf = self.bufferify(leaf)
        if not index:
            try:
                index = self.leaves.index(leaf)
            except ValueError:
                return []

        for layer in self.layers:
            is_right_node = index % 2
            pair_index = index - 1 if is_right_node else index + 1
            if pair_index < len(layer):
                proof.append(
                    {
                        "position": "left" if is_right_node else "right",
                        "data": layer[pair_index],
                    }
                )
            index = index // 2
        return proof

    def get_hex_proof(self, leaf: str, index: Optional[int] = 0) -> List[str]:
        return [self.to_hex(item["data"]) for item in self.get_proof(leaf, index)]

    def verify(self, proof: List[Dict[str, str]], target_node: str, root: str) -> bool:
        hash = self.bufferify(target_node)
        root = self.bufferify(root)
        for node in proof:
            data = self.bufferify(node["data"])
            is_left_node = node["position"] == "left"
            if self.sort_pairs:
                combined = data + hash if data <= hash else hash + data
            else:
                combined = data + hash if is_left_node else hash + data
            hash = self.hash_function(combined)
        return hash == root

    def get_depth(self) -> int:
        return len(self.layers) - 1

    def reset_tree(self) -> None:
        self.leaves = []
        self.layers = []
