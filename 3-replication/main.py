from fastapi import FastAPI, HTTPException
from ring import ConsistentHashRing
import random
import uvicorn

app = FastAPI(title="Key_Value Store")

# In memoory database. Simulate 3 nodes
store = {
    "NodeA" : {},
    "NodeB" : {},
    "NodeC" : {},
}

ring = ConsistentHashRing(list(store.keys()), replicas=5)
Rf = 3 # Replication factor (number of nodes a key should reside on)
READ_Q = 2 # Number of nodes that must return for successful read
WRITE_Q = 2 # Number of nodes that must return successful write

@app.put("/kv/{key}")
def create_update_key(key: str, value: str):

    #Fing the nodes where the key should map to
    nodes = ring.get_nodes(key, Rf)
    successful_writes = 0
    for node in nodes:
        store[node][key] = value
        successful_writes += 1
    
    if successful_writes >= WRITE_Q:
        return {"message": f"{key} created on {successful_writes} {nodes}"}
    else:
        raise HTTPException(status_code=500, detail="Write Quorom not met")


@app.get("/kv/{key}")
def get_value(key: str):
    
    #Fing the node where the key should map to
    nodes = ring.get_nodes(key, Rf)
    responses = []
    for node in nodes:
        node_store = store[node]
        if key in node_store:
            responses.append(node[key])

    if len(responses) >= READ_Q:
        return {key : random.choice(responses)} #in later chapter this random selection will be replced by versioning
    else:
        raise HTTPException(status_code=404, detail=f"{key} not found")
    

@app.delete("/kv/{key}")
def delete_key(key: str):

    nodes = ring.get_nodes(key, Rf)
    success_count = 0
    for node in nodes:
        node_store = store[node]
        if key in node_store:
            del node_store[key]
            success_count += 1
    if success_count >= WRITE_Q:
        return {"message": "Delete successful", "key": key, "deleted_from": nodes[:success_count]}
    else:
        raise HTTPException(status_code=404, detail="Key not found or delete quorum not met")


@app.get("/kv")
def list_leys():
    return {"keys": {node: list(node_store.keys()) for node, node_store in store.items()}}




if __name__== "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)



