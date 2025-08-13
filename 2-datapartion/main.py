from fastapi import FastAPI, HTTPException
from ring import ConsistentHashRing

app = FastAPI(title="Key_Value Store")

# In memoory database. Simulate 3 nodes
store = {
    "NodeA" : {},
    "NodeB" : {},
    "NodeC" : {},
}

ring = ConsistentHashRing(list(store.keys()), replicas=5)

@app.put("/kv/{key}")
def create_update_key(key: str, value: str):

    #Fing the node where the key should map to
    node = ring.get_node(key)
    store[node][key] = value

    return {"message": f"{key} created on {node}"}


@app.get("/kv/{key}")
def get_value(key: str):
    
    #Fing the node where the key should map to
    node = ring.get_node(key)
    node_store = store[node]
    if key not in node_store:
        raise HTTPException(status_code=404, detail=f"{key} not found")
    return {key: node_store[key]}

@app.delete("/kv/{key}")
def delete_key(key: str):

    #Fing the node where the key should map to
    node = ring.get_node(key)
    node_store = store[node]
    if key not in node_store:
        raise HTTPException(status_code=404, detail=f"{key} not found")
    del node_store[key]
    return {"message": "Key deleted", "key": key}

@app.get("/kv")
def list_leys():
    return {"keys": {node: list(node_store.keys()) for node, node_store in store.items()}}







