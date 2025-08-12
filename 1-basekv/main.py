from fastapi import FastAPI, HTTPException

app = FastAPI(title="Key_Value Store")

# In memoory database
store = {}

@app.put("/kv/{key}")
def create_update_key(key: str, value: str):
    store[key] = value
    return {"message": f"{key} created"}


@app.get("/kv/{key}")
def get_value(key: str):
    if key not in store:
        raise HTTPException(status_code=404, detail=f"{key} not found")
    return {key: store.get(key)}

@app.delete("/kv/{key}")
def delete_key(key: str):
    if key not in store:
        raise HTTPException(status_code=404, detail=f"{key} not found")
    del store[key]
    return {"message": "Key deleted", "key": key}

@app.get("/kv")
def list_leys():
    return {"keys": list(store.keys())}


