import hashlib
import bisect

class ConsistentHashRing:
    def __init__(self, nodes=None, replicas=3):
        self.replicas = replicas # number of virtual nodes for a given node to be place on ring
        self.nodes = set() # Nodes in the ring. Total entries = replicas * len(nodes)
        self.ring = dict() #data structure onto which nodes and keys are mapped
        self._keys = [] # data structure for key lookup by hash value for insertion, retrieval, deletion

        if nodes:
            for node in nodes:
                self.add_node(node)

    def _hash(self, key: str):
        """Returns hash value"""
        ## md5 method take bytes argument and hence encode, which is converted to base10 integer from hex
        return int(hashlib.md5(key.encode("utf-8")).hexdigest(),16)

    def add_node(self, node):
        """Add nodes(virtual replicas) to the ring"""
        self.nodes.add(node)
        for i in range(self.replicas):
            virt_node = f"{node}#{i}"
            hash_val = self._hash(virt_node)
            self.ring[hash_val] = node
            bisect.insort(self._keys, hash_val)

    def get_nodes(self, key: str, Rf: int):
        """Get the nodes that should hold the given key per replication factor"""
        
        #handle the case when no key is added
        if len(self._keys) == 0:
            return []
        
        selected_nodes = list()
        key_hash = self._hash(key)
        
        # Get the index of this hash. As index returned by bisect could be out of bound for given hash
        # modulo opeorator bound it to the size of _keys structure and also makes the ring circular
        start_idx = bisect.bisect(self._keys, key_hash) % len(self._keys)
        i = start_idx
        while len(selected_nodes) < Rf:
            node = self.ring[self._keys[i % len(self._keys)]]
            if node not in selected_nodes:
                selected_nodes.append(node)
            i += 1
        
        return selected_nodes
            


        #Use idx to the get node in the ring
        return self.ring[self._keys[idx]]
    
    def remove_node(self, node):
        """Removes the node (vnodes) from the ring"""
        ##To be implmented in later chapters. Let's keep it simple.