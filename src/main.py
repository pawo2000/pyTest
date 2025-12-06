from testsrv.pmanager import PManager

pw = PManager()

###########################

import redis
r = redis.Redis(host='redis', port=6379)

#import debugpy
#debugpy.listen(("0.0.0.0", 5678))
# #debugpy.wait_for_client()

###########################

from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World!"}

@app.get("/hits")
def read_root():
    r.incr("hits")
    return {"Number of hits": r.get("hits")}

@app.get("/add/{address}")
async def read_item(address: str):
    if(address == ""):
        return {"No address provided"}
    return pw.add(address, address);    

@app.get("/remove/{address}")
async def read_item(address: str):
    if(address == ""):
        return {"No address provided"}
    return pw.remove(address);    
