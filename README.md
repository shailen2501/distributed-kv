# distributed-kv

The repo implements a relative simpler design for a distributed key value with a foucs to understand important distributed concepts. The folders represents the concepts and build on top of each other.

My hope in creating this repo is to refresh and implement these concepts  and in doing so, if this has helped you, please give a shout out!

Step up instructions
Project is implemented in Python and FastAPI. I have purposely not used libraries to code the concepts but instead implemented them in pure python to understand the concept deeply.

I am ssuming you know how to install Python and FastAPI, always a google search away.

Repo Structure
## 1-basekv
this is a basic implementation with a single node that provides in memory storage, exposes 4 endpoints for CRUD.

Run app:

(venv) cd <base_path>\distributed-kv\1-basekv > uvicorn main:app --reload

This should start a webserver on port 8000, Luanch browser at http://127.0.0.1:8000 

Go to http://127.0.0.1:8000 and explore the endpoints and expirment with few key and values

## 2-datapartion
the folder implement data partitioning into multiple logical store on the same machine. In later chapters, I'll create a vesrion where stores reside on seperate machines (possibly simulate it with docker)

Consistent hashing technique is used to distribute keys across nodes without rehashing everything when nodes are added or removed as opposed to normal hashing.

